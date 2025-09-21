from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, File as FastAPIFile, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import httpx
import uuid
from datetime import timedelta

from database import get_db, create_tables
from models import User, Project, Prompt, Message
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    get_current_user_api,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from crud import (
    create_user, get_user_by_email, create_project, get_projects_by_user,
    get_project_by_id, create_prompt, get_prompts_by_project, create_message,
    get_messages_by_project, create_file, get_files_by_project, delete_file
)
from chatbot import ChatBot

# Initialize FastAPI app
app = FastAPI(title="Chatbot Platform", version="1.0.0")

# Create database tables
create_tables()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Create uploads directory
os.makedirs("uploads", exist_ok=True)

# Initialize ChatBot instance
try:
    chatbot = ChatBot(model="x-ai/grok-4-fast:free")
    print("ChatBot initialized successfully with Grok 4")
except ValueError as e:
    print(f"Warning: ChatBot initialization failed: {e}")
    chatbot = None

# LLM API endpoint using OpenRouter
async def call_llm_api(message: str, system_prompt: str = "", project_messages: list = None) -> str:
    """Call OpenRouter API through ChatBot class"""
    if not chatbot:
        return "Error: ChatBot not initialized. Please check your OpenRouter API key configuration."
    
    try:
        # Convert project messages to the format expected by ChatBot
        formatted_messages = []
        if project_messages:
            for msg in project_messages:
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        response = await chatbot.chat_with_context(
            message=message,
            system_prompt=system_prompt,
            project_messages=formatted_messages
        )
        return response
    except Exception as e:
        return f"Error calling OpenRouter API: {str(e)}"

# Authentication routes
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint for JWT token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root page - redirect to login"""
    return RedirectResponse(url="/login")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Chatbot Platform is running"}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle login form submission"""
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid email or password"}
        )
    
    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle registration form submission"""
    # Check if user already exists
    if get_user_by_email(db, email):
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": "Email already registered"}
        )
    
    # Create new user
    user = create_user(db, email, password)
    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.api_route("/logout", methods=["GET", "POST"])
async def logout():
    """Logout endpoint - handles both GET and POST"""
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response

# Dashboard and project routes
@app.api_route("/dashboard", methods=["GET", "POST"], response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """User dashboard - handles both GET and POST"""
    if request.method == "POST":
        # Handle POST requests by redirecting to GET
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        # Preserve the authentication cookie
        token = request.cookies.get("access_token")
        if token:
            response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    
    # Handle GET requests
    projects = get_projects_by_user(db, current_user.id)
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "user": current_user, "projects": projects}
    )

@app.api_route("/projects", methods=["GET", "POST"], response_class=HTMLResponse)
async def projects_handler(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle projects - both listing and creation"""
    if request.method == "POST":
        # Handle project creation
        form_data = await request.form()
        name = form_data.get("name")
        if not name:
            raise HTTPException(status_code=400, detail="Project name is required")
        
        project = create_project(db, name, current_user.id)
        response = RedirectResponse(url=f"/projects/{project.id}", status_code=status.HTTP_303_SEE_OTHER)
        # Preserve the authentication cookie
        token = request.cookies.get("access_token")
        if token:
            response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    
    # Handle GET requests - list projects
    projects = get_projects_by_user(db, current_user.id)
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "user": current_user, "projects": projects}
    )

@app.api_route("/projects/{project_id}", methods=["GET", "POST"], response_class=HTMLResponse)
async def project_page(
    request: Request,
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Project page with chat interface - handles both GET and POST"""
    if request.method == "POST":
        # Handle POST requests by redirecting to GET
        response = RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)
        # Preserve the authentication cookie
        token = request.cookies.get("access_token")
        if token:
            response.set_cookie(key="access_token", value=token, httponly=True)
        return response
    
    # Handle GET requests
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    prompts = get_prompts_by_project(db, project_id)
    messages = get_messages_by_project(db, project_id)
    files = get_files_by_project(db, project_id)
    
    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project": project,
            "prompts": prompts,
            "messages": messages,
            "files": files
        }
    )

@app.post("/projects/{project_id}/prompts")
async def create_prompt_endpoint(
    request: Request,
    project_id: int,
    text: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new prompt for a project"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    prompt = create_prompt(db, text, project_id)
    response = RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)
    # Preserve the authentication cookie
    token = request.cookies.get("access_token")
    if token:
        response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@app.get("/projects/{project_id}/prompts")
async def get_prompts_endpoint(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prompts for a project"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    prompts = get_prompts_by_project(db, project_id)
    return {"prompts": [{"id": p.id, "text": p.text, "created_at": p.created_at} for p in prompts]}

@app.post("/projects/{project_id}/chat")
async def chat_endpoint(
    request: Request,
    project_id: int,
    message: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle chat messages"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Save user message
    user_message = create_message(db, "user", message, project_id)
    
    # Get system prompt (if any)
    prompts = get_prompts_by_project(db, project_id)
    system_prompt = prompts[0].text if prompts else ""
    
    # Get previous messages for context
    previous_messages = get_messages_by_project(db, project_id)
    
    # Call LLM API with context
    try:
        response_text = await call_llm_api(message, system_prompt, previous_messages)
    except Exception as e:
        response_text = f"Error calling LLM API: {str(e)}"
    
    # Save assistant response
    assistant_message = create_message(db, "assistant", response_text, project_id)
    
    response = RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)
    # Preserve the authentication cookie
    token = request.cookies.get("access_token")
    if token:
        response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@app.get("/projects/{project_id}/chat")
async def get_chat_messages(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat messages for a project"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    messages = get_messages_by_project(db, project_id)
    return {"messages": [{"role": msg.role, "content": msg.content, "timestamp": msg.timestamp} for msg in messages]}

@app.post("/projects/{project_id}/upload")
async def upload_file(
    request: Request,
    project_id: int,
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file to a project"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join("uploads", unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Save file record to database
    file_record = create_file(
        db=db,
        filename=file.filename,
        file_path=file_path,
        project_id=project_id,
        file_size=len(content),
        content_type=file.content_type
    )
    
    response = RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)
    # Preserve the authentication cookie
    token = request.cookies.get("access_token")
    if token:
        response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@app.get("/projects/{project_id}/files")
async def get_project_files(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get files for a project"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    files = get_files_by_project(db, project_id)
    return {"files": [{"id": f.id, "filename": f.filename, "file_size": f.file_size, "uploaded_at": f.uploaded_at} for f in files]}

@app.get("/files/{file_id}")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a file"""
    from crud import get_file_by_id
    file_record = get_file_by_id(db, file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if user has access to the project
    project = get_project_by_id(db, file_record.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_record.file_path,
        filename=file_record.filename,
        media_type=file_record.content_type
    )

# API endpoints for AJAX
@app.get("/api/projects/{project_id}/messages")
async def get_messages_api(
    project_id: int,
    current_user: User = Depends(get_current_user_api),
    db: Session = Depends(get_db)
):
    """Get messages for a project (API endpoint)"""
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    messages = get_messages_by_project(db, project_id)
    return [{"role": msg.role, "content": msg.content, "timestamp": msg.timestamp} for msg in messages]

# Note: Removed catch-all route to prevent conflicts with defined routes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
