INVALID_REQUEST = {
    'status': False,
    'data': {
        'message': 'Invalid Request'
    }
}
SOMETHING_WENT_WRONG = {
    'status': False,
    'data': {
        'message': 'Something went wrong.'
    }
}
USER_REGISTERED_SUCCESSFULLY = {
    'status': True,
    'data': {
        'message': 'User registered successfully.',
        'status_code': 15
    }
}
GENERIC_API_FAILURE = {
    "success": False,
    "data": {
        "msg": "We are unable to process your request at this moment. Please try after sometime.",
        "error_code": 67
    }
}
USER_ALREADY_EXIST = {
    'status': False,
    'data': {
        'message': 'User already exist.'
    }
}
USER_IS_NOT_REGISTERED = {
    'status': False,
    'data': {
        'message': 'User is not registered.'
    }
}

PASSWORD_IS_INCORRECT = {
    'status': False,
    'data': {
        'message': 'password is incorrect'
    }
}

DATA_SAVED_SUCCESSFULLY = {
    'status': True,
    'data': {
        'message': 'data saved successfully'
    }
}
DATA_UPDATED_SUCCESSFULLY = {
    'status': True,
    'data': {
        'message': 'data updated successfully'
    }
}
DATA_DELETED_SUCCESSFULLY = {
    'status': True,
    'data': {
        'message': 'data deleted successfully'
    }
}

DATA_NOT_FOUND = {
    'status': False,
    'data': {
        'message': 'data not found'
    }
}
