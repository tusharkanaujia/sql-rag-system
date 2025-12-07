import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { Send, Database, Grid, BarChart3, MessageCircle, Copy, Download, Settings, CheckCircle, XCircle, RefreshCw, Sparkles } from 'lucide-react';
import Galaxy from './Galaxy';
import './Galaxy.css';

const API_BASE_URL = 'http://localhost:8000';

const DatabaseRAG = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [schema, setSchema] = useState(null);
  const [tables, setTables] = useState([]);
  const [llamaStatus, setLlamaStatus] = useState(null);
  const [activeTab, setActiveTab] = useState('chat');

  useEffect(() => {
    fetchSchema();
    fetchTables();
    checkLlamaStatus();
  }, []);

  const checkLlamaStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/llama-status`);
      const data = await response.json();
      setLlamaStatus(data);
    } catch (err) {
      setLlamaStatus({
        status: 'error',
        error: 'Failed to connect to backend server'
      });
    }
  };

  const fetchSchema = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/schema`);
      const data = await response.json();
      setSchema(data.schema);
    } catch (err) {
      console.error('Failed to fetch schema:', err);
    }
  };

  const fetchTables = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tables`);
      const data = await response.json();
      setTables(data.tables);
    } catch (err) {
      console.error('Failed to fetch tables:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: query,
          conversation_history: conversationHistory.slice(-5)
        }),
      });

      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data);
        setConversationHistory([...conversationHistory, {
          question: query,
          answer: data.explanation,
          sql: data.sql_query,
          timestamp: new Date().toISOString()
        }]);
      }
      
      setQuery('');
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const downloadCSV = (data) => {
    if (!data || data.length === 0) return;
    
    const headers = Object.keys(data[0]);
    const csvContent = [
      headers.join(','),
      ...data.map(row => headers.map(header => 
        JSON.stringify(row[header] || '')
      ).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'query_results.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const renderChart = (data, chartConfig) => {
    if (!chartConfig || !data || data.length === 0) return null;

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

    switch (chartConfig.type) {
      case 'bar':
        return (
          <div className="mt-6 bg-white/90 backdrop-blur-sm p-4 rounded-lg border border-white/20 shadow-xl">
            <h3 className="text-lg font-semibold mb-4 text-gray-800">{chartConfig.title}</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={chartConfig.x_axis} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey={chartConfig.y_axis} fill="#0088FE" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        );
        
      case 'line':
        return (
          <div className="mt-6 bg-white/90 backdrop-blur-sm p-4 rounded-lg border border-white/20 shadow-xl">
            <h3 className="text-lg font-semibold mb-4 text-gray-800">{chartConfig.title}</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={chartConfig.x_axis} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey={chartConfig.y_axis} stroke="#0088FE" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        );
        
      case 'pie':
        return (
          <div className="mt-6 bg-white/90 backdrop-blur-sm p-4 rounded-lg border border-white/20 shadow-xl">
            <h3 className="text-lg font-semibold mb-4 text-gray-800">{chartConfig.title}</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey={chartConfig.y_axis}
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        );
        
      default:
        return null;
    }
  };

  const renderTable = (data) => {
    if (!data || data.length === 0) return <p className="text-gray-500">No data to display</p>;

    const headers = Object.keys(data[0]);
    
    return (
      <div className="mt-4 overflow-x-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Query Results ({data.length} rows)</h3>
          <button
            onClick={() => downloadCSV(data)}
            className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition shadow-lg"
          >
            <Download size={16} />
            Download CSV
          </button>
        </div>
        <div className="bg-white/90 backdrop-blur-sm rounded-lg border border-white/20 shadow-xl overflow-hidden">
          <table className="min-w-full">
            <thead className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
              <tr>
                {headers.map((header) => (
                  <th key={header} className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data.slice(0, 100).map((row, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white/50' : 'bg-blue-50/50'}>
                  {headers.map((header) => (
                    <td key={header} className="px-4 py-3 text-sm text-gray-900">
                      {row[header] !== null && row[header] !== undefined ? String(row[header]) : 'NULL'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {data.length > 100 && (
          <p className="text-sm text-gray-300 mt-2">Showing first 100 rows of {data.length} total rows</p>
        )}
      </div>
    );
  };

  const renderConversationHistory = () => (
    <div className="space-y-4 max-h-96 overflow-y-auto">
      {conversationHistory.length === 0 ? (
        <p className="text-gray-300 text-center py-8">No conversation history yet. Start asking questions!</p>
      ) : (
        conversationHistory.map((item, index) => (
          <div key={index} className="border border-white/20 rounded-lg p-4 bg-white/90 backdrop-blur-sm shadow-xl">
            <div className="font-medium text-blue-600 mb-2">
              <MessageCircle className="inline mr-2" size={16} />
              Q: {item.question}
            </div>
            <div className="text-gray-700 mb-2 ml-6">A: {item.answer}</div>
            <div className="text-xs text-gray-500 bg-gray-100/80 p-2 rounded ml-6">
              <strong>SQL:</strong> <code>{item.sql}</code>
            </div>
            <div className="text-xs text-gray-400 mt-2 ml-6">
              {new Date(item.timestamp).toLocaleString()}
            </div>
          </div>
        ))
      )}
    </div>
  );

  const renderSchema = () => (
    <div className="space-y-4 max-h-96 overflow-y-auto">
      {schema && Object.entries(schema).map(([tableName, columns]) => (
        <div key={tableName} className="border border-white/20 rounded-lg p-4 bg-white/90 backdrop-blur-sm shadow-xl">
          <h3 className="font-semibold text-blue-600 mb-2 flex items-center">
            <Grid className="mr-2" size={16} />
            {tableName}
          </h3>
          <div className="grid grid-cols-1 gap-1 ml-6">
            {columns.map((col, index) => (
              <div key={index} className="text-sm">
                <span className="font-mono font-medium">{col.column}</span>
                <span className="text-gray-500"> ({col.type})</span>
                {col.nullable === 'NO' && <span className="text-red-500 text-xs ml-2">NOT NULL</span>}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Galaxy Background */}
      <div className="fixed inset-0 z-0" style={{ width: '100vw', height: '100vh' }}>
        <Galaxy
          focal={[0.5, 0.5]}
          rotation={[1.0, 0.0]}
          starSpeed={0.5}
          density={1.2}
          hueShift={240}
          speed={1.0}
          mouseInteraction={true}
          glowIntensity={0.5}
          saturation={0.8}
          mouseRepulsion={true}
          twinkleIntensity={0.3}
          rotationSpeed={0.05}
          repulsionStrength={2}
          autoCenterRepulsion={0}
          transparent={true}
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 p-4 min-h-screen">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white/10 backdrop-blur-md rounded-xl shadow-2xl overflow-hidden border border-white/20">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600/80 to-indigo-600/80 backdrop-blur-sm text-white p-6 border-b border-white/20">
              <h1 className="text-3xl font-bold flex items-center gap-3">
                <Database size={32} />
                Database RAG Assistant
                <Sparkles size={24} className="animate-pulse" />
              </h1>
              <p className="mt-2 opacity-90">Ask questions about your SQL Server database in natural language</p>
            </div>

            {/* Navigation */}
            <div className="bg-white/5 backdrop-blur-sm border-b border-white/10">
              <nav className="flex space-x-8 px-6">
                <button
                  onClick={() => setActiveTab('chat')}
                  className={`py-3 px-1 border-b-2 font-medium text-sm transition ${
                    activeTab === 'chat' 
                      ? 'border-blue-400 text-blue-300' 
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  <MessageCircle className="inline mr-2" size={16} />
                  Chat
                </button>
                <button
                  onClick={() => setActiveTab('schema')}
                  className={`py-3 px-1 border-b-2 font-medium text-sm transition ${
                    activeTab === 'schema' 
                      ? 'border-blue-400 text-blue-300' 
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  <Grid className="inline mr-2" size={16} />
                  Schema
                </button>
                <button
                  onClick={() => setActiveTab('history')}
                  className={`py-3 px-1 border-b-2 font-medium text-sm transition ${
                    activeTab === 'history' 
                      ? 'border-blue-400 text-blue-300' 
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  <BarChart3 className="inline mr-2" size={16} />
                  History
                </button>
                <button
                  onClick={() => setActiveTab('status')}
                  className={`py-3 px-1 border-b-2 font-medium text-sm transition ${
                    activeTab === 'status' 
                      ? 'border-blue-400 text-blue-300' 
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  <Settings className="inline mr-2" size={16} />
                  Status
                </button>
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'chat' && (
                <>
                  {/* Query Input */}
                  <div className="mb-6">
                    <div className="flex gap-4">
                      <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Ask a question... (e.g., 'Show me top 10 customers by revenue')"
                        className="flex-1 px-4 py-3 bg-white/90 backdrop-blur-sm border border-white/30 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent outline-none shadow-lg text-gray-900"
                        disabled={loading}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit(e);
                          }
                        }}
                      />
                      <button
                        onClick={handleSubmit}
                        disabled={loading || !query.trim()}
                        className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition shadow-lg"
                      >
                        {loading ? (
                          <>
                            <RefreshCw className="animate-spin" size={16} />
                            Processing...
                          </>
                        ) : (
                          <>
                            <Send size={16} />
                            Ask
                          </>
                        )}
                      </button>
                    </div>
                    <p className="text-xs text-gray-300 mt-2">
                      💡 Try: "Show me all tables", "Count rows in users table", "Top 5 sales by amount"
                    </p>
                  </div>

                  {/* Error Display */}
                  {error && (
                    <div className="mb-4 p-4 bg-red-500/20 backdrop-blur-sm border border-red-500/50 rounded-lg text-red-100 shadow-lg">
                      <strong>Error:</strong> {error}
                    </div>
                  )}

                  {/* Results */}
                  {results && (
                    <div className="space-y-6">
                      {/* Explanation */}
                      <div className="bg-blue-500/20 backdrop-blur-sm border border-blue-400/30 rounded-lg p-4 shadow-xl">
                        <h3 className="font-semibold text-blue-200 mb-2">Query Explanation:</h3>
                        <p className="text-blue-100">{results.explanation}</p>
                      </div>

                      {/* SQL Query */}
                      {results.sql_query && (
                        <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-4 shadow-xl">
                          <div className="flex justify-between items-center mb-2">
                            <h3 className="font-semibold text-gray-200">Generated SQL:</h3>
                            <button
                              onClick={() => copyToClipboard(results.sql_query)}
                              className="flex items-center gap-1 text-sm text-blue-300 hover:text-blue-100 transition"
                            >
                              <Copy size={14} />
                              Copy
                            </button>
                          </div>
                          <pre className="text-sm bg-black/30 text-green-300 p-3 rounded border border-white/10 overflow-x-auto">
                            <code>{results.sql_query}</code>
                          </pre>
                        </div>
                      )}

                      {/* Chart */}
                      {results.chart_config && renderChart(results.data, results.chart_config)}

                      {/* Data Table */}
                      {renderTable(results.data)}
                    </div>
                  )}
                </>
              )}

              {activeTab === 'schema' && (
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-semibold text-white">Database Schema</h2>
                    <span className="text-sm text-gray-300">{tables.length} tables</span>
                  </div>
                  {renderSchema()}
                </div>
              )}

              {activeTab === 'history' && (
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-semibold text-white">Conversation History</h2>
                    {conversationHistory.length > 0 && (
                      <button
                        onClick={() => setConversationHistory([])}
                        className="text-sm text-red-300 hover:text-red-100 transition"
                      >
                        Clear History
                      </button>
                    )}
                  </div>
                  {renderConversationHistory()}
                </div>
              )}

              {activeTab === 'status' && (
                <div>
                  <h2 className="text-xl font-semibold mb-4 text-white">System Status</h2>
                  
                  {/* Llama Server Status */}
                  <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-4 mb-4 shadow-xl">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-lg font-medium text-white">Local Llama Server</h3>
                      <button
                        onClick={checkLlamaStatus}
                        className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition shadow-lg"
                      >
                        <RefreshCw className="inline mr-1" size={14} />
                        Refresh
                      </button>
                    </div>
                    
                    {llamaStatus ? (
                      <div className="space-y-3">
                        <div className="flex items-center gap-2">
                          {llamaStatus.status === 'connected' ? (
                            <CheckCircle className="text-green-400" size={20} />
                          ) : (
                            <XCircle className="text-red-400" size={20} />
                          )}
                          <span className={`font-medium ${
                            llamaStatus.status === 'connected' ? 'text-green-300' : 'text-red-300'
                          }`}>
                            {llamaStatus.status === 'connected' ? 'Connected' : 'Disconnected'}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                          <div>
                            <strong className="text-gray-300">Server URL:</strong>
                            <div className="font-mono text-blue-300">{llamaStatus.server_url}</div>
                          </div>
                          <div>
                            <strong className="text-gray-300">Model:</strong>
                            <div className="font-mono text-blue-300">{llamaStatus.model}</div>
                          </div>
                        </div>
                        
                        {llamaStatus.test_response && (
                          <div>
                            <strong className="text-gray-300">Test Response:</strong>
                            <div className="bg-black/30 text-green-300 p-2 rounded mt-1 text-sm">
                              {llamaStatus.test_response}
                            </div>
                          </div>
                        )}
                        
                        {llamaStatus.error && (
                          <div className="bg-red-500/20 border border-red-500/50 rounded p-3">
                            <strong className="text-red-300">Error:</strong>
                            <div className="text-red-200 text-sm mt-1">{llamaStatus.error}</div>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="text-gray-300">Checking server status...</div>
                    )}
                  </div>

                  {/* Database Status */}
                  <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg p-4 mb-4 shadow-xl">
                    <h3 className="text-lg font-medium mb-3 text-white">Database Connection</h3>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        {schema ? (
                          <CheckCircle className="text-green-400" size={20} />
                        ) : (
                          <XCircle className="text-red-400" size={20} />
                        )}
                        <span className={`font-medium ${
                          schema ? 'text-green-300' : 'text-red-300'
                        }`}>
                          {schema ? 'Connected' : 'Not Connected'}
                        </span>
                      </div>
                      
                      {schema && (
                        <div className="text-sm">
                          <strong className="text-gray-300">Available Tables:</strong>
                          <div className="text-blue-300">{tables.length} tables found</div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Configuration Guide */}
                  <div className="bg-blue-500/10 backdrop-blur-sm border border-blue-400/30 rounded-lg p-4 shadow-xl">
                    <h3 className="text-lg font-medium text-blue-200 mb-3">Configuration Guide</h3>
                    <div className="text-sm text-blue-100 space-y-2">
                      <p><strong>For Ollama:</strong> Make sure Ollama is running on port 11434</p>
                      <p className="ml-4 font-mono text-green-300">ollama serve</p>
                      <p><strong>For text-generation-webui:</strong> Start with --api flag</p>
                      <p className="ml-4 font-mono text-green-300">python server.py --api --listen</p>
                      <p><strong>Environment Variables in backend/.env:</strong></p>
                      <ul className="list-disc list-inside ml-4 space-y-1 font-mono text-xs text-gray-300">
                        <li>LLAMA_SERVER_URL=http://localhost:11434</li>
                        <li>LLAMA_MODEL=llama3.1</li>
                        <li>DB_SERVER=localhost</li>
                        <li>DB_DATABASE=your_database</li>
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatabaseRAG;