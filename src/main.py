from fastapi import FastAPI


app = FastAPI()

@app.get("/health")
def health_check():
    return {"detail":[{"msg": "Users service ok"}]}



