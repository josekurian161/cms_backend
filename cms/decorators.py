from cms import error_messages
from cms.models import CmsUsersMaster
from rest_framework.response import Response
from rest_framework import status

def auth_cms_user(func):
    def wrapper_auth_user(*args, **kwargs):
        try:
            kwargs = {}
            print(args[1].user.username)
            cms_user_obj = CmsUsersMaster.objects.get(
                email_id=args[1].user.username
            )
        except Exception as ex:
            return Response(error_messages.USER_IS_NOT_REGISTERED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        args[1].data["user"] = cms_user_obj
        args[1].data["role_type"]  = cms_user_obj.role_type
        return func(*args, **kwargs)

    return wrapper_auth_user
