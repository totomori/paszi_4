from fastapi import FastAPI
from app.routes.register import router as register_router

app = FastAPI(title="MVP Register Service")

app.include_router(register_router)
