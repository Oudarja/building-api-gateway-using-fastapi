from fastapi import FastAPI, Request, HTTPException, Security, status, Depends
from fastapi.security.api_key import APIKeyHeader
import httpx

app = FastAPI(title="Simple demo API gateway")

# Mapping service name to backend
Backends = {
    "users": "http://localhost:8001",
    "orders": "http://localhost:8002"
}

# For simple authentication purpose API keys
API_KEYS = ["secret002oUdaRJA"]

# Define API Key header for FastAPI docs
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


# Dependency to validate API key
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

# Catch-all API route for proxying requests
@app.api_route("/{service}/{path:path}", methods=["GET", "POST"])
async def gateway(service: str, path: str, request: Request, api_key: str = Depends(get_api_key)):
    if service not in Backends:
        raise HTTPException(status_code=404, detail="Service not found")

    backend_url = f"{Backends[service]}/{service}/{path}"

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=backend_url,
            headers=request.headers.raw,
            content=await request.body()
        )
    return resp.json()
