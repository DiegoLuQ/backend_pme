from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from utils.security import create_access_token
from utils.utils import OAuth2PasswordBearerWithCookie
from core.config.config import settings
from core.db.repo_user import buscar_usuario_x_correo, buscar_usuarios
from utils.hash import verify_password
from jose import jwt, JWTError
from core.schemas.Schema_user import ShowLogin

router = APIRouter()


def authenticate_user(correo: str, password: str):
    user = buscar_usuario_x_correo(correo)
    pass_hash = user['contraseña']
    if not user:
        return False
    if not verify_password(password, pass_hash):
        return False

    return user


oatuh2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login/auth")


def get_current_user_from_token(token: str = Depends(oatuh2_scheme)):
    #creamos un Custom Exception
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials")
    # credential_exception = JSONResponse(content={"mensaje": "Token de autenticación expirado"}, status_code=401)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
    except JWTError:
        print('error')
        raise credential_exception

    user = buscar_usuario_x_correo(correo=username)
    if user is None:
        raise credential_exception
    user.pop('contraseña')
    return user


def token_decode_frontend(token: str = Depends(oatuh2_scheme)):
    #creamos un Custom Exception
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials")
    # credential_exception = JSONResponse(content={"mensaje": "Token de autenticación expirado"}, status_code=401)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except JWTError:
        print('error')
        raise credential_exception


def get_current(
        current_user: ShowLogin = Depends(get_current_user_from_token)):
    return current_user


# @router.post('/login')
# def login(response:Response, form_data:OAuth2PasswordRequestForm = Depends()):

#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub":user["correo"], "admin":user["is_superuser"]},  expires_delta=access_token_expire)
#     response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#     return {"access_token":access_token, "token_type": "bearer"}
#JSONResponse(status_code=404, content={"msg":"Usuario y/o Correo no son correctos"})


@router.post('/auth')
def authenticate(loginitem: ShowLogin):
    data = jsonable_encoder(loginitem)

    user = authenticate_user(data['username'], data['password'])
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={
        "sub": user["correo"],
        "admin": user["is_superuser"], 
        "usuario": user["nombre"] + ' ' + user["apellido"],
        "id_colegio": user["id_colegio"]
    },
                                       expires_delta=access_token_expire)
    return {
        "access_token":
        access_token,
        "token_type":
        "bearer",
        "payload":
        jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    }


@router.get('/')
def get_usuarios(current_user=Depends(get_current_user_from_token)):
    data = buscar_usuarios()
    return data


@router.get('/perfil')
def get_decode_token(token: str):
    payload = token_decode_frontend(token)

    return payload
