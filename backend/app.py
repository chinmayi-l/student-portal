from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import re

app = FastAPI()

# Configure CORS to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str

# Simple AI response generator (can be replaced with real AI API)
def generate_response(user_message: str) -> str:
    """Generate a response based on user input"""
    message_lower = user_message.lower()
    
    # Educational responses based on keywords
    responses = {
        "hello": "Hello! Welcome to the Student AI Assistant. How can I help you with your studies today?",
        "help": "I can help you with:\n• Academic questions\n• Study tips\n• Course information\n• Assignment guidance\n• Time management advice\n\nWhat would you like help with?",
        "math": "I'd be happy to help with math! Please share the specific topic or problem you're working on.",
        "english": "Great! I can help with English. Are you looking for help with grammar, writing, literature, or something else?",
        "science": "Science is fascinating! Which science subject would you like help with? Physics, Chemistry, Biology, or General Science?",
        "study": "Here are some effective study tips:\n• Break topics into smaller chunks\n• Use active recall\n• Take regular breaks (Pomodoro technique)\n• Teach concepts to others\n• Practice problems regularly",
        "assignment": "I'd be happy to help guide you through your assignment. Could you tell me more about what you're working on?",
        "exam": "Preparing for an exam? Here are tips:\n• Review past papers\n• Create summary notes\n• Practice timed questions\n• Get enough sleep\n• Stay confident!",
        "grade": "Want to improve your grades? Focus on:\n• Regular studying\n• Active class participation\n• Asking for help when needed\n• Understanding concepts deeply\n• Consistent practice",
        "motivation": "Remember, every expert was once a beginner! Stay motivated by:\n• Setting achievable goals\n• Celebrating small wins\n• Taking care of your health\n• Finding your purpose\n• Connecting with peers",
    }
    
    # Check for keyword matches
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    # Default response if no keywords match
    return (
        "Thank you for your question! I'm an educational AI assistant designed to help you with your studies. "
        "I can assist with various subjects and study techniques. "
        "For more specific help, try asking about math, science, English, study tips, assignments, or exam preparation. "
        f"You asked: '{user_message}' - Please provide more details for better assistance!"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat: ChatMessage) -> ChatResponse:
    """
    Handle chat messages and return AI-generated responses
    
    Args:
        chat: ChatMessage containing the user's message
        
    Returns:
        ChatResponse with AI response and timestamp
    """
    if not chat.message or not chat.message.strip():
        return ChatResponse(
            response="Please enter a valid message.",
            timestamp=datetime.now().isoformat()
        )
    
    # Generate response
    ai_response = generate_response(chat.message)
    
    return ChatResponse(
        response=ai_response,
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Student Education Portal AI Assistant Backend",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
