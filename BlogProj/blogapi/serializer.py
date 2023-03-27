from rest_framework import serializers
from .models import Blog, Comment
from django.contrib.auth.models import User
from django.core.mail import send_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        username = self.validated_data['username']
        user = User.objects.create_user(**validated_data)
        send_mail(
            "Blog Platform : New User Registration",
            f"Created your account....Your username is  {username} and password is {password}",
            "remyapillai1988@gmail.com",
            [email]
        )
        return user


class BlogViewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    images = serializers.CharField(read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("user")
        return Blog.objects.create(author=user, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        exclude = ["id", "blog", "updated_date", "created_date"]

    def create(self, validated_data):
        user = self.context.get("user")
        blog = self.context.get("blog")
        return Comment.objects.create(author=user, blog_id=blog.id, **validated_data)


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

    def create(self, validated_data):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        username = self.validated_data['username']
        user = User.objects.create_superuser(**validated_data)
        send_mail(
            "Blog Platform : New Admin User Registration",
            f"Created your account....Your username is  {username} and password is {password}",
            "remyapillai1988@gmail.com",
            [email]
        )
        return user
