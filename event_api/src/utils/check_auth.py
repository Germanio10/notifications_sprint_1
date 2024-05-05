import random

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError
from fastapi import HTTPException
from models.user import User
from starlette import status


class CheckAuth(AuthJWT):
    async def __call__(
        self,
    ) -> User:
        try:
            await self.jwt_required()
            user_id = await self.get_jwt_subject()
            role_id = (await self.get_raw_jwt())["role_id"]
            return User(user_id=user_id, role_id=role_id)

        except MissingTokenError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not authorized",
            )

        except JWTDecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid",
            )
