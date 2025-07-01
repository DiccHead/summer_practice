from fastapi import FastAPI

from test_endpoints import router as test_endpoint
from html_pages import router as html_pages
from auth import router as auth


app = FastAPI()

app.include_router(router=html_pages)
app.include_router(router=auth)
app.include_router(router=test_endpoint)