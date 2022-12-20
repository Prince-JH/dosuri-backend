from rest_framework import exceptions as exc


class NicknameDuplicated(exc.APIException):
    default_detail = 'Nickname duplicated.'
    status_code = 409
    