
from fastapi import FastAPI, Request, HTTPException

GATEWAY_SECRET = "secret002oUdaRJA"

# This middleware is for giving restricition to each service (orders and users)
def register_midddleware(app):
    @app.middleware("http")
    async def check_gateway_secret(request: Request, call_next):
        secret = request.headers.get("x-api-key")
        if secret != GATEWAY_SECRET:
            raise HTTPException(status_code=403, detail="Forbidden: Only API Gateway allowed")
        return await call_next(request)