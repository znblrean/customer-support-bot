import sys
print(sys.path)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Customer Support Bot API is running"}