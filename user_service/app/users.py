import uuid
from typing import Dict, Optional

import jwt
from app.db import User, get_user_db
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import BearerTransport, JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase

SECRET = "SECRET"
KID = "global_key"

# Custom JWT Auth class to add key id to the header for Kong validation
class CustomJWTAuthentication(JWTAuthentication):
    def __init__(
        self,
        secret: str,
        lifetime_seconds: int,
        tokenUrl: str,
        algorithm: str = "HS256",
        kid: Optional[str] = None,
    ):
        super().__init__(secret, lifetime_seconds, tokenUrl, algorithm)
        self.kid = kid

    def _generate_token(self, user_id: str, data: Dict[str, str]) -> str:
        to_encode = data.copy()
        to_encode.update({"sub": str(user_id)})
        header = {"alg": self.algorithm}
        if self.kid:
            header["kid"] = self.kid
        return jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm, headers=header
        )


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = CustomJWTAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login",
    algorithm="HS256",
    kid=KID,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user
