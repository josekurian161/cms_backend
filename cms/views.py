from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from cms.shared import logger_info
from rest_framework.permissions import IsAuthenticated
from cms import helpers
from cms.decorators import auth_cms_user


# Create your views here.
class Login(APIView):
    def post(self, request, *args, **kwargs):
        logger_info('login  Api Service  Started')
        return helpers.login(self, request)


class Registration(APIView):
    def post(self, request, *args, **kwargs):
        logger_info('Registration  Api Service  Started')
        return helpers.register(self, request)


class ListContent(APIView):
    permission_classes = [IsAuthenticated]

    @auth_cms_user
    def post(self, request, *args, **kwargs):
        logger_info('ListContent  Api Service  Started')
        return helpers.list_content(self, request)


class AddContent(APIView):
    permission_classes = [IsAuthenticated]

    @auth_cms_user
    def post(self, request, *args, **kwargs):
        logger_info('AddContent  Api Service  Started')
        return helpers.add_content(self, request)


class UpdateContent(APIView):
    permission_classes = [IsAuthenticated]

    @auth_cms_user
    def post(self, request, *args, **kwargs):
        logger_info('Registration  Api Service  Started')
        return helpers.update_content(self, request)


class DeleteContent(APIView):
    permission_classes = [IsAuthenticated]

    @auth_cms_user
    def delete(self, request, *args, **kwargs):
        logger_info('Registration  Api Service  Started')
        return helpers.delete_content(self, request)
