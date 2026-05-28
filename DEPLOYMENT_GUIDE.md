# Umukozi Deployment Guide

## 🚀 Database Connection Issue - SOLVED

### Problem
Application deployed but no database connection available.

### Solution
Database tables have been successfully initialized and the application is now ready.

---

## 📋 Deployment Steps

### 1. Environment Setup
```bash
# Run the deployment setup script
python deploy_setup.py
```

### 2. Database Initialization
```bash
# Initialize database with all tables
python init_database.py
```

### 3. Start the Application

#### Option A: Direct Python (Development/SQLite)
```bash
python app.py
```

#### Option B: Docker (Production/PostgreSQL)
```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

---

## 🔧 Database Configuration

### Development (SQLite)
- **Database File:** `instance/umukozi.db`
- **URL:** `sqlite:///umukozi.db`
- **Auto-created:** Yes

### Production (PostgreSQL)
- **Host:** `localhost:5432` (or `db:5432` in Docker)
- **Database:** `umukozi_db`
- **User:** `umukozi_user`
- **URL:** `postgresql://umukozi_user:password@localhost:5432/umukozi_db`

---

## 👤 Default Admin Account

**Email:** `admin@umukozi.rw`  
**Password:** `admin123`  
**⚠️ Important:** Change this password after first login!

---

## 🌍 Environment Variables

Create a `.env` file with these settings:

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key

# Database Configuration
DATABASE_URL=sqlite:///umukozi.db  # For development
# DATABASE_URL=postgresql://user:pass@host:5432/db  # For production

# File Upload
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

---

## 🐳 Docker Deployment

### Quick Start
```bash
# Start all services
docker-compose up -d

# Initialize database (first time only)
docker-compose exec web python init_database.py

# Access the application
http://localhost:5000
```

### Services Included
- **web:** Flask application (Port 5000)
- **db:** PostgreSQL database (Port 5432)
- **redis:** Redis cache (Port 6379)
- **nginx:** Reverse proxy (Ports 80, 443)

---

## 🔍 Troubleshooting

### Database Connection Issues
1. **Check DATABASE_URL** in `.env` file
2. **Verify database service** is running
3. **Run initialization script:** `python init_database.py`

### Permission Issues
```bash
# Create required directories
mkdir -p instance static/uploads logs

# Set proper permissions
chmod 755 instance static/uploads logs
```

### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs web
docker-compose logs db
```

---

## 📊 Database Status

✅ **Database:** Connected  
✅ **Tables:** Created  
✅ **Admin User:** Ready  
✅ **Application:** Ready to start  

---

## 🎯 Next Steps

1. **Change admin password** after first login
2. **Configure email settings** if using notifications
3. **Set up SSL certificates** for production
4. **Configure backup strategy** for database
5. **Monitor application logs** regularly

---

## 📞 Support

If you encounter issues:
1. Check the logs in the `logs/` directory
2. Verify all environment variables are set
3. Ensure database service is running
4. Review this guide for common solutions

The application is now fully configured and ready for use! 🎉
