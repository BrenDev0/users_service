from fastapi import FastAPI
from .routes import router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"detail":[{"msg": "Users service ok"}]}

app.include_router(router)



