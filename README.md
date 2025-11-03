# building-api-gateway-using-fastapi
This repo is for building api gateway and only request routing and simple auth are done here . Though there are more use cases of api gateway. API gateway is  mainly used in case of microservice based architecture where there are several services that have to be handled.

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
```

