import logging
import requests
from django.conf import settings
from rest_framework.response import Response
from cms import error_messages
from rest_framework import status
from base64 import b64decode
logger = logging.getLogger("cms")


def logger_info(str):
    logger.info(str)


def end_logger_info(view, response):
    logger.info("{} ended....".format(view))
    logger.info(response)
    return True


def basic_response(message, status, view=None):
    end_logger_info(view, message)
    return Response(message, status=status)


def main_exception(view, exception, error_message=None):
    logger.error(exception)
    logger.exception("Exception raised in {} as {}".format(view, str(exception)))
    return Response(error_messages.GENERIC_API_FAILURE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_auth_token(self, username, password):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username': username,
        'password': password
    }
    host = self.request.get_host()
    print(settings.SERVER_PROTOCOLS + host + "/api-token-auth/")
    response = requests.post(settings.SERVER_PROTOCOLS + host + "/api-token-auth/",
                             json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return False


def response_translator(self,data):
    transaltor = {}
    transaltor["success"]=True
    transaltor["data"]=data
    return transaltor


def save_base64(file, path):
    if ";base64," in file:
        path, ext = path.rsplit(".")
        extension, file = file.split(";base64,")
        extension = extension.split("/")[-1]
        path = path + "." + extension
    with open(path, "wb") as f:
        write_status = f.write(b64decode(file))
    return path

def save_file(file: str, path: str):
    """
    Save File in given path
    Accept Base64 data uri and file url.
    """
    path = save_base64(file, path)
    return path
