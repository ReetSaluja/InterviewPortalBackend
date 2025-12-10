from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # <-- ADD THIS LINE
from db.database import Base, engine
from routers.candidate_router import router as candidate_router
from routers.auth_router import router as auth_router
from routers.interviewer_router import router as interviewer_router
# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Interview Backend",
    version="1.0.0",
)

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(candidate_router)
app.include_router(interviewer_router)

@app.get("/")
def root():
    return {
        "message": "Interview Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "candidates": {
                "create": "POST /candidates/",
                "get_all": "GET /candidates/",
                "update": "PUT /candidates/{candidate_id}"
            }
        }
    }