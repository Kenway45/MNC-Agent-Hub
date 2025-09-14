from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import re
import requests
from datetime import datetime
import uuid
import logging

# MCP Integration
from mcp_integration import MCPIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MNC Agent Hub", description="Enterprise Document Management System with MCP Integration")

# Sample document database
DOCS = {
    "doc_001": {
        "id": "doc_001",
        "title": "Employee Handbook",
        "category": "handbook",
        "text": "Welcome to MNC Corporation. This handbook outlines company policies, procedures, and guidelines for all employees. Our company values include integrity, innovation, and collaboration. We provide comprehensive benefits including health insurance, retirement plans, and professional development opportunities.",
        "tags": ["hr", "policy", "benefits", "guidelines"],
        "uploaded_at": "2024-01-15T10:00:00Z",
        "uploaded_by": "admin"
    },
    "doc_002": {
        "id": "doc_002", 
        "title": "IT Security Policy",
        "category": "policy",
        "text": "All employees must follow strict security protocols. Use strong passwords, enable two-factor authentication, and never share login credentials. Report any suspicious activities immediately. All company data must be encrypted and backed up regularly.",
        "tags": ["security", "policy", "it", "compliance"],
        "uploaded_at": "2024-01-20T14:30:00Z",
        "uploaded_by": "admin"
    },
    "doc_003": {
        "id": "doc_003",
        "title": "Remote Work Guidelines", 
        "category": "guideline",
        "text": "Remote work is supported with proper equipment and guidelines. Employees must maintain regular communication, attend virtual meetings, and ensure secure internet connections. Work hours should align with team collaboration needs.",
        "tags": ["remote", "work", "guidelines", "policy"],
        "uploaded_at": "2024-02-01T09:15:00Z",
        "uploaded_by": "admin"
    }
}

# Employee activity log
EMPLOYEE_LOG = []

# Initialize MCP Integration
mcp_integration = MCPIntegration(app)
mcp_integration.setup_integration(DOCS, EMPLOYEE_LOG)

# Start MCP server on application startup
@app.on_event("startup")
async def startup_event():
    """Start MCP server when main app starts"""
    logger.info("Starting MCP server integration...")
    mcp_integration.start_mcp_server()
    logger.info("MNC Agent Hub with MCP server ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop MCP server when main app shuts down"""
    logger.info("Shutting down MCP server...")
    mcp_integration.stop_mcp_server()

class DocumentUpload(BaseModel):
    title: str
    content: str
    category: str
    uploaded_by: str = "admin"
    tags: Optional[List[str]] = []

class EmployeeQuery(BaseModel):
    employee_id: str
    query: str
    query_type: str
    doc_id: Optional[str] = None

def call_ollama_for_json(prompt: str, model: str = "deepseek-coder:6.7b"):
    try:
        r = requests.post("http://localhost:11434/api/generate",
                         json={"model": model, "prompt": prompt, "stream": False})
        if r.status_code != 200:
            return {"summary": "AI service unavailable", "action_items": []}
        raw = r.text
    except:
        raw = '{"summary": "AI service unavailable", "action_items": []}'
    
    m = re.search(r"(\{.*\})", str(raw), flags=re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    return {"summary": str(raw), "action_items": []}

@app.get("/summarize/{doc_id}")
async def summarize(doc_id: str, max_sentences: int = 3, model: str = "deepseek-coder:6.7b"):
    if doc_id not in DOCS:
        raise HTTPException(status_code=404, detail="doc not found")
    text = DOCS[doc_id]["text"]
    prompt = (f"You MUST respond ONLY with valid JSON with two fields: "
              f'{{"summary": "<concise summary>", "action_items": ["item1","item2"]}}. '
              f"Summary should be concise and up to {max_sentences} sentences. Document:\\n\\n{text}")
    resp_json = call_ollama_for_json(prompt, model=model)
    return {"summary": resp_json.get("summary", "") if isinstance(resp_json, dict) else str(resp_json),
            "action_items": resp_json.get("action_items", []) if isinstance(resp_json, dict) else []}

# Main Entry Page - Agent Hub
@app.get("/", response_class=HTMLResponse)
async def agent_hub():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent Hub</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f5f5;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .hub-container {
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 40px;
                text-align: center;
                max-width: 500px;
                width: 90%;
            }
            
            .hub-title {
                color: #333;
                font-size: 2.5em;
                font-weight: 300;
                margin-bottom: 10px;
            }
            
            .hub-subtitle {
                color: #666;
                font-size: 1.1em;
                margin-bottom: 40px;
            }
            
            .access-options {
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .access-card {
                flex: 1;
                background: #fafafa;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 30px 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
            }
            
            .access-card:hover {
                border-color: #4CAF50;
                background: #f8fff8;
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            
            .access-card.admin:hover {
                border-color: #2196F3;
                background: #f8fbff;
            }
            
            .access-card h3 {
                color: #333;
                font-size: 1.4em;
                font-weight: 500;
                margin-bottom: 10px;
            }
            
            .access-card p {
                color: #666;
                font-size: 0.95em;
                line-height: 1.4;
            }
            
            .employee-form {
                display: none;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
            }
            
            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }
            
            label {
                display: block;
                color: #333;
                font-weight: 500;
                margin-bottom: 8px;
            }
            
            input {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 4px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            
            input:focus {
                outline: none;
                border-color: #4CAF50;
            }
            
            .btn {
                background: #4CAF50;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            
            .btn:hover {
                background: #45a049;
                transform: translateY(-1px);
            }
            
            .btn.admin {
                background: #2196F3;
            }
            
            .btn.admin:hover {
                background: #1976D2;
            }
            
            .back-btn {
                background: #666;
                font-size: 14px;
                padding: 8px 16px;
                margin-right: 10px;
            }
            
            .back-btn:hover {
                background: #555;
            }
            
            @media (max-width: 600px) {
                .access-options {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="hub-container">
            <h1 class="hub-title">Agent Hub</h1>
            <p class="hub-subtitle">Choose your access level</p>
            
            <div class="access-options">
                <div class="access-card" onclick="showEmployeeForm()">
                    <h3>Employee Access</h3>
                    <p>Browse documents, search content, and get AI-powered assistance</p>
                </div>
                
                <div class="access-card admin" onclick="goToAdmin()">
                    <h3>Admin Access</h3>
                    <p>Manage documents, view analytics, and monitor employee activity</p>
                </div>
            </div>
            
            <div class="employee-form" id="employeeForm">
                <div class="form-group">
                    <label for="employeeId">Employee ID</label>
                    <input type="text" id="employeeId" placeholder="Enter your Employee ID" required>
                </div>
                <button class="btn back-btn" onclick="hideEmployeeForm()">Back</button>
                <button class="btn" onclick="goToEmployee()">Enter Portal</button>
            </div>
        </div>
        
        <script>
            function showEmployeeForm() {
                document.querySelector('.access-options').style.display = 'none';
                document.getElementById('employeeForm').style.display = 'block';
                document.getElementById('employeeId').focus();
            }
            
            function hideEmployeeForm() {
                document.querySelector('.access-options').style.display = 'flex';
                document.getElementById('employeeForm').style.display = 'none';
                document.getElementById('employeeId').value = '';
            }
            
            function goToEmployee() {
                const employeeId = document.getElementById('employeeId').value.trim();
                
                if (!employeeId) {
                    alert('Please enter your Employee ID');
                    return;
                }
                
                if (employeeId.length < 3) {
                    alert('Employee ID must be at least 3 characters');
                    return;
                }
                
                window.location.href = `/employee/${employeeId}`;
            }
            
            function goToAdmin() {
                window.location.href = '/admin';
            }
            
            // Handle Enter key in employee ID field
            document.addEventListener('DOMContentLoaded', function() {
                document.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && document.getElementById('employeeForm').style.display !== 'none') {
                        goToEmployee();
                    }
                });
            });
        </script>
    </body>
    </html>
    """

# Employee Portal (after login)
@app.get("/employee/{employee_id}", response_class=HTMLResponse)
async def employee_portal(employee_id: str):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent Hub - Employee Portal</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0; 
                padding: 20px; 
                background: #f5f5f5;
                min-height: 100vh;
            }}
            
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 8px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .header {{ 
                background: #4CAF50;
                color: white; 
                padding: 30px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center;
            }}
            
            h1 {{ 
                color: white; 
                margin: 0; 
                font-size: 2em;
                font-weight: 500;
            }}
            
            .employee-info {{ 
                background: rgba(255, 255, 255, 0.2); 
                padding: 10px 20px; 
                border-radius: 20px;
            }}
            
            .section {{ 
                margin: 0; 
                padding: 30px; 
                border-bottom: 1px solid #e0e0e0;
            }}
            
            .section:last-child {{
                border-bottom: none;
            }}
            
            .section h3 {{ 
                color: #333;
                font-size: 1.3em;
                font-weight: 500;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #4CAF50;
            }}
            
            input, select, textarea {{ 
                width: 100%; 
                padding: 12px 16px; 
                border: 2px solid #e0e0e0; 
                border-radius: 4px; 
                font-size: 14px; 
                margin-bottom: 15px;
                transition: border-color 0.3s ease;
            }}
            
            input:focus, select:focus, textarea:focus {{
                outline: none;
                border-color: #4CAF50;
            }}
            
            button {{ 
                background: #4CAF50; 
                color: white; 
                padding: 12px 24px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 14px; 
                font-weight: 500;
                transition: all 0.3s ease;
            }}
            
            button:hover {{ 
                background: #45a049;
                transform: translateY(-1px);
            }}
            
            .document-card {{ 
                background: white; 
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 4px; 
                border: 1px solid #e0e0e0;
                transition: all 0.3s ease;
            }}
            
            .document-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                border-color: #4CAF50;
            }}
            
            .document-card h4 {{
                color: #333;
                margin-bottom: 10px;
                font-weight: 500;
            }}
            
            .results {{ 
                margin-top: 20px; 
                padding: 20px; 
                background: #f8f9fa; 
                border-radius: 4px; 
                border-left: 4px solid #4CAF50;
            }}
            
            .loading {{ 
                display: none; 
                color: #666; 
                font-style: italic;
                text-align: center;
                padding: 15px;
                background: #f0f0f0;
                border-radius: 4px;
                margin: 10px 0;
            }}
            
            .tag {{ 
                background: #e8f5e8; 
                padding: 3px 8px; 
                border-radius: 12px; 
                font-size: 11px; 
                color: #2e7d2e; 
                margin-right: 5px;
                border: 1px solid #c8e6c8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>Agent Hub - Employee Portal</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Document Management System</p>
                </div>
                <div class="employee-info">
                    <strong>Employee: {employee_id}</strong>
                    <br><a href="/" style="color: white; text-decoration: none; font-size: 12px;">← Back to Home</a>
                </div>
            </div>
            
            <div class="section">
                <h3>Available Documents</h3>
                <button onclick="loadDocuments()">Refresh Documents</button>
                <div id="documentsResult"></div>
            </div>
            
            <div class="section">
                <h3>Search Documents</h3>
                <input type="text" id="searchQuery" placeholder="Search documents (e.g., compliance, privacy, roadmap)">
                <button onclick="searchDocuments()">Search</button>
                <div class="loading" id="searchLoading">Searching documents...</div>
                <div id="searchResults"></div>
            </div>
            
            <div class="section">
                <h3>Get Document Summary</h3>
                <input type="text" id="docIdSummary" placeholder="Document ID (e.g., doc_001)">
                <select id="maxSentences">
                    <option value="2">Short (2 sentences)</option>
                    <option value="3">Medium (3 sentences)</option>
                    <option value="5">Long (5 sentences)</option>
                </select>
                <button onclick="getSummary()">Get AI Summary</button>
                <div class="loading" id="summaryLoading">Generating summary...</div>
                <div id="summaryResults"></div>
            </div>
            
            <div class="section">
                <h3>Ask a Question</h3>
                <textarea id="questionText" rows="3" placeholder="Ask any question about company documents..."></textarea>
                <button onclick="askQuestion()">Ask Question</button>
                <div class="loading" id="questionLoading">Processing question...</div>
                <div id="questionResults"></div>
            </div>
            
            <div class="section">
                <h3>My Activity History</h3>
                <button onclick="loadHistory()">View My History</button>
                <div id="historyResults"></div>
            </div>
        </div>
        
        <script>
            const API_BASE = window.location.origin;
            const EMPLOYEE_ID = "{employee_id}";
            
            // Auto-load documents on page load
            window.addEventListener('load', loadDocuments);
            
            async function loadDocuments() {{
                try {{
                    const response = await fetch(`${{API_BASE}}/documents`);
                    const documents = await response.json();
                    
                    let html = '<div style="margin-top: 15px;">';
                    documents.forEach(doc => {{
                        html += `
                            <div class="document-card">
                                <h4>${{doc.title}}</h4>
                                <p><strong>ID:</strong> ${{doc.id}}</p>
                                <div>${{doc.tags.map(tag => `<span class="tag">${{tag}}</span>`).join('')}}</div>
                                <button onclick="getSummaryForDoc('${{doc.id}}')" style="margin-top: 10px;">Get Summary</button>
                            </div>
                        `;
                    }});
                    html += '</div>';
                    
                    document.getElementById('documentsResult').innerHTML = html;
                }} catch (error) {{
                    document.getElementById('documentsResult').innerHTML = `<div style="color: red;">Error loading documents: ${{error.message}}</div>`;
                }}
            }}
            
            async function searchDocuments() {{
                const query = document.getElementById('searchQuery').value.trim();
                if (!query) {{
                    alert('Please enter a search query!');
                    return;
                }}
                
                document.getElementById('searchLoading').style.display = 'block';
                document.getElementById('searchResults').innerHTML = '';
                
                try {{
                    const response = await fetch(`${{API_BASE}}/employee/query`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            employee_id: EMPLOYEE_ID,
                            query: query,
                            query_type: 'search'
                        }})
                    }});
                    
                    const result = await response.json();
                    
                    let html = '<div class="results"><h4>Search Results:</h4>';
                    if (result.response && result.response.length > 0) {{
                        result.response.forEach(doc => {{
                            html += `
                                <div class="document-card">
                                    <h4>${{doc.title}}</h4>
                                    <p><strong>ID:</strong> ${{doc.id}} | <strong>Relevance:</strong> ${{doc.score}}</p>
                                    <div>${{doc.tags.map(tag => `<span class="tag">${{tag}}</span>`).join('')}}</div>
                                </div>
                            `;
                        }});
                    }} else {{
                        html += '<p>No matching documents found.</p>';
                    }}
                    html += '</div>';
                    
                    document.getElementById('searchResults').innerHTML = html;
                }} catch (error) {{
                    document.getElementById('searchResults').innerHTML = `<div style="color: red;">Search failed: ${{error.message}}</div>`;
                }} finally {{
                    document.getElementById('searchLoading').style.display = 'none';
                }}
            }}
            
            async function getSummary() {{
                const docId = document.getElementById('docIdSummary').value.trim();
                const maxSentences = document.getElementById('maxSentences').value;
                
                if (!docId) {{
                    alert('Please enter a document ID!');
                    return;
                }}
                
                document.getElementById('summaryLoading').style.display = 'block';
                document.getElementById('summaryResults').innerHTML = '';
                
                try {{
                    const response = await fetch(`${{API_BASE}}/summarize/${{docId}}?max_sentences=${{maxSentences}}`);
                    const result = await response.json();
                    
                    let html = '<div class="results">';
                    html += `<h4>Summary for ${{docId}}:</h4>`;
                    html += `<p><strong>Summary:</strong> ${{result.summary}}</p>`;
                    if (result.action_items && result.action_items.length > 0) {{
                        html += '<p><strong>Key Points:</strong></p><ul>';
                        result.action_items.forEach(item => {{
                            html += `<li>${{item}}</li>`;
                        }});
                        html += '</ul>';
                    }}
                    html += '</div>';
                    
                    document.getElementById('summaryResults').innerHTML = html;
                }} catch (error) {{
                    document.getElementById('summaryResults').innerHTML = `<div style="color: red;">Summary failed: ${{error.message}}</div>`;
                }} finally {{
                    document.getElementById('summaryLoading').style.display = 'none';
                }}
            }}
            
            function getSummaryForDoc(docId) {{
                document.getElementById('docIdSummary').value = docId;
                getSummary();
            }}
            
            async function askQuestion() {{
                const question = document.getElementById('questionText').value.trim();
                if (!question) {{
                    alert('Please enter a question!');
                    return;
                }}
                
                document.getElementById('questionLoading').style.display = 'block';
                document.getElementById('questionResults').innerHTML = '';
                
                try {{
                    const response = await fetch(`${{API_BASE}}/employee/query`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            employee_id: EMPLOYEE_ID,
                            query: question,
                            query_type: 'question'
                        }})
                    }});
                    
                    const result = await response.json();
                    
                    let html = '<div class="results">';
                    html += `<h4>Answer:</h4>`;
                    html += `<p>${{result.response}}</p>`;
                    html += '</div>';
                    
                    document.getElementById('questionResults').innerHTML = html;
                }} catch (error) {{
                    document.getElementById('questionResults').innerHTML = `<div style="color: red;">Question failed: ${{error.message}}</div>`;
                }} finally {{
                    document.getElementById('questionLoading').style.display = 'none';
                }}
            }}
            
            async function loadHistory() {{
                try {{
                    const response = await fetch(`${{API_BASE}}/employee/${{EMPLOYEE_ID}}/history`);
                    const history = await response.json();
                    
                    let html = '<div class="results"><h4>My Activity History:</h4>';
                    if (history.length > 0) {{
                        history.forEach(item => {{
                            html += `
                                <div style="padding: 10px; margin: 10px 0; background: #f0f0f0; border-radius: 4px;">
                                    <p><strong>${{item.query_type.toUpperCase()}}:</strong> ${{item.query}}</p>
                                    <small>${{new Date(item.timestamp).toLocaleString()}}</small>
                                </div>
                            `;
                        }});
                    }} else {{
                        html += '<p>No activity history found.</p>';
                    }}
                    html += '</div>';
                    
                    document.getElementById('historyResults').innerHTML = html;
                }} catch (error) {{
                    document.getElementById('historyResults').innerHTML = `<div style="color: red;">Failed to load history: ${{error.message}}</div>`;
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.get("/documents")
async def get_documents():
    return list(DOCS.values())

@app.post("/employee/query")
async def employee_query(query: EmployeeQuery):
    # Log the query
    log_entry = {
        "query_id": str(uuid.uuid4()),
        "employee_id": query.employee_id,
        "query": query.query,
        "query_type": query.query_type,
        "doc_id": query.doc_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    EMPLOYEE_LOG.append(log_entry)
    
    if query.query_type == "search":
        # Search documents by keywords
        results = []
        search_terms = query.query.lower().split()
        
        for doc in DOCS.values():
            score = 0
            text_lower = (doc["title"] + " " + doc["text"] + " " + " ".join(doc["tags"])).lower()
            
            for term in search_terms:
                if term in text_lower:
                    score += text_lower.count(term)
            
            if score > 0:
                results.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "score": score,
                    "tags": doc["tags"]
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return {"response": results}
    
    elif query.query_type == "question":
        # Use AI to answer questions
        context = ""
        for doc in DOCS.values():
            context += f"Document {doc['id']}: {doc['title']}\\n{doc['text']}\\n\\n"
        
        prompt = f"Answer this question based on the company documents: {query.query}\\n\\nDocuments:\\n{context}"
        
        try:
            r = requests.post("http://localhost:11434/api/generate",
                             json={"model": "deepseek-coder:6.7b", "prompt": prompt, "stream": False})
            if r.status_code == 200:
                return {"response": r.json().get("response", "AI service unavailable")}
        except:
            pass
        
        return {"response": "AI service is currently unavailable. Please try again later."}
    
    return {"response": "Query type not supported"}

@app.get("/employee/{employee_id}/history")
async def get_employee_history(employee_id: str):
    try:
        # Filter logs for specific employee
        history = [log for log in EMPLOYEE_LOG if log["employee_id"] == employee_id]
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Import admin functions
from admin_endpoints import (
    upload_document_endpoint,
    get_admin_stats_endpoint,
    get_all_documents_endpoint,
    get_employee_stats_endpoint,
    get_query_history_endpoint,
    get_analytics_endpoint
)

# Admin endpoints
@app.post("/admin/upload-document")
async def upload_document(doc: DocumentUpload):
    return await upload_document_endpoint(doc, DOCS)

@app.get("/admin/stats")
async def get_admin_stats():
    return await get_admin_stats_endpoint(DOCS, EMPLOYEE_LOG)

@app.get("/admin/documents")
async def get_all_documents():
    return await get_all_documents_endpoint(DOCS)

@app.get("/admin/employee-stats")
async def get_employee_stats():
    return await get_employee_stats_endpoint(EMPLOYEE_LOG)

@app.get("/admin/query-history")
async def get_query_history(
    employee_id: Optional[str] = None,
    query_type: Optional[str] = None,
    date: Optional[str] = None
):
    return await get_query_history_endpoint(employee_id, query_type, date, EMPLOYEE_LOG)

@app.get("/admin/analytics")
async def get_analytics():
    return await get_analytics_endpoint(EMPLOYEE_LOG)

# Admin Dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    from admin_dashboard import get_admin_dashboard
    return get_admin_dashboard()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)