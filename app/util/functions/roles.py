from fastapi import Depends, HTTPException, status
from app.util.functions.auth import AuthContext, operator_auth
from app.core.config import settings

operator_auth_application_id = settings.zitadel_operator_client_id
explorer_auth_application_id = settings.zitadel_explorer_client_id
user_auth_application_id = settings.internal_service_client_id


# Utility to check client_id for role

def require_operator(current_auth: AuthContext = Depends(operator_auth)):
    if current_auth.client_id != operator_auth_application_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: operator role required."
        )
    return current_auth

def require_explorer(current_auth: AuthContext = Depends(operator_auth)):
    if current_auth.client_id != explorer_auth_application_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: explorer role required."
        )
    return current_auth

def require_user(current_auth: AuthContext = Depends(operator_auth)):
    if current_auth.client_id != user_auth_application_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user role required."
        )
    return current_auth
