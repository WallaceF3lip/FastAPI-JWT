from fastapi import FastAPI

from core.configs import Settings
from api.V1.api import api_router

app = FastAPI(title="FastAPI JWT - Exemplo")
app.include_router(api_router, prefix=Settings().API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")


"""
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzY4MTg4ODUxLCJpYXQiOjE3Njc1ODQwNTEsInN1YiI6IjEifQ.DsQYcxBVdCuzNbK-XerIze9Wgik8gY6_-wlSfsuoLWk",
"token_type": "bearer"
"""