import uuid
from fastapi import APIRouter, HTTPException, Body, Depends, Header
from core.schema import Input, Output
from api.core import agent

router = APIRouter()

async def get_user_id(x_user_id: str = Header(...)):
    return x_user_id

@router.post("/start", response_model=Output)
async def start_appointment(
    user_id: str = Depends(get_user_id)
) -> Output:
    thread_id = str(uuid.uuid4())
    try:
        result = await agent.start(thread_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/resume", response_model=Output)
async def continue_appointment(
    user_id: str = Depends(get_user_id), 
    data: Input = Body(...)) -> Output:
    try:
        result = await agent.resume(data.thread_id, data.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


