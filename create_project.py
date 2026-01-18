#!/usr/bin/env python3
"""
SQL Server RAG System - Complete Project Generator
Generates all files needed for the SQL Server RAG System
"""

import os
import sys

# Color codes for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def print_status(msg):
    print(f"{BLUE}[INFO]{RESET} {msg}")

def print_success(msg):
    print(f"{GREEN}[✓]{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}[!]{RESET} {msg}")

def print_error(msg):
    print(f"{RED}[✗]{RESET} {msg}")

def create_file(path, content):
    """Create a file with content"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"Created: {path}")
        return True
    except Exception as e:
        print_error(f"Failed to create {path}: {e}")
        return False

def main():
    print("\n" + "="*70)
    print(f"{BLUE}🌌 SQL Server RAG System - Complete Project Generator{RESET}")
    print("="*70 + "\n")
    
    base_dir = "sql-rag-system"
    
    # Create directory structure
    print_status("Creating directory structure...")
    dirs = [
        base_dir,
        f"{base_dir}/backend",
        f"{base_dir}/frontend",
        f"{base_dir}/frontend/public",
        f"{base_dir}/frontend/src"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    print_success(f"Created {len(dirs)} directories\n")
    
    # File contents
    files = {}
    
    # ========== ROOT FILES ==========
    
    files[f"{base_dir}/README.md"] = """# 🌌 SQL Server RAG System with Galaxy Background

A beautiful, intelligent database query interface powered by local LLMs with a stunning WebGL galaxy background.

## ✨ Features

- 🌌 **WebGL Galaxy Background** - Interactive animated starfield
- 🤖 **Local LLM** - Privacy-first, no API costs
- 💬 **Natural Language** - Talk to your database in plain English
- 📊 **Auto Charts** - Bar, line, and pie chart generation
- 🔒 **100% Private** - All processing happens locally
- 📝 **Smart Context** - Remembers conversation history

## 🚀 Quick Start

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
cp .env.template .env  # Edit with your DB settings
python app.py

# 2. Frontend (new terminal)
cd frontend
npm install
npm start

# 3. Ollama (new terminal)
ollama serve
ollama pull llama3.1
```

Open http://localhost:3000

## 📚 Documentation

- See `backend/README.md` for API documentation
- See `frontend/README.md` for frontend details
- Example queries and customization in docs

## 🛠️ Tech Stack

- Backend: FastAPI, PyODBC, Pandas
- Frontend: React, Recharts, OGL (WebGL)
- AI: Ollama, Llama 3.1 / CodeLlama

## 📝 License

MIT License - Free to use and modify
"""

    files[f"{base_dir}/backend/README.md"] = """# Backend - SQL Server RAG API

FastAPI server that converts natural language to SQL queries using local LLM.

## Setup

```bash
pip install -r requirements.txt
cp .env.template .env
# Edit .env with your database credentials
python test_connection.py
python app.py
```

## Configuration

Edit `.env`:

```env
LLAMA_SERVER_URL=http://localhost:11434
LLAMA_MODEL=llama3.1
DB_SERVER=localhost
DB_DATABASE=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password
```

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /schema` - Database schema
- `GET /tables` - List tables
- `GET /llama-status` - LLM server status
- `POST /query` - Execute natural language query

## Testing

```bash
python test_connection.py
```

## Supported LLM Servers

- Ollama (recommended)
- text-generation-webui
- LocalAI
- Any OpenAI-compatible API
"""

    files[f"{base_dir}/frontend/README.md"] = """# Frontend - React Application

React application with WebGL Galaxy background.

## Setup

```bash
npm install
npm start
```

Opens at http://localhost:3000

## Components

- **App.js** - Main application
- **Galaxy.jsx** - WebGL background
- **Galaxy.css** - Styles

## Customization

Edit Galaxy props in App.js:

```javascript
<Galaxy
  hueShift={240}      // Color: 240=blue, 280=purple, 120=green
  saturation={0.8}    // Color intensity (0-1)
  glowIntensity={0.5} // Star brightness (0-1)
  density={1.2}       // Star count (0.5-3)
/>
```

## Build for Production

```bash
npm run build
```

Output in `build/` directory.
"""

    files[f"{base_dir}/backend/requirements.txt"] = """# FastAPI and web framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6

# Database connectivity
pyodbc>=4.0.39
pandas>=2.0.0
sqlparse>=0.4.4

# HTTP requests for local LLM
requests>=2.31.0

# Additional utilities
python-dotenv>=1.0.0
pydantic>=2.4.0
"""

    files[f"{base_dir}/backend/.env.template"] = """# ============================================
# SQL Server RAG System - Configuration
# ============================================

# Local LLM Server
LLAMA_SERVER_URL=http://localhost:11434
LLAMA_MODEL=llama3.1

# SQL Server Database
DB_SERVER=localhost
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_TRUSTED_CONNECTION=no

# Examples:
# Windows Auth: DB_TRUSTED_CONNECTION=yes
# SQL Auth: DB_TRUSTED_CONNECTION=no (provide username/password)
"""

    files[f"{base_dir}/backend/.gitignore"] = """# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/

# Virtual Environment
venv/
env/
.venv/

# Environment
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
"""

    files[f"{base_dir}/frontend/package.json"] = """{
  "name": "sql-rag-frontend",
  "version": "1.0.0",
  "private": true,
  "proxy": "http://localhost:8000",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "recharts": "^2.10.0",
    "lucide-react": "^0.263.1",
    "ogl": "^1.0.6"
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
    "production": [">0.2%", "not dead"],
    "development": ["last 1 chrome version", "last 1 firefox version"]
  }
}
"""

    files[f"{base_dir}/frontend/.gitignore"] = """# Dependencies
node_modules/
.pnp/

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
"""

    files[f"{base_dir}/frontend/public/index.html"] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000428" />
    <meta name="description" content="SQL Server RAG System - Chat with your database using natural language" />
    <title>SQL Server RAG Assistant</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""

    files[f"{base_dir}/frontend/src/index.js"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

    files[f"{base_dir}/frontend/src/index.css"] = """* {
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
  font-family: 'Courier New', monospace;
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
}

::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.7);
}
"""

    files[f"{base_dir}/frontend/src/Galaxy.css"] = """.galaxy-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.galaxy-container canvas {
  width: 100% !important;
  height: 100% !important;
}
"""

    # Placeholder files for large components
    files[f"{base_dir}/backend/_INSTRUCTIONS_app.py.md"] = """# ⚠️ REQUIRED: Copy app.py

This file needs to be created manually.

## Steps:

1. Look for the artifact named: **`backend_app`**
2. Copy the entire content (~350 lines)
3. Create file: `backend/app.py`
4. Paste the content and save

## What it contains:
- FastAPI server setup
- Local Llama integration  
- SQL generation with LLM
- Database connection handling
- API endpoints (/query, /schema, /tables, etc.)

## Verify:
After copying, you should be able to run:
```bash
python app.py
```
"""

    files[f"{base_dir}/backend/_INSTRUCTIONS_test_connection.py.md"] = """# ⚠️ REQUIRED: Copy test_connection.py

This file needs to be created manually.

## Steps:

1. Look for the artifact named: **`test_scripts`**
2. Copy the entire content (~200 lines)
3. Create file: `backend/test_connection.py`
4. Paste the content and save

## What it contains:
- Database connection testing
- Llama server connection testing
- Model availability check
- Diagnostic output

## Verify:
After copying, you should be able to run:
```bash
python test_connection.py
```
"""

    files[f"{base_dir}/frontend/src/_INSTRUCTIONS_App.js.md"] = """# ⚠️ REQUIRED: Copy App.js

This file needs to be created manually.

## Steps:

1. Look for the artifact named: **`frontend_app_webgl`**
2. Copy the entire content (~650 lines)
3. Create file: `frontend/src/App.js`
4. Paste the content and save

## What it contains:
- Main React application
- Galaxy background integration
- Chat interface
- Chart rendering with Recharts
- Data table display
- Status monitoring

## Verify:
After copying, the file should start with:
```javascript
import React, { useState, useEffect } from 'react';
import { LineChart, Line, ... } from 'recharts';
```
"""

    files[f"{base_dir}/frontend/src/_INSTRUCTIONS_Galaxy.jsx.md"] = """# ⚠️ REQUIRED: Copy Galaxy.jsx

This file needs to be created manually.

## Steps:

1. Use the **WebGL Galaxy component** from the document you provided earlier
2. Copy the entire content (~350 lines)
3. Create file: `frontend/src/Galaxy.jsx` (or `Galaxy.tsx`)
4. Paste the content and save

## What it contains:
- WebGL shader code (vertex and fragment)
- OGL rendering engine
- Mouse interaction handling
- Star field generation
- Customizable parameters

## Verify:
After copying, the file should start with:
```javascript
import { Renderer, Program, Mesh, Color, Triangle } from 'ogl';
import { useEffect, useRef } from 'react';
import './Galaxy.css';
```
"""

    # Create all files
    print_status("Generating project files...\n")
    
    created = 0
    failed = 0
    
    for filepath, content in files.items():
        if create_file(filepath, content):
            created += 1
        else:
            failed += 1
    
    print(f"\n{'='*70}")
    print(f"{GREEN}✓ Created {created} files{RESET}")
    if failed > 0:
        print(f"{RED}✗ Failed {failed} files{RESET}")
    print(f"{'='*70}\n")
    
    # Print next steps
    print(f"{YELLOW}📋 IMPORTANT - Manual Steps Required:{RESET}\n")
    print("You need to copy 4 large files from the chat artifacts:\n")
    
    steps = [
        ("backend/app.py", "backend_app", "~350 lines"),
        ("backend/test_connection.py", "test_scripts", "~200 lines"),
        ("frontend/src/App.js", "frontend_app_webgl", "~650 lines"),
        ("frontend/src/Galaxy.jsx", "User's document", "~350 lines")
    ]
    
    for i, (file, artifact, size) in enumerate(steps, 1):
        print(f"{i}. {BLUE}{file}{RESET}")
        print(f"   Artifact: {artifact}")
        print(f"   Size: {size}")
        print()
    
    print(f"{'='*70}")
    print(f"{GREEN}✅ Next Steps:{RESET}")
    print(f"{'='*70}\n")
    
    print("1. Copy the 4 files above from artifacts")
    print("2. Configure database:")
    print(f"   {BLUE}cd {base_dir}/backend{RESET}")
    print(f"   {BLUE}cp .env.template .env{RESET}")
    print(f"   {BLUE}nano .env{RESET}  # Edit with your settings")
    print("\n3. Install backend:")
    print(f"   {BLUE}pip install -r requirements.txt{RESET}")
    print(f"   {BLUE}python test_connection.py{RESET}")
    print(f"   {BLUE}python app.py{RESET}")
    print("\n4. Install frontend (new terminal):")
    print(f"   {BLUE}cd {base_dir}/frontend{RESET}")
    print(f"   {BLUE}npm install{RESET}")
    print(f"   {BLUE}npm start{RESET}")
    print("\n5. Start Ollama (new terminal):")
    print(f"   {BLUE}ollama serve{RESET}")
    print(f"   {BLUE}ollama pull llama3.1{RESET}")
    print("\n6. Open browser:")
    print(f"   {BLUE}http://localhost:3000{RESET}")
    print(f"\n{'='*70}")
    print(f"{GREEN}🎉 Project structure created successfully!{RESET}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}Operation cancelled{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{RED}Error: {e}{RESET}")
        sys.exit(1)
