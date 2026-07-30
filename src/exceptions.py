from enum import StrEnum
import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from fastapi import status
from fastapi.responses import JSONResponse

class ExceptionCategory(StrEnum):
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not found"
    CONFLICT = "conflict"
    UNPROCESSABLE = "unprocessable"
    UNAUTHORIZED = "unauthorized"
    BAD_REQUEST = "bad request"
    BLOCKED = "blocked"



class AppError(Exception):
    def __init__(self, detail: str, category: ExceptionCategory):
        super().__init__(detail)
        self.detail = detail
        self.category =  category


class UnauthorizedException(AppError):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail=detail, category=ExceptionCategory.UNAUTHORIZED)

class NotFoundException(AppError):
    def __init__(self, detail: str = "Not found"):
        super().__init__(detail=detail, category=ExceptionCategory.NOT_FOUND)

class ForbiddenException(AppError):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail=detail, category=ExceptionCategory.FORBIDDEN)

class BadRequestException(AppError):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail=detail, category=ExceptionCategory.BAD_REQUEST)

class RequestBlockedException(AppError):
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(detail=detail, category=ExceptionCategory.BLOCKED)

class ConflictException(AppError):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(detail=detail, category=ExceptionCategory.CONFLICT)





logger = logging.getLogger(__name__)


_STATUS_CODE_MAP: dict[ExceptionCategory, int] = {
    ExceptionCategory.FORBIDDEN: status.HTTP_403_FORBIDDEN,
    ExceptionCategory.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    ExceptionCategory.UNPROCESSABLE: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ExceptionCategory.CONFLICT: status.HTTP_409_CONFLICT,
    ExceptionCategory.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ExceptionCategory.BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
    ExceptionCategory.BLOCKED: status.HTTP_429_TOO_MANY_REQUESTS,
}


class ExceptionHanlder(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try: 
            response = await call_next(request)


        except AppError as e:
            response = JSONResponse(
                status_code=_STATUS_CODE_MAP[e.category],
                content={"detail": [{"msg": e.detail}]}
            )

        except Exception as e:
            logger.exception(e)
            response = JSONResponse(
                status_code=500,
                content={"detail": [{"msg": "Unable to process request at this time"}]}
            )
        
        return response