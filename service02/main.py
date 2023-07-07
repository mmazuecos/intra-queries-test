from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel
import requests


class PostRequester:
    def __init__(self, endpoint):
        self.endpoint = endpoint
 
    def post_data(self, number):
        data = {'number': number}  # Assuming the endpoint expects a 'number' parameter
 
        try:
            response = requests.post(self.endpoint, json=data)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


class Input(BaseModel):
    number: int


# A global config to make the requester available to the router
class GlobalConfig:
    def __init__(self):
        # service1_endpoint cosists of the following:
        # - http://: the protocol
        # - service01: the name of the docker container running the app1
        # - :3000: the port on which the app1 is running
        # - /api/service1/samplepost: the endpoint of the app1
        # TODO find a way to not hardcode this the endpoint 
        self.service1_endpoint = "http://service01:3000/api/service1/samplepost"
        self.post_requester = PostRequester(self.service1_endpoint)


app = FastAPI()
router = APIRouter(prefix="/api/service2")
global_config = GlobalConfig()


# Sample GET
@router.get("/sampleget")
def get_sample():
    return {"message": "This is a sample GET method in service2"}


# Sample POST
@router.post("/samplepost")
def post_sample(input: Input):
    """
    Asks the endpoint of service1 to square the input number
    and then squares the result
    """
    # Request the endpoint of app1
    res = global_config.post_requester.post_data(input.number)
    if res is None:
        return {"message": "An error occurred"}
    return {"result": res['result'] ** 2}

app.include_router(router)
