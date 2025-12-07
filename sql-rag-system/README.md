# 🌌 SQL Server RAG System with Galaxy Background

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
