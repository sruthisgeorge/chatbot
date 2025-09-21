# Chatbot Platform

A minimalistic chatbot platform built with FastAPI, SQLite, and OpenRouter API. This platform allows users to create projects/agents, manage prompts, and chat with AI models using Grok 4 and other advanced models through OpenRouter.

## Features

- **User Authentication**: JWT-based authentication with email/password
- **Project Management**: Create and manage multiple chatbot projects
- **Prompt Management**: Associate system prompts with projects
- **Chat Interface**: Real-time chat with AI models
- **File Upload**: Upload and manage files for projects
- **Responsive UI**: Clean, modern interface using Bootstrap

## Project Structure

```
 main.py              # FastAPI application entry point
 models.py            # SQLAlchemy ORM models
 auth.py              # Authentication utilities (JWT, bcrypt)
 crud.py              # Database CRUD operations
 database.py          # Database configuration
 chatbot.py           # OpenAI ChatBot integration class
 config.py            # Configuration management
 test_chatbot.py      # ChatBot testing script
 requirements.txt     # Python dependencies
 templates/           # Jinja2 HTML templates
    base.html
    login.html
    register.html
    dashboard.html
    project.html
 static/              # Static files (CSS, JS)
    style.css
 uploads/             # File upload directory (created automatically)
```

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenRouter API**:
   - Get your API key from [OpenRouter](https://openrouter.ai/)
   - Set the environment variable:
     ```bash
     export OPENROUTER_API_KEY="your_api_key_here"
     ```
   - Or create a `.env` file with:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```

4. **Test the ChatBot integration** (optional):
   ```bash
   python test_chatbot.py
   ```

5. **Run the application**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**:
   Open your browser and go to `http://localhost:8000`

## Railway Deployment

This application is ready for deployment on Railway. See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed deployment instructions.

### Quick Railway Deployment

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Railway**: Go to [railway.app](https://railway.app) and connect your repository
3. **Set Environment Variables**:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `SECRET_KEY`: A secure secret key for JWT tokens
4. **Add PostgreSQL**: Add a PostgreSQL database service in Railway
5. **Deploy**: Railway will automatically deploy your application

The application includes:
- Railway configuration files (`railway.json`, `Procfile`)
- Production startup script (`start_server.py`)
- Docker support (`Dockerfile`)
- Health check endpoints (`/health`)
- PostgreSQL support for production
- Environment variable configuration

## Usage

### Getting Started

1. **Register**: Create a new account with your email and password
2. **Login**: Sign in to access your dashboard
3. **Create Project**: Click "Create New Project" to start a new chatbot project
4. **Add Prompts**: Set system prompts to define your chatbot's behavior
5. **Chat**: Start chatting with your AI agent
6. **Upload Files**: Add files to your project for reference

### API Endpoints

- `GET /` - Redirects to login
- `GET /login` - Login page
- `POST /login` - Handle login
- `GET /register` - Registration page
- `POST /register` - Handle registration
- `GET /dashboard` - User dashboard
- `POST /projects` - Create new project
- `GET /projects/{id}` - Project page with chat
- `POST /projects/{id}/prompts` - Add system prompt
- `POST /projects/{id}/chat` - Send chat message
- `POST /projects/{id}/upload` - Upload file
- `GET /files/{id}` - Download file

## Configuration

### Environment Variables

You can set these environment variables to customize the application:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `OPENROUTER_MODEL`: Model to use (default: "x-ai/grok-2-1212" for Grok 4)
- `SECRET_KEY`: JWT secret key (default: "your-secret-key-change-in-production")
- `DATABASE_URL`: Database connection string (default: "sqlite:///./chatbot.db")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time (default: 30)
- `MAX_FILE_SIZE`: Maximum file upload size in bytes (default: 10485760 = 10MB)

### OpenRouter Integration

The platform now includes full OpenRouter integration through the `ChatBot` class:

- **Automatic API Key Management**: Uses environment variables or config
- **Conversation Context**: Maintains chat history for better responses
- **Error Handling**: Graceful handling of API errors and rate limits
- **Model Selection**: Support for multiple AI models including Grok 4, Claude, GPT, and more
- **System Prompts**: Custom system prompts per project
- **Grok 4 Personality**: Default system prompt includes Grok's characteristic wit and directness

The `ChatBot` class provides these methods:
- `chat()`: Basic chat functionality
- `chat_with_context()`: Chat with conversation history
- `set_model()`: Change the AI model
- `validate_api_key()`: Test API key validity
- `get_available_models()`: List available models from OpenRouter

## Database Schema

### Tables

- **users**: User accounts (id, email, password_hash, created_at)
- **projects**: Chatbot projects (id, user_id, name, created_at)
- **prompts**: System prompts (id, project_id, text, created_at)
- **messages**: Chat messages (id, project_id, role, content, timestamp)
- **files**: Uploaded files (id, project_id, filename, file_path, file_size, content_type, uploaded_at)

### Relationships

- User  Projects (one-to-many)
- Project  Prompts (one-to-many)
- Project  Messages (one-to-many)
- Project  Files (one-to-many)

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- User session management
- File upload validation
- SQL injection protection via SQLAlchemy ORM

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Reset

To reset the database, simply delete the `chatbot.db` file and restart the application. The tables will be recreated automatically.

### Adding New Features

1. **Models**: Add new tables in `models.py`
2. **CRUD**: Add database operations in `crud.py`
3. **Routes**: Add new endpoints in `main.py`
4. **Templates**: Create new HTML templates in `templates/`
5. **Static Files**: Add CSS/JS in `static/`

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in the uvicorn command
2. **Database errors**: Delete `chatbot.db` and restart
3. **Import errors**: Ensure all dependencies are installed
4. **File upload issues**: Check that the `uploads/` directory exists and is writable
5. **OpenRouter API errors**: 
   - Verify your API key is correct and has sufficient credits
   - Check your internet connection
   - Ensure you're not hitting rate limits
   - Verify the model (x-ai/grok-2-1212) is available
   - Run `python test_chatbot.py` to diagnose issues

### Logs

The application logs are displayed in the terminal where you run uvicorn. For production, consider using a proper logging configuration.

## License

This project is open source and available under the MIT License.
