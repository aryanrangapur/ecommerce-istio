from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx  # For internal calls
import random

app = FastAPI(title="Order Service")

INVENTORY_URL = "http://inventory-service.ecommerce.svc.cluster.local/api/v1/inventory"
PAYMENT_URL = "http://payment-service.ecommerce.svc.cluster.local/api/v1/payments/charge"

class OrderRequest(BaseModel):
    productId: str
    quantity: int
    userId: str

class OrderResponse(BaseModel):
    orderId: str
    status: str
    total: float
@app.post("/api/v1/orders", response_model=OrderResponse)
async def create_order(req: OrderRequest):
    prices = {"prod-123": 99.99, "prod-456": 199.99}
    total = prices.get(req.productId, 0) * req.quantity

    async with httpx.AsyncClient() as client:
        # Reserve inventory
        res_reserve = await client.post(
            f"{INVENTORY_URL}/reserve",
            json={"productId": req.productId, "quantity": req.quantity}
        )
        if res_reserve.status_code != 200:
            raise HTTPException(status_code=400, detail="Reservation failed")

        res_id = res_reserve.json()["reservationId"]

        # Process payment
        res_payment = await client.post(
            PAYMENT_URL,
            json={"orderId": "ord-temp", "amount": total, "userId": req.userId}
        )
        if res_payment.status_code != 200:
            await client.post(
                f"{INVENTORY_URL}/commit",
                json={"reservationId": res_id, "commit": False}
            )
            raise HTTPException(status_code=402, detail="Payment failed")

        # Commit inventory
        await client.post(
            f"{INVENTORY_URL}/commit",
            json={"reservationId": res_id, "commit": True}
        )

    order_id = f"ord-{random.randint(1000, 9999)}"
    return {"orderId": order_id, "status": "completed", "total": total}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
