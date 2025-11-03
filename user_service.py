from fastapi import FastAPI
from middleware import register_midddleware
app = FastAPI()

register_midddleware(app)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}
