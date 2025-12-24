from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(title="Foto Owl API Gateway")

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow frontend access (local dev)
    allow_credentials=True,
    allow_methods=["*"],        # allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "API Gateway running"}
