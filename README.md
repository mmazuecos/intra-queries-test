# Simple private vs public service example

This example shows how to leave private services from within NGINX.

The idea is to leave app1 private to the docker network, and make app2 public to the world.

## Architecture
```
.
├── Docker
│   ├── Dockerfile.service01
│   └── Dockerfile.service02
├── docker-compose.yml
├── nginx.conf
├── README.md
├── requirements.txt
├── service01
│   ├── main.py
│   └── __pycache__
└── service02
    ├── main.py
    └── __pycache__
```

App1 runs the following on POST:
```
# This is the method that service2 will call
@router.post("/samplepost")
def post_sample(input: Input):
    """
    Recieves a number and returns its square
    """
    return {"result": input.number ** 2}
```

while App2 runs the following on POST:
```
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
```

where `global_config.post_requester.post_data` is a method that makes a POST request to the endpoint of App1.

## How to run
```
docker-compose up --build
```

From Postman or curl make the following requests:
```
curl --location --request POST 'http://localhost/api/service2/samplepost' \
--header 'Content-Type: application/json' \
--data-raw '{
    "number": 2
}'
```

If everything works fine, you should get the following response:
```
{
    "result": 16
}
```