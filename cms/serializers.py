import time
import os
from rest_framework import serializers
from cms import constants
from cms.models import CmsUsersMaster, UsersContent
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from cms import error_messages, helpers
from django.core.exceptions import ValidationError
from cms.shared import save_file
from django.conf import settings


class RegistrationSerializer(serializers.Serializer):
    email_id = serializers.CharField(max_length=100, required=True, validators=[constants.email_id_regex])
    password = serializers.CharField(max_length=8, required=True, validators=[constants.password_regex])
    full_name = serializers.CharField(max_length=100, required=True)
    address = serializers.CharField(max_length=200, required=False)
    city = serializers.CharField(max_length=60, required=False)
    state = serializers.CharField(max_length=60, required=False)
    country = serializers.CharField(max_length=60, required=False)
    pincode = serializers.CharField(max_length=60, required=True)

    def create(self, value):
        cms_user_obj = CmsUsersMaster.objects.create(
            email_id=value.get("email_id", None),
            full_name=value.get("full_name", None),
            address=value.get("address", None),
            city=value.get("city", None),
            state=value.get("state", None),
            country=value.get("country", None),
            pincode=value.get("pincode", None)
        )

        cms_user_obj.password = make_password(value.get("password"))
        cms_user_obj.save()

    def get(self, value):
        try:
            kwargs = {}
            if value.get("email_id"):
                kwargs.update({"email_id": value.get("email_id")})
            cms_user_obj = CmsUsersMaster.objects.get(**kwargs)
            return cms_user_obj
        except Exception as ex:
            return False


class AuthUserSerializer(serializers.Serializer):
    def create(self, value):
        user = User(username=value.get("email_id"))
        user.password = make_password(value.get("password"))
        user.save()

    def get(self, value):
        try:
            kwargs = {}
            if value.get("email_id"):
                kwargs.update({"username": value.get("email_id")})
            auth_user_obj = User.objects.get(**kwargs)
            return auth_user_obj
        except Exception as ex:
            return False


class LoginSerializer(serializers.Serializer):
    email_id = serializers.CharField(max_length=100, required=True, validators=[constants.email_id_regex])
    password = serializers.CharField(max_length=8, required=True)

    def check_valid(self, value):
        try:
            kwargs = {}
            if value.get("email_id"):
                kwargs.update({"email_id": value.get("email_id")})
            cms_user_obj = CmsUsersMaster.objects.get(
                **kwargs
            )
        except Exception as ex:
            return error_messages.USER_IS_NOT_REGISTERED, False
        if not check_password(value.get("password"), cms_user_obj.password):
            return error_messages.PASSWORD_IS_INCORRECT, False
        try:
            user = User.objects.get(username=value.get("email_id"))
            if not check_password(value.get("password"), user.password):
                user.password = make_password(value.get("password"))
                user.save()
            return cms_user_obj, True
        except Exception as ex:
            return error_messages.IN_VALD_REQUEST, False


class CmsUsersModelSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id')

    class Meta:
        model = CmsUsersMaster
        fields = ['user_id', 'role_type', 'email_id', 'full_name']


class UsersContentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30, required=True)
    body = serializers.CharField(max_length=300, required=True)
    summary = serializers.CharField(max_length=60, required=True)
    categories = serializers.CharField(max_length=60, required=True)
    pdf = serializers.CharField()

    def validate(self, value):
        if value.get("pdf", None):
            if not ("application/pdf" in value.get("pdf")):
                raise ValidationError('Invalid value')
        return True

    def get(self, value):
        try:
            kwargs = {}
            if value.get("content_id"):
                kwargs.update({"id": value.get("content_id")})
            if value.get("role_type") == constants.USER:
                if value.get("user"):
                    kwargs.update({"user": value.get("user")})
            cms_user_obj = UsersContent.objects.get(
                **kwargs
            )
            return cms_user_obj
        except Exception as ex:
            return False

    def create(self, value):
        users_content_obj = UsersContent.objects.create(
            user=value.get("user", None),
            title=value.get("title", None),
            body=value.get("body", None),
            summary=value.get("summary", None),
            categories=value.get("categories", None)
        )

        if value.get("pdf", None):
            file_path = settings.PDF_BASE_PATH + str(users_content_obj.id) + "_" + time.strftime(
                "%Y%m%d-%H%M%S") + ".pdf"
            save_file(value.get("pdf", None), file_path)
            users_content_obj.pdf_document_path = file_path
            users_content_obj.save()

    def update(self, value, user_content_obj):
        user_content_obj.title = value.get("title", user_content_obj.title)
        user_content_obj.body = value.get("body", user_content_obj.body)
        user_content_obj.summary = value.get("summary", user_content_obj.summary)
        user_content_obj.categories = value.get("categories", user_content_obj.categories)
        user_content_obj.save()

        if value.get("pdf", None):
            os.remove(user_content_obj.pdf_document_path)
            file_path = settings.PDF_BASE_PATH + str(user_content_obj.id) + "_" + time.strftime(
                "%Y%m%d-%H%M%S") + ".pdf"
            save_file(value.get("pdf", None), file_path)
            user_content_obj.pdf_document_path = file_path
            user_content_obj.save()

    def list(self, value):
        offset = value.get("offset", 0)
        limit = value.get("limit", 10)
        kwargs = {}
        if value.get("role_type") == constants.USER:
            if value.get("user"):
                kwargs.update({"user": value.get("user")})
        if value.get("title"):
            kwargs.update({"title__contains": value.get("title")})
        if value.get("body"):
            kwargs.update({"body__contains": value.get("body")})
        if value.get("summary"):
            kwargs.update({"summary__contains": value.get("summary")})
        if value.get("categories"):
            kwargs.update({"categories": value.get("categories")})
        if value.get("search"):
            entry_query = helpers.get_query(value.get("search"), [
                "title", "body", "summary", "categories"
            ])
            cms_user_obj = UsersContent.objects.filter(
                entry_query
            ).filter(**kwargs).all()[offset:offset + limit]
        else:
            cms_user_obj = UsersContent.objects.filter(**kwargs).all()[offset:offset + limit]
        return cms_user_obj

    def delete(self, value):
        try:
            kwargs = {}
            if value.get("content_id"):
                kwargs.update({"id": value.get("content_id")})
            if value.get("role_type") == constants.USER:
                if value.get("user"):
                    kwargs.update({"user": value.get("user")})
            cms_user_obj = UsersContent.objects.get(
                **kwargs
            )
            cms_user_obj.delete()
        except Exception as ex:
            return False


class UsersContentModelSerializer(serializers.ModelSerializer):
    content_id = serializers.IntegerField(source='id')

    class Meta:
        model = UsersContent
        fields = ["content_id", "title", "body", "summary", "pdf_document_path", "categories"]
