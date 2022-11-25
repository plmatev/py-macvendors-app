from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.addresses import router as mac_router


tags = [
    {
        "name": "MAC Vendor Lookup",
        "description": "Get details about vendor and IEEE OUI block"
    }
]

app = FastAPI(
    title="MAC Vendor Lookup",
    openapi_tags=tags,
    version="1.0.0",
    contact={
        "name": "Plamen Matev",
        "email": "plmatev@gmail.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mac_router, tags=["IEEE MAC Blocks"], prefix="/api/v1")
