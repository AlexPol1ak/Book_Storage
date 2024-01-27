from fastapi import Depends, HTTPException
from starlette import status

from user.auth_config import current_user


async def is_admin_user(auth_user=Depends(current_user)):
    """
    Dependency, checks if the authorized user is an administrator.
    And returns admin. Or raises an HTTPException exception.
    """
    if hasattr(auth_user, 'is_admin') and auth_user.is_admin is True:
        return auth_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not enough authority.")


async def is_superuser(auth_user=Depends(current_user)):
    """
    Dependency, checks if the authorized user is a superuser.
    And returns superuser. Or raises an HTTPException exception.
    """

    if hasattr(auth_user, 'is_superuser') and auth_user.is_superuser is True:
        return auth_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not enough authority.")


async def is_superuser_or_admin(auth_user=Depends(current_user)):
    """
    Dependency, checks if the authorized user is a superuser or admin.
    And returns superuser or admin. Or raises an HTTPException exception.
    """
    if ((hasattr(auth_user, 'is_superuser') and auth_user.is_superuser is True)
            or (hasattr(auth_user, 'is_admin') and auth_user.is_admin is True)):
        return auth_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not enough authority.")
