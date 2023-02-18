from rest_framework import exceptions as exc


class NicknameDuplicated(exc.APIException):
    default_detail = 'Nickname duplicated.'
    status_code = 409


class UserHasNoAddress(exc.APIException):
    default_detail = 'User does not have address info.'
    status_code = 400


class KakaoApiException(exc.APIException):
    default_detail = 'Kakao api error.'
    status_code = 400
