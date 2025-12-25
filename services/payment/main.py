from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="Payment Service")

class ChargeRequest(BaseModel):
    orderId: str
    amount: float
    userId: str

class ChargeResponse(BaseModel):
    transactionId: str
    status: str
    refundable: bool

@app.post("/api/v1/payments/charge", response_model=ChargeResponse)
async def charge(req: ChargeRequest):
    # Mock: 80% success
    if random.random() < 0.2:  # 20% fail
        raise HTTPException(status_code=500, detail="Payment gateway error")
    txn_id = f"txn-{random.randint(1000, 9999)}"
    return {"transactionId": txn_id, "status": "succeeded", "refundable": True}

@app.post("/api/v1/payments/refund")
async def refund(req: ChargeRequest):  # Simplified
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
