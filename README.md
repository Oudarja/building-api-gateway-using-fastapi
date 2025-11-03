# building-api-gateway-using-fastapi
This project demonstrates a secure API Gateway built using FastAPI that routes requests to multiple backend microservices. Only the API Gateway can access the backend services directly, enforcing internal security using a gateway secret. End users access services via the API Gateway using an API key. Here only request routing and simple auth are done here . Though there are more use cases of api gateway. API gateway is  mainly used in case of microservice based architecture where there are several services that have to be handled.

# Backend services:
- User Service → Handles users
- Order Service → Handles orders
Instead of calling them separately, the client calls the API Gateway, which decides where to forward the request.

```
      Client
        |
        v
-------------------
|  API   Gateway  |
-------------------
   |          |
   v          v
User Service  Order Service

Client --> API Gateway (Port 8000) --> Backend Services (Ports 8001, 8002)

```

## API Gateway
- Receives requests from clients.
- Validates the client API key (x-api-key).
- Forwards requests to the correct backend service.
- Adds a gateway secret (x-api-key) to communicate with backends securely.

## Backend Services
- User Service (8001)
  Handles /users/{user_id} endpoints.
- Order Service (8002)
  Handles /orders/{order_id} endpoints.
- Both services are protected with middleware, allowing only requests containing the gateway secret.

# Features
- Secure access control
      - Clients must use a valid API key to access any endpoint via the gateway.
      - Direct access to backend services is blocked without the gateway secret.
- Dynamic routing / proxy
      - Gateway dynamically forwards requests to multiple backend services based on the URL path.
- FastAPI docs support
      - Swagger UI (/docs) is available on the API Gateway for testing endpoints with the API key.
  
```
├── api_gateway.py       # Main API Gateway
├── users_service.py     # User backend service
├── order_service.py     # Order backend service
├── middleware.py        # Middleware for gateway secret protection
└── README.md
```

# Setup & Run
## Clone the repo 
```
git clone https://github.com/Oudarja/building-api-gateway-using-fastapi.git
```
## Python version : 
```3.9.13```
## Create environment
```
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```
## Install dependencies
```
pip install fastapi uvicorn httpx
```
## Run backend services
```
# User Service
uvicorn users_service:app --port 8001

# Order Service
uvicorn order_service:app --port 8002

```
## Run API Gateway
```
uvicorn api_gateway:app --port 8000
```
## Access via API Gateway
### Get User:
```
GET http://127.0.0.1:8000/users/1
Headers:
  x-api-key: secret002oUdaRJA
```
### Get Order:
```
GET http://127.0.0.1:8000/orders/1
Headers:
  x-api-key: secret002oUdaRJA
```
FastAPI Swagger UI: ```http://127.0.0.1:8000/docs```
Use the Authorize button to provide the API key.

*** Direct backend access
- Any request to ```http://127.0.0.1:8001``` or ```8002``` without the gateway secret will be blocked (403 Forbidden).
- This ensures only the API Gateway can call backend services.




## Summary
This setup provides a centralized access point for multiple services with internal security. The API Gateway handles authentication, routing, and request forwarding, while backend services are protected from direct access.

# Notes:
- ## httpx
  - httpx is a modern HTTP client library for Python — similar to requests, but with async (asynchronous) support.
  - httpx is a library used to make HTTP requests (GET, POST, PUT, DELETE, etc.) to APIs or web services — just like
    requests, but it works with both sync and async code.
  - it is used when code needs to communicate with another API or service — especially in that situation
      ```
      | Purpose                                    | Library    | Mode                |
      | ------------------------------------------ | ---------- | ------------------- |
      | Simple HTTP calls                          | `requests` | Sync                |
      | Fast, async HTTP calls                     | `httpx`    | Async + Sync        |
      | HTTP/2, connection pooling, better control | `httpx`    | Async/Advanced apps |
      ```
- ## async and await
  - When operations involve external input/output (I/O), such as making API calls, querying a database, or reading and writing files, not using async/await causes the code to pause and wait for the operation to
    complete. During this waiting period, the server’s worker thread is blocked and cannot handle other incoming requests until the current operation finishes. This can significantly slow down the application
    when multiple clients access it simultaneously, as each request may occupy a thread while waiting for I/O. In high-traffic situations, this can lead to long response times and may even exhaust server
    resources.In scenarios where a request involves a network or database call without asynchronous handling, the function stops and waits for the operation to complete. The CPU remains idle during this time, and
    no other request can use that worker thread. If many users make requests concurrently, the server requires a separate thread for each request, consuming substantial resources and reducing scalability.
    By contrast, asynchronous functions (async def) combined with await enable the server to handle these operations in a non-blocking manner. While an asynchronous function waits for an I/O operation, the event
    loop can switch to processing other requests instead of remaining idle. This allows the server to handle many requests concurrently, improving both performance and scalability, particularly in applications
    that make multiple external API calls or interact frequently with databases.
    In summary:
    - Without async → blocking I/O → thread waits → poor scalability.
    - With async → non-blocking I/O → event loop handles multiple requests → high efficiency.
