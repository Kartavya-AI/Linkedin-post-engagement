from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.crew.linkedin_crew import LinkedinCrew
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn Automation Crew API",
    description="AI-powered LinkedIn prospecting and engagement automation",
    version="1.0.0"
)

# Initialize CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for structured input
class LinkedInSearchRequest(BaseModel):
    search_query: str

@app.get("/")
async def root():
    return {
        "message": "🔗 Welcome to LinkedIn Automation Crew API!",
        "description": "AI-powered LinkedIn prospecting and engagement automation",
        "version": "1.0.0"
    }

@app.post("/run")
async def run_linkedin_crew(request: LinkedInSearchRequest):
    """
    Run LinkedIn automation crew for prospecting and engagement
    """
    try:
        if not request.search_query.strip():
            raise HTTPException(status_code=400, detail="Search query is required")
        
        # Check if LinkedIn access token is configured
        linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        if not linkedin_token:
            raise HTTPException(
                status_code=500, 
                detail="LinkedIn access token not configured. Please add LINKEDIN_ACCESS_TOKEN to your .env file"
            )
        
        # Create LinkedIn crew instance
        linkedin_crew = LinkedinCrew()
        
        # Prepare inputs for the crew
        inputs = {
            'search_query': request.search_query
        }
        
        # Run the LinkedIn automation crew
        result = linkedin_crew.crew().kickoff(inputs=inputs)
        
        return {
            "status": "success",
            "search_query": request.search_query,
            "automation_steps": [
                "✅ Transformed query into customer-focused search strategies",
                "✅ Discovered relevant LinkedIn prospects",
                "✅ Analyzed prospect content and engagement opportunities",
                "✅ Generated engagement strategy and suggested comments"
            ],
            "result": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LinkedIn automation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)