from fastapi import HTTPException
from fastapi import Security
from fastapi.security import APIKeyHeader
from starlette import status

from config import SECURITY_KEY

API_KEY = SECURITY_KEY
API_KEY_NAME = "Gourav's Key"

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    print(api_key_header, "\n", API_KEY)
    if api_key_header != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, \
                            detail="Invalid API Key")
    else:
        return

