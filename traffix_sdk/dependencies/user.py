from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from loguru import logger
from traffix_sdk.dependencies.fastapi import DatabaseDep, ApiKeyDep
from traffix_sdk.models import TraffixAPIUser
from traffix_sdk.database.async_drivers import sqlmodel as crud


async def get_user_from_apikey(
    db: DatabaseDep, api_key: ApiKeyDep
) -> TraffixAPIUser | None:
    """Returns a User based on a valid API Key"""
    if not api_key:
        return None

    existing_api_key = await crud.traffix_api_key.get_by_api_key(db=db, api_key=api_key)
    if not existing_api_key or not existing_api_key.user:
        return None

    return existing_api_key.user


async def get_user_from_cookie() -> None:
    """Returns a User based on a valid Cookie"""
    pass


async def get_user_from_jwt() -> None:
    """Returns a User based on a valid JWT"""
    pass


def get_user(
    user_from_apikey: TraffixAPIUser = Depends(get_user_from_apikey),
    user_from_cookie: TraffixAPIUser = Depends(get_user_from_cookie),
    user_from_jwt: TraffixAPIUser = Depends(get_user_from_jwt),
) -> TraffixAPIUser | None:
    """Returns a user if found in the database"""
    if not user_from_apikey and not user_from_cookie and not user_from_jwt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if user_from_apikey:
        logger.debug(f"auth: User {user_from_apikey.id} authenticated using API Key")
        return user_from_apikey
    elif user_from_cookie:
        logger.debug(f"auth: User {user_from_cookie.id} authenticated using Cookie")
        return user_from_cookie
    elif user_from_jwt:
        logger.debug(f"auth: User {user_from_jwt.id} authenticated using JWT")
        return user_from_jwt


def get_active_user(user: TraffixAPIUser = Depends(get_user)) -> TraffixAPIUser | None:
    """Returns the user if its active otherwise throw a HTTP 401 unauthorized"""
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


def get_active_superuser(
    user: TraffixAPIUser = Depends(get_active_user),
) -> TraffixAPIUser | None:
    """Returns the user if its active and is a superuser otherwise throw a HTTP 403 forbidden"""
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return user
