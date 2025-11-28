from fastapi import FastAPI
from database import Base, engine
from routers.candidate_router import router as candidate_router

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Interview Backend",
    version="1.0.0",
)

# Register router
app.include_router(candidate_router)