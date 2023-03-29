from typing import List
from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import AccountBase, AccountDB, AccountUpdate
from authentication import AuthHandler
router = APIRouter()
auth_handler = AuthHandler()

@router.get("/", response_description="List all accounts")
async def list_all_accounts(
    request: Request,
    min_price: int=0,
    max_price:int=100000,
    rate: float | None = None,
    page:int=1,
    ) -> List[AccountDB]:

    RESULTS_PER_PAGE = 25
    skip = (page-1)*RESULTS_PER_PAGE    
    
    query = {"price":{"$lt":max_price, "$gt":min_price}}
    if rate:
        query["rate"] = rate
    full_query = request.app.mongodb['accounts'].find(query).sort("_id",-1).skip(skip).limit(RESULTS_PER_PAGE)
    results = [AccountDB(**raw_account) async for raw_account in full_query]
    return results

# create new account
@router.post("/", response_description="Add new account")
async def create_account(request: Request, account: AccountBase = Body(...)):
    account = jsonable_encoder(account)
    new_account = await request.app.mongodb["accounts"].insert_one(account)
    created_account = await request.app.mongodb["accounts"].find_one(
        {"_id": new_account.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_account)

# get account by ID
@router.get("/{id}", response_description="Get a single account")
async def show_account(id: str, request: Request):
    if (account := await request.app.mongodb["accounts"].find_one({"_id": id})) is not None:
        return AccountDB(**account)
    raise HTTPException(status_code=404, detail=f"Account with {id} not found")

@router.patch("/{id}", response_description="Update account")
async def update_task(id: str, request: Request, account: AccountUpdate = Body(...)):
    await request.app.mongodb['accounts'].update_one(
        {"_id": id}, {"$set": account.dict(exclude_unset=True)}
    )
    if (account := await request.app.mongodb['accounts'].find_one({"_id": id})) is not None:
        return AccountDB(**account)
    raise HTTPException(status_code=404, detail=f"Account with {id} not found")

@router.delete("/{id}", response_description="Delete account")
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb['accounts'].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    raise HTTPException(status_code=404, detail=f"Account with {id} not found")
