# File Architecture Documentation

This document provides a comprehensive overview of the file structure and architecture of the Chatbot Platform.

## Project Overview

The Chatbot Platform is a FastAPI-based web application that provides AI-powered chatbot functionality using OpenRouter's Grok 4 model. The platform supports user authentication, project management, and real-time chat interactions.

## Root Directory Structure

```
/Users/sruthigeorge/code_base/
├── main.py                    # FastAPI application entry point
├── models.py                  # SQLAlchemy ORM models
├── auth.py                    # Authentication utilities (JWT, bcrypt)
├── crud.py                    # Database CRUD operations
├── database.py                # Database configuration
├── chatbot.py                 # OpenRouter ChatBot integration class
├── config.py                  # Configuration management
├── start_server.py            # Production startup script
├── requirements.txt           # Python dependencies
├── railway.json               # Railway deployment configuration
├── Procfile                   # Process definition for Railway
├── Dockerfile                 # Container configuration
├── .dockerignore              # Docker ignore file
├── .gitignore                 # Git ignore file
├── production.env.template    # Environment variables template
├── README.md                  # Project documentation
├── RAILWAY_DEPLOYMENT.md      # Railway deployment guide
├── architecture.md            # This file
├── templates/                 # Jinja2 HTML templates
├── static/                    # Static files (CSS, JS)
├── uploads/                   # File upload directory
└── test_files/                # Test and debug scripts
```

## Core Application Files

### `main.py`
**Purpose**: FastAPI application entry point and main application logic
**Key Components**:
- FastAPI app initialization
- Route definitions (authentication, projects, chat, file uploads)
- ChatBot integration
- Health check endpoints
- Error handling

**Key Routes**:
- `/` - Root redirect
- `/health` - Health check endpoint
- `/login`, `/register` - Authentication
- `/dashboard` - User dashboard
- `/projects/{id}` - Project management
- `/projects/{id}/chat` - Chat functionality
- `/projects/{id}/upload` - File uploads

### `models.py`
**Purpose**: SQLAlchemy ORM models for database schema
**Models**:
- `User` - User accounts and authentication
- `Project` - Chatbot projects
- `Prompt` - System prompts for projects
- `Message` - Chat messages
- `File` - Uploaded files

**Relationships**:
- User → Projects (one-to-many)
- Project → Prompts (one-to-many)
- Project → Messages (one-to-many)
- Project → Files (one-to-many)

### `auth.py`
**Purpose**: Authentication and authorization utilities
**Key Functions**:
- Password hashing with bcrypt
- JWT token creation and validation
- User authentication
- Current user dependency injection

### `crud.py`
**Purpose**: Database CRUD (Create, Read, Update, Delete) operations
**Key Functions**:
- User management (create, get by email)
- Project management (create, get by user, get by ID)
- Prompt management (create, get by project)
- Message management (create, get by project)
- File management (create, get by project, delete)

### `database.py`
**Purpose**: Database configuration and connection management
**Key Features**:
- SQLite support for development
- PostgreSQL support for production
- Automatic database URL detection
- Connection pooling for production
- Table creation and session management

### `chatbot.py`
**Purpose**: OpenRouter API integration and ChatBot functionality
**Key Features**:
- OpenRouter API client
- Grok 4 model integration
- Conversation context management
- Error handling and rate limiting
- Model validation and selection

**Key Methods**:
- `chat()` - Basic chat functionality
- `chat_with_context()` - Chat with conversation history
- `set_model()` - Change AI model
- `validate_api_key()` - Test API key validity
- `get_available_models()` - List available models

### `config.py`
**Purpose**: Configuration management and environment variables
**Configuration Areas**:
- OpenRouter API settings
- Database configuration
- JWT settings
- File upload settings
- Production environment settings
- Railway deployment settings

## Deployment Files

### `start_server.py`
**Purpose**: Production startup script for Railway deployment
**Features**:
- Environment variable validation
- Production server configuration
- Health check initialization
- Error handling and logging

### `railway.json`
**Purpose**: Railway deployment configuration
**Configuration**:
- Build settings
- Start command
- Health check path
- Restart policy
- Timeout settings

### `Procfile`
**Purpose**: Process definition for Railway
**Process**: `web: python start_server.py`

### `Dockerfile`
**Purpose**: Container configuration for Docker deployment
**Features**:
- Python 3.11 slim base image
- System dependencies installation
- Non-root user for security
- Health check configuration
- Optimized layer caching

### `.dockerignore`
**Purpose**: Docker build context optimization
**Exclusions**:
- Git files
- Python cache
- Virtual environments
- Development files
- Documentation

## Template Files

### `templates/`
**Purpose**: Jinja2 HTML templates for web interface
**Templates**:
- `base.html` - Base template with common layout
- `login.html` - User login form
- `register.html` - User registration form
- `dashboard.html` - User dashboard with project list
- `project.html` - Project page with chat interface

## Static Files

### `static/`
**Purpose**: Static assets (CSS, JavaScript, images)
**Files**:
- `style.css` - Application styling

## Upload Directory

### `uploads/`
**Purpose**: File storage for project uploads
**Features**:
- Automatic directory creation
- Unique filename generation
- File type validation
- Size limits

## Test Files

### Test Scripts
**Purpose**: Testing and debugging utilities
**Files**:
- `test_chatbot.py` - ChatBot integration tests
- `test_server.py` - Server startup tests
- `test_auth.py` - Authentication tests
- `test_routes.py` - Route testing
- `debug_routes.py` - Route debugging
- `final_test.py` - Final integration tests
- `quick_test.py` - Quick functionality tests
- `test_fix.py` - Fix validation tests

## Configuration Files

### `requirements.txt`
**Purpose**: Python package dependencies
**Key Dependencies**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `bcrypt` - Password hashing
- `python-jose` - JWT handling
- `httpx` - HTTP client
- `psycopg2-binary` - PostgreSQL driver

### `.gitignore`
**Purpose**: Git version control exclusions
**Exclusions**:
- Environment files
- Python cache
- Virtual environments
- Database files
- Uploads
- Logs
- IDE files
- OS files

### `production.env.template`
**Purpose**: Environment variables template
**Variables**:
- OpenRouter API configuration
- Database settings
- JWT configuration
- Production settings
- Railway configuration

## Documentation Files

### `README.md`
**Purpose**: Main project documentation
**Sections**:
- Project overview
- Features
- Installation
- Usage
- Configuration
- API endpoints
- Database schema
- Security features
- Development
- Troubleshooting

### `RAILWAY_DEPLOYMENT.md`
**Purpose**: Railway deployment guide
**Sections**:
- Prerequisites
- Deployment steps
- Environment variables
- Configuration files
- Health checks
- Monitoring
- Troubleshooting
- Scaling
- Security
- Cost optimization

## Data Flow Architecture

### Request Flow
1. **Client Request** → FastAPI Router
2. **Authentication** → JWT validation
3. **Database Query** → CRUD operations
4. **AI Processing** → ChatBot integration
5. **Response** → JSON/HTML response

### Chat Flow
1. **User Message** → Project endpoint
2. **Message Storage** → Database
3. **Context Retrieval** → Previous messages
4. **AI Processing** → OpenRouter API
5. **Response Storage** → Database
6. **Response Delivery** → User interface

### File Upload Flow
1. **File Upload** → Upload endpoint
2. **Validation** → File type and size
3. **Storage** → Uploads directory
4. **Database Record** → File metadata
5. **Response** → Success confirmation

## Security Architecture

### Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- Session management
- Cookie-based token storage

### Authorization
- User-based access control
- Project ownership validation
- File access permissions
- API endpoint protection

### Data Protection
- Environment variable encryption
- Secure database connections
- File upload validation
- SQL injection prevention

## Deployment Architecture

### Development
- SQLite database
- Local file storage
- Debug logging
- Hot reload

### Production (Railway)
- PostgreSQL database
- Containerized deployment
- Health monitoring
- Auto-scaling
- HTTPS encryption

## Performance Considerations

### Database
- Connection pooling
- Query optimization
- Index usage
- Transaction management

### API
- Async request handling
- Rate limiting
- Caching strategies
- Error handling

### File Storage
- Size limits
- Type validation
- Cleanup procedures
- Backup strategies

## Monitoring and Logging

### Health Checks
- Database connectivity
- ChatBot initialization
- Application status
- Resource usage

### Logging
- Request logging
- Error tracking
- Performance metrics
- Security events

## Future Enhancements

### Potential Additions
- Real-time WebSocket chat
- File processing capabilities
- Advanced AI model selection
- User management dashboard
- Analytics and reporting
- Multi-language support
- API rate limiting
- Caching layer
- Background task processing

This architecture provides a solid foundation for a scalable, secure, and maintainable chatbot platform with clear separation of concerns and comprehensive deployment support.
