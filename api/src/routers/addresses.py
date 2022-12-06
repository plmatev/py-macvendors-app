from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import (
    ExecutionTimeout,
    OperationFailure,
    NetworkTimeout,
    ServerSelectionTimeoutError,
)

from helpers.mac_parser import mac_to_int
from models.mac_block_models import mac_block_helper, company_block_helper

import os


load_dotenv()

mongo_user = os.getenv("mongo_user")
mongo_pass = os.getenv("mongo_pass")

MONGODB_URL = f"mongodb://{mongo_user}:{mongo_pass}@mongodb:27017/"

client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
database = client.MacAddrRange
db_collection_mac_addresses_mas = database.MA_S
db_collection_mac_addresses_mam = database.MA_M
db_collection_mac_addresses_mal = database.MA_L

router = APIRouter()


@router.get(
    "/oui/{mac_address}",
    responses={
        400: {"content": {"application/json": {"example": {"detail": "string"}}}},
        404: {"content": {"application/json": {"example": {"detail": "string"}}}},
        503: {
            "content": {"application/json": {"example": {"detail": "string"}}},
            "headers": {
                "Retry-After": {
                    "description": "Returned with HTTP status code 503 (Service Unavailable)",
                    "type": "string",
                }
            },
        },
    },
    name="Get OUI assignment by Specific MAC Address",
)
async def get_single_mac_oui(mac_address: str):
    mac_raw, mac_int = mac_to_int(mac_address)

    if not mac_raw:
        raise HTTPException(
            status_code=400, detail="Invalid or unsupported MAC address format"
        )

    for db_collection in (
        db_collection_mac_addresses_mas,
        db_collection_mac_addresses_mam,
        db_collection_mac_addresses_mal,
    ):

        try:
            mac_block = await db_collection.find_one(
                {
                    "mac_b10_l": {"$lte": mac_int},
                    "mac_b10_h": {"$gte": mac_int},
                }
            )

            if mac_block:
                return JSONResponse(content=mac_block_helper(mac_block))

        except (
            ExecutionTimeout,
            OperationFailure,
            NetworkTimeout,
            ServerSelectionTimeoutError,
        ):
            raise HTTPException(
                status_code=503,
                detail="Error connecting to database",
                headers={"Retry-After": "120"},
            )

    raise HTTPException(status_code=404, detail="MAC Block/Vendor not found")


@router.get(
    "/vendorname/{mac_address}",
    responses={
        400: {"content": {"application/json": {"example": {"detail": "string"}}}},
        404: {"content": {"application/json": {"example": {"detail": "string"}}}},
        503: {
            "content": {"application/json": {"example": {"detail": "string"}}},
            "headers": {
                "Retry-After": {
                    "description": "Returned with HTTP status code 503 (Service Unavailable)",
                    "type": "string",
                }
            },
        },
    },
    name="Get Vendor name by Specific MAC Address",
)
async def get_single_mac_vendor(mac_address: str):
    mac_raw, mac_int = mac_to_int(mac_address)

    if not mac_raw:
        raise HTTPException(
            status_code=400, detail="Invalid or unsupported MAC address format"
        )

    for db_collection in (
        db_collection_mac_addresses_mas,
        db_collection_mac_addresses_mam,
        db_collection_mac_addresses_mal,
    ):

        try:
            mac_block = await db_collection.find_one(
                {
                    "mac_b10_l": {"$lte": mac_int},
                    "mac_b10_h": {"$gte": mac_int},
                },
                {"_id": 0, "company": 1},
            )

            if mac_block:
                return HTMLResponse(content=mac_block["company"])

        except (
            ExecutionTimeout,
            OperationFailure,
            NetworkTimeout,
            ServerSelectionTimeoutError,
        ):
            raise HTTPException(
                status_code=503,
                detail="Error connecting to database",
                headers={"Retry-After": "120"},
            )

    raise HTTPException(status_code=404, detail="MAC Vendor not found")


@router.get(
    "/company/{company_name}",
    responses={
        404: {"content": {"application/json": {"example": {"detail": "string"}}}},
        503: {
            "content": {"application/json": {"example": {"detail": "string"}}},
            "headers": {
                "Retry-After": {
                    "description": "Returned with HTTP status code 503 (Service Unavailable)",
                    "type": "string",
                }
            },
        },
    },
    name="Get Vendor assigned OUI blocks by Company Name",
)
async def get_oui_block_by_company(company_name: str):
    result = []

    for db_collection in (
        db_collection_mac_addresses_mas,
        db_collection_mac_addresses_mam,
        db_collection_mac_addresses_mal,
    ):

        try:
            async for res in db_collection.find(
                {"company": {"$regex": f"^{company_name}.*", "$options": "i"}},
                {"_id": 0, "company": 1, "mac_b16_l": 1, "mac_b16_h": 1},
            ):

                result.append(company_block_helper(res))

        except (
            ExecutionTimeout,
            OperationFailure,
            NetworkTimeout,
            ServerSelectionTimeoutError,
        ):
            raise HTTPException(
                status_code=503,
                detail="Error connecting to database",
                headers={"Retry-After": "120"},
            )

    if result:
        return JSONResponse(content=result)

    raise HTTPException(status_code=404, detail="MAC Vendor not found")
