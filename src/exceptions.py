from typing import Any
from fastapi import HTTPException, status

class MyHttpException(HTTPException):
    def __init__(self, status_code: int, detail: Any):
        super().__init__(status_code=status_code, detail=detail)
        
    def get_example(self):
        return {
            "summary": self.__class__.__name__,
            "value": {
                "detail": self.detail
            }
        }
        

class UnsupportedMediaType(MyHttpException):
    def __init__(self, detail: Any):
        super().__init__(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail)

class BadRequest(MyHttpException):
    def __init__(self, detail: Any):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

