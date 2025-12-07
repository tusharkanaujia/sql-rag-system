# 🚀 Quick Start Guide - SQL Server RAG System

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
