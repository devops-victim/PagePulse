from fastapi import FastAPI
import uvicorn
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Page Pulse API",
    version="1.0.0",
    description="Audit websites for SEO and accessibility metrics."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)