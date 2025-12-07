from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc
import pandas as pd
import requests
import json
from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import sqlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SQL RAG API",
    description="RAG system for SQL Server database with local Llama",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from environment variables
DATABASE_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': os.getenv('DB_SERVER', 'localhost'),
    'database': os.getenv('DB_DATABASE', 'master'),
    'username': os.getenv('DB_USERNAME', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'trusted_connection': os.getenv('DB_TRUSTED_CONNECTION', 'no')
}

# Local Llama server configuration
LLAMA_CONFIG = {
    'base_url': os.getenv('LLAMA_SERVER_URL', 'http://localhost:11434'),
    'model': os.getenv('LLAMA_MODEL', 'llama3.1'),
    'timeout': 120,
    'max_tokens': 2000,
    'temperature': 0.1
}

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    conversation_history: Optional[List[Dict[str, str]]] = []

class QueryResponse(BaseModel):
    sql_query: str
    explanation: str
    data: List[Dict[str, Any]]
    chart_config: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Database helper class
class DatabaseInfo:
    def __init__(self):
        self.schema_info = None
    
    def get_connection(self):
        """Create database connection"""
        if DATABASE_CONFIG['trusted_connection'].lower() == 'yes':
            conn_string = (
                f"DRIVER={DATABASE_CONFIG['driver']};"
                f"SERVER={DATABASE_CONFIG['server']};"
                f"DATABASE={DATABASE_CONFIG['database']};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_string = (
                f"DRIVER={DATABASE_CONFIG['driver']};"
                f"SERVER={DATABASE_CONFIG['server']};"
                f"DATABASE={DATABASE_CONFIG['database']};"
                f"UID={DATABASE_CONFIG['username']};"
                f"PWD={DATABASE_CONFIG['password']};"
            )
        return pyodbc.connect(conn_string)
    
    def get_schema_info(self):
        """Get database schema information"""
        if self.schema_info:
            return self.schema_info
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        schema_query = """
        SELECT 
            t.TABLE_SCHEMA,
            t.TABLE_NAME,
            c.COLUMN_NAME,
            c.DATA_TYPE,
            c.IS_NULLABLE,
            c.COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.TABLES t
        JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME 
            AND t.TABLE_SCHEMA = c.TABLE_SCHEMA
        WHERE t.TABLE_TYPE = 'BASE TABLE'
        ORDER BY t.TABLE_SCHEMA, t.TABLE_NAME, c.ORDINAL_POSITION
        """
        
        df = pd.read_sql(schema_query, conn)
        
        # Group by table
        schema_dict = {}
        for _, row in df.iterrows():
            table_key = f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
            if table_key not in schema_dict:
                schema_dict[table_key] = []
            schema_dict[table_key].append({
                'column': row['COLUMN_NAME'],
                'type': row['DATA_TYPE'],
                'nullable': row['IS_NULLABLE'],
                'default': row['COLUMN_DEFAULT']
            })
        
        conn.close()
        self.schema_info = schema_dict
        return self.schema_info

db_info = DatabaseInfo()

def call_local_llama(prompt: str) -> str:
    """Call local Llama server API - supports multiple formats"""
    try:
        # Try Ollama API format first
        ollama_payload = {
            "model": LLAMA_CONFIG['model'],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": LLAMA_CONFIG['temperature'],
                "num_predict": LLAMA_CONFIG['max_tokens']
            }
        }
        
        response = requests.post(
            f"{LLAMA_CONFIG['base_url']}/api/generate",
            json=ollama_payload,
            timeout=LLAMA_CONFIG['timeout'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        
        # Try OpenAI-compatible format
        openai_payload = {
            "model": LLAMA_CONFIG['model'],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": LLAMA_CONFIG['temperature'],
            "max_tokens": LLAMA_CONFIG['max_tokens']
        }
        
        response = requests.post(
            f"{LLAMA_CONFIG['base_url']}/v1/chat/completions",
            json=openai_payload,
            timeout=LLAMA_CONFIG['timeout'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        
        # Try text-generation-webui format
        textgen_payload = {
            "prompt": prompt,
            "max_new_tokens": LLAMA_CONFIG['max_tokens'],
            "temperature": LLAMA_CONFIG['temperature'],
            "do_sample": True,
        }
        
        response = requests.post(
            f"{LLAMA_CONFIG['base_url']}/api/v1/generate",
            json=textgen_payload,
            timeout=LLAMA_CONFIG['timeout'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['results'][0]['text'].strip()
            
        raise Exception(f"All API formats failed. Status: {response.status_code}")
        
    except requests.exceptions.Timeout:
        raise Exception("Request to Llama server timed out. Try a smaller model or increase timeout.")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to Llama server at {LLAMA_CONFIG['base_url']}. Make sure it's running.")
    except Exception as e:
        raise Exception(f"Llama API Error: {str(e)}")

def generate_sql_with_llm(question: str, schema_info: dict, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Generate SQL query using local Llama model"""
    
    # Create schema context
    schema_context = "Database Schema:\n"
    for table, columns in list(schema_info.items())[:20]:  # Limit to 20 tables
        schema_context += f"\nTable: {table}\n"
        for col in columns[:10]:  # Limit columns per table
            schema_context += f"  - {col['column']} ({col['type']})\n"
    
    # Create conversation context
    conversation_context = ""
    if conversation_history:
        conversation_context = "\nRecent conversation:\n"
        for msg in conversation_history[-2:]:
            conversation_context += f"Q: {msg.get('question', '')}\nSQL: {msg.get('answer', '')}\n"
    
    prompt = f"""You are a SQL Server expert. Generate a valid T-SQL query for the user's question.

{schema_context}
{conversation_context}

User Question: {question}

CRITICAL INSTRUCTIONS:
1. Generate ONLY valid SQL Server T-SQL syntax
2. Use appropriate JOINs when needed
3. Include TOP 100 clause for SELECT statements to limit results
4. Use proper table schema prefixes (e.g., dbo.TableName)
5. Return ONLY a JSON response, no additional text

Response Format (JSON ONLY):
{{
    "sql_query": "SELECT TOP 100 ... FROM ...",
    "explanation": "Brief explanation of what the query does",
    "chart_suggestion": {{
        "type": "bar",
        "x_axis": "column_name",
        "y_axis": "column_name",
        "title": "Chart title"
    }}
}}

Return ONLY the JSON object, nothing else."""

    try:
        response_text = call_local_llama(prompt)
        
        # Extract JSON from response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_text = response_text[json_start:json_end]
            try:
                parsed = json.loads(json_text)
                # Validate required fields
                if 'sql_query' in parsed:
                    return parsed
            except json.JSONDecodeError:
                pass
        
        # Fallback: extract SQL manually
        lines = response_text.split('\n')
        sql_line = ""
        for line in lines:
            line_upper = line.strip().upper()
            if line_upper.startswith('SELECT') or line_upper.startswith('WITH'):
                sql_line = line.strip()
                break
        
        return {
            "sql_query": sql_line,
            "explanation": "Generated SQL query for your question",
            "chart_suggestion": None
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

def execute_sql_query(sql_query: str) -> List[Dict[str, Any]]:
    """Execute SQL query and return results"""
    conn = db_info.get_connection()
    try:
        # Validate SQL
        parsed = sqlparse.parse(sql_query)
        if not parsed:
            raise ValueError("Invalid SQL query")
        
        # Execute query
        df = pd.read_sql(sql_query, conn)
        
        # Convert datetime to string
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert to dict
        return df.to_dict('records')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL Execution Error: {str(e)}")
    finally:
        conn.close()

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SQL RAG API is running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "schema": "/schema",
            "tables": "/tables",
            "query": "/query",
            "llama_status": "/llama-status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/schema")
async def get_schema():
    """Get database schema information"""
    try:
        schema = db_info.get_schema_info()
        return {"schema": schema, "table_count": len(schema)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch schema: {str(e)}")

@app.get("/tables")
async def get_tables():
    """Get list of all tables"""
    try:
        schema = db_info.get_schema_info()
        tables = list(schema.keys())
        return {"tables": tables, "count": len(tables)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tables: {str(e)}")

@app.get("/llama-status")
async def check_llama_status():
    """Check if local Llama server is accessible"""
    try:
        test_response = call_local_llama("Say 'OK' if you're working")
        return {
            "status": "connected",
            "server_url": LLAMA_CONFIG['base_url'],
            "model": LLAMA_CONFIG['model'],
            "test_response": test_response[:100]
        }
    except Exception as e:
        return {
            "status": "error",
            "server_url": LLAMA_CONFIG['base_url'],
            "model": LLAMA_CONFIG['model'],
            "error": str(e)
        }

@app.post("/query", response_model=QueryResponse)
async def query_database(request: QueryRequest):
    """Process natural language query and return results"""
    try:
        # Get schema
        schema = db_info.get_schema_info()
        
        # Generate SQL
        llm_response = generate_sql_with_llm(
            request.question,
            schema,
            request.conversation_history
        )
        
        sql_query = llm_response.get("sql_query", "")
        explanation = llm_response.get("explanation", "")
        chart_suggestion = llm_response.get("chart_suggestion")
        
        if not sql_query:
            return QueryResponse(
                sql_query="",
                explanation="Could not generate SQL query",
                data=[],
                error="Failed to generate valid SQL query"
            )
        
        # Execute SQL
        data = execute_sql_query(sql_query)
        
        return QueryResponse(
            sql_query=sql_query,
            explanation=explanation,
            data=data,
            chart_config=chart_suggestion
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return QueryResponse(
            sql_query="",
            explanation="",
            data=[],
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Starting SQL RAG API Server")
    print("=" * 60)
    print(f"📊 Database: {DATABASE_CONFIG['database']} on {DATABASE_CONFIG['server']}")
    print(f"🤖 LLM Server: {LLAMA_CONFIG['base_url']}")
    print(f"🔧 Model: {LLAMA_CONFIG['model']}")
    print(f"🌐 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)