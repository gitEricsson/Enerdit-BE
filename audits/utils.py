from rest_framework.exceptions import APIException

class AppError(APIException):
    def __init__(self, detail, status_code):
        self.status_code = status_code
        super().__init__(detail)