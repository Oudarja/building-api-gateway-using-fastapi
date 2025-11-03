from fastapi import FastAPI
from middleware import register_midddleware
app = FastAPI()
register_midddleware(app)

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    return {"order_id": order_id, "item": "Laptop"}
