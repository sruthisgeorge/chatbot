# Railway Deployment Guide

This guide will help you deploy the Chatbot Platform to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **OpenRouter API Key**: Get your API key from [openrouter.ai](https://openrouter.ai)
3. **GitHub Repository**: Push your code to GitHub

## Deployment Steps

### 1. Connect to Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the Python project

### 2. Add Environment Variables

In your Railway project dashboard, go to the "Variables" tab and add:

#### Required Variables
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

#### Optional Variables
```
OPENROUTER_MODEL=x-ai/grok-4-fast:free
SECRET_KEY=your-secure-secret-key-here
ENVIRONMENT=production
DEBUG=false
```

### 3. Add PostgreSQL Database (Recommended)

1. In your Railway project, click "New"
2. Select "Database"  "PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

### 4. Deploy

1. Railway will automatically deploy when you push to your main branch
2. Monitor the deployment in the "Deployments" tab
3. Check logs if there are any issues

## Configuration Files

The following files are included for Railway deployment:

- `railway.json` - Railway configuration
- `Procfile` - Process definition
- `start_server.py` - Production startup script
- `Dockerfile` - Container configuration (optional)
- `.dockerignore` - Docker ignore file

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | - | Yes |
| `OPENROUTER_MODEL` | AI model to use | `x-ai/grok-4-fast:free` | No |
| `DATABASE_URL` | Database connection string | Auto-set by Railway | No |
| `SECRET_KEY` | JWT secret key | Random | No |
| `ENVIRONMENT` | Environment name | `development` | No |
| `DEBUG` | Debug mode | `false` | No |
| `PORT` | Server port | `8000` | No |
| `HOST` | Server host | `0.0.0.0` | No |

## Health Checks

Railway will automatically monitor your application using the `/health` endpoint, which checks:

- Database connectivity
- ChatBot initialization
- Overall application health

## Monitoring

1. **Logs**: View real-time logs in the Railway dashboard
2. **Metrics**: Monitor CPU, memory, and network usage
3. **Health**: Check the `/health` endpoint for detailed status

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Runtime Errors**
   - Verify environment variables are set correctly
   - Check logs for specific error messages

3. **Database Issues**
   - Ensure PostgreSQL service is running
   - Check `DATABASE_URL` is set correctly

4. **API Errors**
   - Verify `OPENROUTER_API_KEY` is valid
   - Check OpenRouter service status

### Debug Commands

```bash
# Check health endpoint
curl https://your-app.railway.app/health

# View logs
railway logs

# Connect to database
railway connect
```

## Scaling

Railway automatically handles:
- Load balancing
- Auto-scaling based on traffic
- Zero-downtime deployments

## Security

- Environment variables are encrypted
- HTTPS is enabled by default
- Database connections are secure
- JWT tokens are properly configured

## Cost Optimization

- Railway offers a free tier with usage limits
- Monitor usage in the dashboard
- Consider upgrading for production workloads

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- OpenRouter Support: [openrouter.ai](https://openrouter.ai)
