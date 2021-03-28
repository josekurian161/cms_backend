import re
from django.db.models import Q
from cms.serializers import RegistrationSerializer, AuthUserSerializer, LoginSerializer, CmsUsersModelSerializer, \
    UsersContentSerializer, UsersContentModelSerializer
from cms import shared, error_messages, constants
from rest_framework import status
from django.db import IntegrityError, connection, transaction


def login(self, request):
    try:
        with transaction.atomic():
            request_data = request.data
            is_valid = LoginSerializer(data=request_data).is_valid()
            if not is_valid:
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            cms_user_obj, is_valid = LoginSerializer.check_valid(self, value=request_data)
            if not is_valid:
                return shared.basic_response(message=cms_user_obj,
                                             status=status.HTTP_412_PRECONDITION_FAILED,
                                             view=self.get_view_name())

            serialized_data = CmsUsersModelSerializer(cms_user_obj, many=False).data
            auth_token = shared.generate_auth_token(self, password=request_data.get("password"),
                                                    username=request_data.get("email_id"))
            if not auth_token:
                return shared.basic_response(message=error_messages.SOMETHING_WENT_WRONG,
                                      status=status.HTTP_412_PRECONDITION_FAILED,
                                      view=self.get_view_name())
            print(auth_token)
            serialized_data["token"] = auth_token.get("token", None)
            response_translator = shared.response_translator(self, serialized_data)
            return shared.basic_response(message=response_translator,
                                         status=status.HTTP_200_OK,
                                         view=self.get_view_name())
    except Exception as ex:
        return shared.main_exception(self.get_view_name(), ex)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(" ", (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def register(self, request):
    try:
        with transaction.atomic():
            request_data = request.data
            is_valid = RegistrationSerializer(data=request_data).is_valid()
            if not is_valid:
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            is_exist = RegistrationSerializer.get(self, request_data)
            if is_exist:
                return shared.basic_response(message=error_messages.USER_ALREADY_EXIST,
                                             status=status.HTTP_412_PRECONDITION_FAILED,
                                             view=self.get_view_name())
            RegistrationSerializer.create(self, request_data)
            is_exist = AuthUserSerializer.get(self, request_data)
            if not is_exist:
                AuthUserSerializer.create(self, request_data)
            return shared.basic_response(message=error_messages.USER_REGISTERED_SUCCESSFULLY,
                                         status=status.HTTP_200_OK,
                                         view=self.get_view_name())
    except Exception as ex:
        return shared.main_exception(self.get_view_name(), ex)


def add_content(self, request):
    try:
        with transaction.atomic():
            request_data = request.data
            is_valid = UsersContentSerializer(data=request_data).is_valid()
            if not is_valid:
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            UsersContentSerializer.create(self, request_data)
            return shared.basic_response(message=error_messages.DATA_SAVED_SUCCESSFULLY,
                                         status=status.HTTP_200_OK,
                                         view=self.get_view_name())
    except Exception as ex:
        return shared.main_exception(self.get_view_name(), ex)


def update_content(self, request):
    try:
        with transaction.atomic():
            request_data = request.data
            if not request_data.get("content_id", None):
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            is_valid = UsersContentSerializer(data=request_data).is_valid()
            if not is_valid:
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            user_content_obj = UsersContentSerializer.get(self, request_data)
            if not user_content_obj:
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            UsersContentSerializer.update(self, request_data, user_content_obj)
            return shared.basic_response(message=error_messages.DATA_UPDATED_SUCCESSFULLY,
                                         status=status.HTTP_200_OK,
                                         view=self.get_view_name())
    except Exception as ex:
        return shared.main_exception(self.get_view_name(), ex)


def list_content(self, request):
    try:
        with transaction.atomic():
            request_data = request.data
            users_content_list = UsersContentSerializer.list(self, request_data)
            if not users_content_list:
                return shared.basic_response(message=error_messages.DATA_NOT_FOUND,
                                             status=status.HTTP_404_NOT_FOUND,
                                             view=self.get_view_name())
            serialized_data = UsersContentModelSerializer(users_content_list, many=True).data
            response_translator = shared.response_translator(self, serialized_data)
            return shared.basic_response(message=response_translator,
                                         status=status.HTTP_200_OK,
                                         view=self.get_view_name())
    except Exception as ex:
        return shared.main_exception(self.get_view_name(), ex)


def delete_content(self, request):
    try:
        with transaction.atomic():
            request_data = request.data
            if not request_data.get("content_id", None):
                return shared.basic_response(message=error_messages.INVALID_REQUEST,
                                             status=status.HTTP_400_BAD_REQUEST,
                                             view=self.get_view_name())
            UsersContentSerializer.delete(self, request_data)
            return shared.basic_response(message=error_messages.DATA_DELETED_SUCCESSFULLY,
                                         status=status.HTTP_200_OK,
                                         view=self.get_view_name())
    except Exception as ex:
        return shared.main_exception(self.get_view_name(), ex)
