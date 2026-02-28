from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader

API_KEY = "test-api-key-123"

api_key_header = APIKeyHeader(
    name="X-API-Key",
    description="Статический API ключ",
    auto_error=False,
)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing",
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return api_key