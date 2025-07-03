from fastapi import FastAPI

from test_endpoints import router as test_endpoint
from html_pages import router as html_pages
from forms import router as forms
from elements import router as elements
from auth import router as auth


app = FastAPI()

app.include_router(html_pages)
app.include_router(auth)
app.include_router(forms)
app.include_router(elements)
app.include_router(test_endpoint)