#!/usr/bin/env python3
"""
SQL Server RAG System - Automatic Project Generator
This script creates all necessary files and directory structure
"""

import os
import sys

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        "sql-rag-system",
        "sql-rag-system/backend",
        "sql-rag-system/frontend",
        "sql-rag-system/frontend/public",
        "sql-rag-system/frontend/src"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_file(path, content):
    """Create a file with given content"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created file: {path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create {path}: {e}")
        return False

def generate_files():
    """Generate all project files"""
    
    files = {}
    
    # ==================== ROOT FILES ====================
    
    files["sql-rag-system/README.md"] = '''# 🌌 SQL Server RAG System with Galaxy Background

A beautiful, intelligent database query interface that lets you chat with your SQL Server database using natural language. Powered by local LLMs and featuring a stunning WebGL galaxy background.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![React](https://img.shields.io/badge/react-18.2+-61dafb)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- 🌌 **WebGL Galaxy Background** - Interactive starfield with mouse interaction
- 🤖 **Local LLM Integration** - No external API calls, 100% private
- 💬 **Natural Language Queries** - Ask questions in plain English
- 📊 **Auto Visualizations** - Generates charts based on data type
- 🔒 **Privacy First** - All processing happens locally
- 📝 **Query History** - Track your searches
- 🎨 **Customizable** - Colors, themes, and settings

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- SQL Server
- Ollama (or another local LLM server)

### Installation

1. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.template .env
   # Edit .env with your settings
   python app.py
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Start Ollama**
   ```bash
   ollama serve
   ollama pull llama3.1
   ```

📖 **For detailed instructions, see QUICK_START.md**

## 🎯 Example Queries

```
"What tables are in my database?"
"Show me 10 rows from the customers table"
"Count total orders by month"
"Top 5 products by revenue"
```

## 📚 Documentation

- **QUICK_START.md** - Get running in 15 minutes
- **SETUP_INSTRUCTIONS.md** - Detailed setup guide

## 🛠️ Tech Stack

- **Backend:** FastAPI, PyODBC, Pandas
- **Frontend:** React 18, Recharts, OGL (WebGL)
- **AI/LLM:** Ollama, Llama 3.1, CodeLlama

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

---

**Built with ❤️ for database administrators and data analysts**
'''

    files["sql-rag-system/QUICK_START.md"] = '''# 🚀 Quick Start Guide - SQL Server RAG System

Get up and running in 15 minutes!

## Prerequisites Check

- [ ] Python 3.8+: `python --version`
- [ ] Node.js 14+: `node --version`
- [ ] SQL Server accessible
- [ ] Ollama installed

## Step 1: Setup Ollama (5 minutes)

```bash
# Install Ollama
# Windows: Download from https://ollama.com/download
# Linux/Mac:
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.1

# Start Ollama (keep this terminal open)
ollama serve
```

## Step 2: Setup Backend (5 minutes)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.template .env

# Edit .env with your database credentials
# Windows: notepad .env
# Linux/Mac: nano .env

# Test connections
python test_connection.py

# Start backend
python app.py
```

## Step 3: Setup Frontend (5 minutes)

Open a NEW terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Browser should open at `http://localhost:3000`

## 🎉 You're Ready!

1. Check Status Tab - Verify connections are green ✅
2. Try a query: "What tables do I have?"
3. Explore the Schema tab
4. Customize the Galaxy background colors!

## 🐛 Troubleshooting

**Backend won't start:**
```bash
python test_connection.py
```

**Frontend errors:**
```bash
rm -rf node_modules
npm install
```

**Ollama not connecting:**
```bash
curl http://localhost:11434/api/tags
```
'''

    # ==================== BACKEND FILES ====================
    
    files["sql-rag-system/backend/requirements.txt"] = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pyodbc==0.4.39
pandas==2.1.3
sqlparse==0.4.4
requests==2.31.0
python-dotenv==1.0.0
pydantic==2.4.2
'''

    files["sql-rag-system/backend/.env.template"] = '''# SQL Server RAG System - Environment Configuration

# Local LLM Server Configuration
LLAMA_SERVER_URL=http://localhost:11434
LLAMA_MODEL=llama3.1

# SQL Server Database Configuration
DB_SERVER=localhost
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_TRUSTED_CONNECTION=no

# Examples:
# Local SQL Server with SQL Auth:
# DB_SERVER=localhost
# DB_DATABASE=AdventureWorks
# DB_USERNAME=sa
# DB_PASSWORD=YourPassword123
# DB_TRUSTED_CONNECTION=no

# Remote SQL Server with Windows Auth:
# DB_SERVER=sql-server.company.com
# DB_DATABASE=SalesDB
# DB_TRUSTED_CONNECTION=yes
'''

    files["sql-rag-system/backend/.gitignore"] = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual Environment
venv/
env/
ENV/
.venv

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite
'''

    # Note: app.py and test_connection.py are too long for this generator
    # They need to be copied from the artifacts
    
    files["sql-rag-system/backend/_COPY_app.py.txt"] = '''
⚠️ IMPORTANT: This file is a placeholder.

Please copy the content of the 'backend_app' artifact to create app.py

The app.py file is approximately 350 lines and contains:
- FastAPI server setup
- Local Llama integration
- SQL generation logic
- Database connection handling
- API endpoints

Artifact name: backend_app
Target file: backend/app.py
'''

    files["sql-rag-system/backend/_COPY_test_connection.py.txt"] = '''
⚠️ IMPORTANT: This file is a placeholder.

Please copy the content of the 'test_scripts' artifact to create test_connection.py

The test_connection.py file is approximately 200 lines and contains:
- Database connection testing
- Llama server connection testing
- Model availability checking
- Diagnostic output

Artifact name: test_scripts
Target file: backend/test_connection.py
'''

    # ==================== FRONTEND FILES ====================
    
    files["sql-rag-system/frontend/package.json"] = '''{
  "name": "sql-rag-frontend",
  "version": "1.0.0",
  "description": "SQL Server RAG System - Frontend",
  "private": true,
  "proxy": "http://localhost:8000",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "recharts": "^2.8.0",
    "lucide-react": "^0.263.1",
    "ogl": "^1.0.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": ["react-app"]
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version"]
  }
}
'''

    files["sql-rag-system/frontend/.gitignore"] = '''# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Production
/build

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
'''

    files["sql-rag-system/frontend/public/index.html"] = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="SQL Server RAG System - Chat with your database" />
    <title>SQL Server RAG - Database Chat Assistant</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''

    files["sql-rag-system/frontend/src/index.js"] = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''

    files["sql-rag-system/frontend/src/index.css"] = '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
}

#root {
  min-height: 100vh;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.7);
}
'''

    files["sql-rag-system/frontend/src/Galaxy.css"] = '''.galaxy-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.galaxy-container canvas {
  width: 100% !important;
  height: 100% !important;
}
'''

    files["sql-rag-system/frontend/src/_COPY_App.js.txt"] = '''
⚠️ IMPORTANT: This file is a placeholder.

Please copy the content of the 'frontend_app_webgl' artifact to create App.js

The App.js file is approximately 650 lines and contains:
- React main application component
- Galaxy background integration
- Chat interface
- Chart rendering
- Data table display
- Status monitoring

Artifact name: frontend_app_webgl
Target file: frontend/src/App.js
'''

    files["sql-rag-system/frontend/src/_COPY_Galaxy.jsx.txt"] = '''
⚠️ IMPORTANT: This file is a placeholder.

Please copy the WebGL Galaxy component from the document you provided earlier.

The Galaxy.jsx file is approximately 350 lines and contains:
- WebGL shader code
- OGL rendering
- Mouse interaction
- Star field generation
- Customizable parameters

Source: The document you provided with the OGL imports
Target file: frontend/src/Galaxy.jsx
'''

    # Create all files
    print("\n" + "="*60)
    print("🌌 SQL Server RAG System - Project Generator")
    print("="*60 + "\n")
    
    total_files = len(files)
    created_files = 0
    
    for filepath, content in files.items():
        if create_file(filepath, content):
            created_files += 1
    
    print("\n" + "="*60)
    print(f"📊 Summary: Created {created_files}/{total_files} files")
    print("="*60 + "\n")
    
    # Print instructions for manual files
    print("⚠️  MANUAL STEPS REQUIRED:\n")
    print("The following files need to be copied manually from artifacts:\n")
    print("1. backend/app.py")
    print("   → Copy from artifact: 'backend_app'")
    print("   → Approximately 350 lines\n")
    
    print("2. backend/test_connection.py")
    print("   → Copy from artifact: 'test_scripts'")
    print("   → Approximately 200 lines\n")
    
    print("3. frontend/src/App.js")
    print("   → Copy from artifact: 'frontend_app_webgl'")
    print("   → Approximately 650 lines\n")
    
    print("4. frontend/src/Galaxy.jsx")
    print("   → Copy from the document you provided")
    print("   → Approximately 350 lines\n")
    
    print("="*60)
    print("📁 Project Structure Created:")
    print("="*60)
    print("""
sql-rag-system/
├── README.md
├── QUICK_START.md
├── backend/
│   ├── requirements.txt
│   ├── .env.template
│   ├── .gitignore
│   ├── _COPY_app.py.txt (placeholder)
│   └── _COPY_test_connection.py.txt (placeholder)
└── frontend/
    ├── package.json
    ├── .gitignore
    ├── public/
    │   └── index.html
    └── src/
        ├── index.js
        ├── index.css
        ├── Galaxy.css
        ├── _COPY_App.js.txt (placeholder)
        └── _COPY_Galaxy.jsx.txt (placeholder)
""")
    
    print("="*60)
    print("✅ Next Steps:")
    print("="*60)
    print("""
1. Copy the 4 large files from artifacts (see above)
2. Edit backend/.env with your database credentials
3. Install backend: cd backend && pip install -r requirements.txt
4. Install frontend: cd frontend && npm install
5. Start Ollama: ollama serve && ollama pull llama3.1
6. Start backend: python backend/app.py
7. Start frontend: npm start (in frontend directory)
8. Open http://localhost:3000

🎉 Enjoy your Database RAG System!
""")

if __name__ == "__main__":
    try:
        create_directory_structure()
        print()
        generate_files()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)