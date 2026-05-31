from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Hola": "Mundo!"}

@app.get("/health")
def health():
    return {"status": "ok"}