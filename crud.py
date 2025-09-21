from sqlalchemy.orm import Session
from models import User, Project, Prompt, Message, File
from auth import hash_password
from typing import List, Optional

# User CRUD operations
def create_user(db: Session, email: str, password: str) -> User:
    """Create a new user"""
    hashed_password = hash_password(password)
    db_user = User(email=email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

# Project CRUD operations
def create_project(db: Session, name: str, user_id: int) -> Project:
    """Create a new project"""
    db_project = Project(name=name, user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects_by_user(db: Session, user_id: int) -> List[Project]:
    """Get all projects for a user"""
    return db.query(Project).filter(Project.user_id == user_id).all()

def get_project_by_id(db: Session, project_id: int, user_id: int) -> Optional[Project]:
    """Get a specific project by ID (ensuring user ownership)"""
    return db.query(Project).filter(
        Project.id == project_id, 
        Project.user_id == user_id
    ).first()

def update_project(db: Session, project_id: int, user_id: int, name: str) -> Optional[Project]:
    """Update a project"""
    project = get_project_by_id(db, project_id, user_id)
    if project:
        project.name = name
        db.commit()
        db.refresh(project)
    return project

def delete_project(db: Session, project_id: int, user_id: int) -> bool:
    """Delete a project"""
    project = get_project_by_id(db, project_id, user_id)
    if project:
        db.delete(project)
        db.commit()
        return True
    return False

# Prompt CRUD operations
def create_prompt(db: Session, text: str, project_id: int) -> Prompt:
    """Create a new prompt"""
    db_prompt = Prompt(text=text, project_id=project_id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompts_by_project(db: Session, project_id: int) -> List[Prompt]:
    """Get all prompts for a project"""
    return db.query(Prompt).filter(Prompt.project_id == project_id).all()

def get_prompt_by_id(db: Session, prompt_id: int) -> Optional[Prompt]:
    """Get a specific prompt by ID"""
    return db.query(Prompt).filter(Prompt.id == prompt_id).first()

def update_prompt(db: Session, prompt_id: int, text: str) -> Optional[Prompt]:
    """Update a prompt"""
    prompt = get_prompt_by_id(db, prompt_id)
    if prompt:
        prompt.text = text
        db.commit()
        db.refresh(prompt)
    return prompt

def delete_prompt(db: Session, prompt_id: int) -> bool:
    """Delete a prompt"""
    prompt = get_prompt_by_id(db, prompt_id)
    if prompt:
        db.delete(prompt)
        db.commit()
        return True
    return False

# Message CRUD operations
def create_message(db: Session, role: str, content: str, project_id: int) -> Message:
    """Create a new message"""
    db_message = Message(role=role, content=content, project_id=project_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_project(db: Session, project_id: int, limit: int = 50) -> List[Message]:
    """Get messages for a project (most recent first)"""
    return db.query(Message).filter(
        Message.project_id == project_id
    ).order_by(Message.timestamp.desc()).limit(limit).all()

# File CRUD operations
def create_file(db: Session, filename: str, file_path: str, project_id: int, 
                file_size: int = None, content_type: str = None) -> File:
    """Create a new file record"""
    db_file = File(
        filename=filename,
        file_path=file_path,
        project_id=project_id,
        file_size=file_size,
        content_type=content_type
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_files_by_project(db: Session, project_id: int) -> List[File]:
    """Get all files for a project"""
    return db.query(File).filter(File.project_id == project_id).all()

def get_file_by_id(db: Session, file_id: int) -> Optional[File]:
    """Get a specific file by ID"""
    return db.query(File).filter(File.id == file_id).first()

def delete_file(db: Session, file_id: int) -> bool:
    """Delete a file record"""
    file = get_file_by_id(db, file_id)
    if file:
        db.delete(file)
        db.commit()
        return True
    return False
