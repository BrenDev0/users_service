from fastapi import FastAPI
from .routes import router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"detail":[{"msg": "Users service ok"}]}

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

