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


class RequireTokenException(exc.APIException):
    default_detail = 'Require token.'
    status_code = 400


class WrongUsernameOrPasswordException(exc.APIException):
    default_detail = 'Wrong username or password.'
    status_code = 400


class HomeAddressExists(exc.APIException):
    default_detail = 'Home address exists.'
    status_code = 400


class OfficeAddressExists(exc.APIException):
    default_detail = 'Office address exists.'
    status_code = 400
