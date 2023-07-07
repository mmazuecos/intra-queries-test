from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel


# FastAPI app and router
app = FastAPI()
router = APIRouter(prefix="/api/service1")


# Input model
class Input(BaseModel):
    number: int


# Sample GET and POST methods
@router.get("/sampleget")
def get_sample():
    return {"message": "This is a sample GET method in service1"}


# This is the method that service2 will call
@router.post("/samplepost")
def post_sample(input: Input):
    """
    Recieves a number and returns its square
    """
    return {"result": input.number ** 2}

# Include the router
app.include_router(router)
