from pydantic import BaseModel, ValidationError, EmailStr, PositiveInt, validator
from typing import Optional
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = ["HS256"]
SECRET_KEY = 'django-insecure-xu6bs^jfjm+ok(36#+(6&$^6#m@pj6b))=or0^0-ip$dk)3n&0'


class UserOutPydantic(BaseModel):
    email: EmailStr
    user_handle: str
    user_id: PositiveInt

    # Won't be using any user model in this service
    # class Config:
    #     orm_mode = True

async def get_current_user_util(token: str=Depends(oauth2_scheme)):
    user = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = UserOutPydantic(**payload)
    except:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Invalid Token",
        )
    return user