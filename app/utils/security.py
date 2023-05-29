from typing import Optional, Union, Any
from datetime import datetime, timedelta    
from jose import jwt
from core.config.config import settings

def create_access_token(data:dict, expires_delta:Optional[timedelta]=None):
    try:
      
        para_codificar = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        para_codificar.update({'exp':expire})
        codificar_jwt = jwt.encode(para_codificar, settings.SECRET_KEY, algorithm='HS256')
        return codificar_jwt
    except Exception as e:
      print(e)
    
def decode_token(token:str):
   try:
     data = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
     return data
   except Exception as e:
     print(e)