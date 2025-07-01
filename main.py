from fastapi import FastAPI

from test_endpoints import router as test_endpoint


app = FastAPI()

app.include_router(router=test_endpoint)
