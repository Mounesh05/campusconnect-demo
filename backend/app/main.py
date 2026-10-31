from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routes import events, registrations, attendance

app = FastAPI(title="CampusConnect Lite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(events.router, prefix="/api")
app.include_router(registrations.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "CampusConnect Lite API is running"}