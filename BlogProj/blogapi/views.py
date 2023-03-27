import datetime
from .permissions import IsAdmin
from django.shortcuts import render
from .serializer import (UserSerializer,BlogViewSerializer,CommentSerializer,AdminUserSerializer)
from django.contrib.auth.models import User
from rest_framework import  generics,status
from rest_framework.viewsets import ModelViewSet,ViewSet
from .models import Blog,Comment
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import authentication,permissions
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from datetime import datetime
# Create your views here.
class UserModelViewsetView(ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    queryset = User.objects.all()

class BlogModelView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogViewSerializer
    queryset = Blog.objects.all()
    def create(self,request,*args,**kwargs):
        user=request.user
        serializer=BlogViewSerializer(data=request.data,context={"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self, request, *args, **kwargs):
        user=request.user
        id=kwargs.get("pk")
        blog=Blog.objects.filter(id=id)
        if blog:
            serializer = BlogViewSerializer(blog, many=True)
            return Response(serializer.data)
        else:
            return Response({"msg":"No post created till"})

    def update(self, request, *args, **kwargs):
        user=request.user
        id=kwargs.get("pk")
        blog=Blog.objects.get(author=user,id=id)
        blog.updated_date=datetime.now()
        serializer=BlogViewSerializer(instance=blog,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def destroy(self, request, *args, **kwargs):
        user=request.user
        id=kwargs.get("pk")
        blog=Blog.objects.get(author=user,id=id)
        serializer=BlogViewSerializer(blog)
        blog.delete()
        return Response({"Message": f"Blog of id {id} get deleted "})

    def list(self, request, *args, **kwargs):
        blog=Blog.objects.all()
        blog_lst=[]
        for bg in blog:
            usr=User.objects.get(id=bg.author_id)
            cmt=Comment.objects.filter(blog_id=bg.id)
            cmt_cnt=Comment.objects.filter(blog_id=bg.id).count()
            sumc=0
            for cm in cmt:
                sumc+=cm.rating
            if cmt_cnt==0:
                avg=0
            else:
                avg=sumc/cmt_cnt
            blog_lst.append({
                "Blog Title":bg.blog_title,
                "Blog Content":bg.content,
                "Blog Author":usr.first_name,
                "Total Comments":cmt_cnt,
                "Overall Rating":avg

            })
        return Response({"Blogs are":blog_lst})

class CommentModelView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    def create(self, request, *args, **kwargs):
        user=request.user
        id=self.request.POST["blog_id"]
        # print(id)
        blog=Blog.objects.get(id=id)
        serializer=CommentSerializer(data=request.data,context={"user":user,"blog":blog})
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Your review is added","data":serializer.data})
        else:
            return Response(serializer.errors)


    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        blog=Blog.objects.get(id=id)
        comment=Comment.objects.filter(blog_id=id)
        comment_data=[]
        for cm in comment:
            user=User.objects.get(id=cm.author_id)
            comment_data.append({
                "Author":user.first_name,
                "Comment":cm.comment,
                "Rating":cm.rating
            })
        return Response({"Blog name":blog.blog_title,"Comments are":comment_data})

    def update(self, request, *args, **kwargs):
        user=request.user
        id=kwargs.get("pk")
        comment=Comment.objects.get(id=id)
        if comment.author_id==user.id:
            comment.updated_date = datetime.now()
            if comment:
                serializer=CommentSerializer(instance=comment,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Update": "Your comment get updated","data":serializer.data})
                else:
                    return Response(serializer.errors)
        else:
            return Response("You dont have permission to update this comment....")

    def destroy(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get("pk")
        comment = Comment.objects.get(id=id)
        if comment.author_id == user.id:
            serializer = CommentSerializer(comment)
            comment.delete()
            return Response({"Message": f"comment of id {id} get deleted "})
        else:
            return Response("You dont have permission to delete this comment...")

class AdminCommentView(generics.RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes=[IsAdmin,]
    queryset = Comment.objects.all()
    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get("id")
        blog = Blog.objects.get(id=id)
        comment = Comment.objects.filter(blog_id=id)
        comment_data = []
        for cm in comment:
            user = User.objects.get(id=cm.author_id)
            comment_data.append({
                "Author": user.first_name,
                "Comment": cm.comment,
                "Rating": cm.rating
            })
        return Response({"Blog name": blog.blog_title, "Comments are": comment_data})

    def destroy(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get("id")
        comment = Comment.objects.get(id=id)

        serializer = CommentSerializer(comment)
        comment.delete()
        return Response({"Message": f"comment of id {id} get deleted "})

class AdminBlogRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = BlogViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes=[IsAdmin,]
    queryset = Blog.objects.all()
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("id")
        blog = Blog.objects.filter(id=id)
        if blog:
            serializer = BlogViewSerializer(blog, many=True)
            return Response(serializer.data)
        else:
            return Response({"msg": "No post created till"})

    def destroy(self, request, *args, **kwargs):
        user=request.user
        id=kwargs.get("id")
        blog=Blog.objects.get(id=id)
        serializer=BlogViewSerializer(blog)
        blog.delete()
        return Response({"Message": f"Blog of id {id} get deleted "})

class AdminBlogListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    permission_classes=[IsAdmin]
    serializer_class = BlogViewSerializer
    queryset = Blog.objects.all()

class AdminUserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    permission_classes=[IsAdmin,]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"Message":"Lgout successfully"})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


