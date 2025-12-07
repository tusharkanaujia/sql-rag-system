"""
Test script to verify database and Llama server connections
"""
import pyodbc
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DATABASE_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': os.getenv('DB_SERVER', 'localhost'),
    'database': os.getenv('DB_DATABASE', 'master'),
    'username': os.getenv('DB_USERNAME', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'trusted_connection': os.getenv('DB_TRUSTED_CONNECTION', 'no')
}

LLAMA_CONFIG = {
    'base_url': os.getenv('LLAMA_SERVER_URL', 'http://localhost:11434'),
    'model': os.getenv('LLAMA_MODEL', 'llama3.1')
}

def test_database_connection():
    """Test SQL Server database connection"""
    print("\n" + "="*60)
    print("🔍 Testing Database Connection")
    print("="*60)
    
    try:
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
        
        print(f"📊 Server: {DATABASE_CONFIG['server']}")
        print(f"📊 Database: {DATABASE_CONFIG['database']}")
        print(f"🔐 Auth: {'Windows' if DATABASE_CONFIG['trusted_connection'].lower() == 'yes' else 'SQL'}")
        
        conn = pyodbc.connect(conn_string)
        print("✅ Database connection successful!")
        
        cursor = conn.cursor()
        
        # Get table count
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        table_count = cursor.fetchone()[0]
        print(f"✅ Found {table_count} tables in database")
        
        # Get sample table names
        cursor.execute("""
            SELECT TOP 5 TABLE_SCHEMA + '.' + TABLE_NAME as TableName
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = cursor.fetchall()
        if tables:
            print(f"📋 Sample tables:")
            for table in tables:
                print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Database connection failed!")
        print(f"   Error: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Verify SQL Server is running")
        print("   2. Check server name and database name")
        print("   3. Verify credentials (username/password)")
        print("   4. Check firewall settings")
        print("   5. Ensure ODBC Driver 17 is installed")
        return False

def test_llama_connection():
    """Test local Llama server connection"""
    print("\n" + "="*60)
    print("🤖 Testing Llama Server Connection")
    print("="*60)
    
    print(f"🌐 Server URL: {LLAMA_CONFIG['base_url']}")
    print(f"🔧 Model: {LLAMA_CONFIG['model']}")
    
    try:
        # Try Ollama format
        print("\n⏳ Testing Ollama API format...")
        ollama_payload = {
            "model": LLAMA_CONFIG['model'],
            "prompt": "Say 'OK' if you're working",
            "stream": False
        }
        
        response = requests.post(
            f"{LLAMA_CONFIG['base_url']}/api/generate",
            json=ollama_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get('response', 'No response')
            print("✅ Llama server connection successful!")
            print(f"📝 Test response: {llm_response[:100]}")
            return True
        
        # Try OpenAI-compatible format
        print("\n⏳ Trying OpenAI-compatible API format...")
        openai_payload = {
            "model": LLAMA_CONFIG['model'],
            "messages": [{"role": "user", "content": "Say 'OK' if you're working"}]
        }
        
        response = requests.post(
            f"{LLAMA_CONFIG['base_url']}/v1/chat/completions",
            json=openai_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result['choices'][0]['message']['content']
            print("✅ Llama server connection successful!")
            print(f"📝 Test response: {llm_response[:100]}")
            return True
        
        print(f"❌ Llama server connection failed!")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Llama server!")
        print(f"   Server URL: {LLAMA_CONFIG['base_url']}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure Ollama is running: 'ollama serve'")
        print("   2. Or start your LLM server with API enabled")
        print("   3. Check the LLAMA_SERVER_URL in .env file")
        print("   4. Verify firewall settings")
        return False
        
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out!")
        print("   The server is taking too long to respond")
        print("\n💡 Troubleshooting tips:")
        print("   1. Use a smaller/faster model")
        print("   2. Check server resources (CPU/RAM)")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_llama_model():
    """Test if the specified model is available"""
    print("\n" + "="*60)
    print("🔍 Checking Model Availability")
    print("="*60)
    
    try:
        # Try to list available models (Ollama)
        response = requests.get(
            f"{LLAMA_CONFIG['base_url']}/api/tags",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            models = result.get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            print(f"📦 Available models:")
            for name in model_names:
                if name:
                    status = "✓" if LLAMA_CONFIG['model'] in name else " "
                    print(f"   [{status}] {name}")
            
            if any(LLAMA_CONFIG['model'] in name for name in model_names):
                print(f"\n✅ Model '{LLAMA_CONFIG['model']}' is available!")
                return True
            else:
                print(f"\n⚠️  Model '{LLAMA_CONFIG['model']}' not found!")
                print(f"\n💡 To download the model, run:")
                print(f"   ollama pull {LLAMA_CONFIG['model']}")
                return False
        
    except Exception as e:
        print(f"⚠️  Could not check model availability: {str(e)}")
        return None

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 SQL RAG System - Connection Tests")
    print("="*60)
    
    db_ok = test_database_connection()
    llama_ok = test_llama_connection()
    
    if llama_ok:
        test_llama_model()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    print(f"Database Connection: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"Llama Server Connection: {'✅ PASS' if llama_ok else '❌ FAIL'}")
    print("="*60)
    
    if db_ok and llama_ok:
        print("\n🎉 All tests passed! You're ready to start the servers.")
        print("\n📝 Next steps:")
        print("   1. Start backend: python app.py")
        print("   2. Start frontend: npm start (in frontend directory)")
        print("   3. Open http://localhost:3000 in your browser")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before proceeding.")
    
    print()

if __name__ == "__main__":
    main()