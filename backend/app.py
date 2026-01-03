from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.case_routes import router as case_router
from middleware.error_handler import error_handler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(case_router)
app.add_exception_handler(Exception, error_handler)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)