"""FastAPI application for Integration Service."""  
from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware  
from .api.pipeline import router  
from .config.settings import settings  
  
app = FastAPI(  
    title="NeuroGraph Integration Service",  
    description="Orchestration service for Neural Subgraph Mining pipeline"  
)  
  
# CORS middleware  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
# Include routers  
app.include_router(router)  
  
@app.get("/")  
async def root():  
    return {"message": "NeuroGraph Integration Service API"}  
  
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=9000)