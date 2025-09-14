# 🤖 MCP (Model Context Protocol) Server Guide

## Overview

The MNC Agent Hub includes a fully integrated **MCP (Model Context Protocol) server** that provides standardized AI model communication for enterprise document management. This enables seamless integration with various AI clients and provides a robust foundation for AI-powered document operations.

## 🌟 What is MCP?

**Model Context Protocol (MCP)** is an open standard for connecting AI assistants with external data sources and tools. It provides:

- **Standardized Communication**: Consistent API interface across different AI models
- **Tool Integration**: Structured way to expose business logic as AI-callable tools
- **Resource Management**: Organized access to documents and data
- **Secure Context**: Controlled information sharing with AI models

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Clients    │◄──►│   MCP Server     │◄──►│  Agent Hub      │
│                 │    │                  │    │                 │
│ • Claude        │    │ • Tools          │    │ • Documents     │
│ • GPT           │    │ • Resources      │    │ • Analytics     │
│ • Local LLMs    │    │ • Prompts        │    │ • Employee Data │
│ • Custom Apps   │    │ • WebSocket/HTTP │    │ • Search Engine │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Server Details

### **Server Information**
- **Host**: `localhost`
- **Port**: `3001`
- **Protocol Version**: `2024-11-05`
- **WebSocket Endpoint**: `ws://localhost:3001/mcp`
- **HTTP Endpoint**: `http://localhost:3001/mcp/http`
- **Health Check**: `http://localhost:3001/health`

### **Capabilities**
- ✅ **Resources**: Access to company documents
- ✅ **Tools**: AI-callable business operations  
- ✅ **Prompts**: Pre-configured prompt templates
- ✅ **Completion**: Text generation capabilities
- ✅ **Logging**: Activity tracking and audit trails

## 🛠️ Available Tools

### 1. **search_documents**
Search through company documents using AI-powered relevance scoring.

```json
{
  "name": "search_documents",
  "arguments": {
    "query": "security policy",
    "employee_id": "emp_001",
    "max_results": 5
  }
}
```

**Response**: List of relevant documents with scores

### 2. **summarize_document**
Generate AI-powered summary of a specific document.

```json
{
  "name": "summarize_document", 
  "arguments": {
    "doc_id": "doc_001",
    "max_sentences": 3
  }
}
```

**Response**: Document summary with key points

### 3. **answer_question**
Answer questions about company documents using context-aware AI.

```json
{
  "name": "answer_question",
  "arguments": {
    "question": "What is our vacation policy?",
    "employee_id": "emp_001",
    "context_docs": ["doc_001", "doc_002"]
  }
}
```

**Response**: AI-generated answer based on document context

### 4. **get_analytics**
Get system analytics and employee activity data.

```json
{
  "name": "get_analytics",
  "arguments": {
    "metric_type": "system"
  }
}
```

**Response**: Analytics data (system/employee/documents/queries)

### 5. **auto_tag_document**
Automatically generate tags for a document using AI analysis.

```json
{
  "name": "auto_tag_document",
  "arguments": {
    "content": "This document outlines our security procedures...",
    "title": "Security Guidelines",
    "category": "policy"
  }
}
```

**Response**: Suggested tags with confidence scores

## 📚 Resources

The MCP server exposes company documents as resources:

- **URI Format**: `document://{doc_id}`
- **MIME Type**: `text/plain`
- **Access**: Read-only document content
- **Metadata**: Title, category, tags, upload date

### Example Resource Access
```json
{
  "method": "resources/read",
  "params": {
    "uri": "document://doc_001"
  }
}
```

## 🎯 Prompts

Pre-configured prompt templates for common operations:

### 1. **document_summary**
Comprehensive document summarization prompt.

### 2. **search_assistant** 
Help employees find relevant documents and information.

### 3. **compliance_check**
Check document compliance with company policies.

## 💻 Client Examples

### WebSocket Client (Python)

```python
import asyncio
import json
import websockets

async def mcp_client():
    uri = "ws://localhost:3001/mcp"
    
    async with websockets.connect(uri) as websocket:
        # Initialize connection
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "Agent Hub Client",
                    "version": "1.0.0"
                }
            }
        }
        
        await websocket.send(json.dumps(init_message))
        response = await websocket.recv()
        print("Server capabilities:", json.loads(response))
        
        # Search documents
        search_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "search_documents",
                "arguments": {
                    "query": "employee handbook",
                    "employee_id": "emp_001"
                }
            }
        }
        
        await websocket.send(json.dumps(search_message))
        response = await websocket.recv()
        print("Search results:", json.loads(response))

asyncio.run(mcp_client())
```

### HTTP Client (Python)

```python
import requests

# Search documents via HTTP
tool_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "search_documents",
        "arguments": {
            "query": "security policy",
            "employee_id": "emp_001"
        }
    }
}

response = requests.post(
    "http://localhost:3001/mcp/http",
    json=tool_request
)

result = response.json()
print("Search results:", result)
```

### cURL Example

```bash
# Test MCP server health
curl http://localhost:3001/health

# Call search tool
curl -X POST http://localhost:3001/mcp/http \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call", 
    "params": {
      "name": "search_documents",
      "arguments": {
        "query": "employee policy",
        "employee_id": "emp_001"
      }
    }
  }'
```

## 🔧 Integration with Agent Hub

The MCP server is automatically integrated with the main Agent Hub:

### **Automatic Startup**
- MCP server starts automatically with Agent Hub
- Runs on separate thread (port 3001)
- Shares document store and employee logs

### **Status Monitoring**
Check MCP server status:
```bash
curl http://localhost:8888/mcp/status
```

### **Tool Testing**
Test MCP tools through main app:
```bash
curl -X POST http://localhost:8888/mcp/test-tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "search_documents",
    "arguments": {
      "query": "handbook",
      "employee_id": "emp_001"
    }
  }'
```

## 🔍 Use Cases

### 1. **AI Assistant Integration**
- Connect Claude, GPT, or local LLMs to company documents
- Provide context-aware responses about policies and procedures
- Enable natural language document queries

### 2. **Custom Application Development**
- Build internal tools that leverage company knowledge
- Create chatbots with access to company information
- Develop workflow automation with document context

### 3. **Analytics and Reporting**
- Generate insights from employee document interactions
- Track popular documents and search patterns
- Monitor system usage and performance

### 4. **Content Management**
- Automatically tag and categorize documents
- Generate summaries and extract key information
- Maintain document organization and metadata

## 🚀 Getting Started

### 1. **Start the System**
```bash
./Agent_Hub.sh
```

### 2. **Verify MCP Server**
```bash
curl http://localhost:3001/health
```

### 3. **List Available Tools**
```python
import requests

response = requests.post(
    "http://localhost:3001/mcp/http",
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
)

print(response.json())
```

### 4. **Test Document Search**
```python
import requests

response = requests.post(
    "http://localhost:3001/mcp/http",
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "search_documents",
            "arguments": {
                "query": "employee handbook",
                "employee_id": "emp_001"
            }
        }
    }
)

print(response.json())
```

## 🔒 Security Considerations

- **Local Processing**: All AI operations run locally via Ollama
- **No External Calls**: No data leaves your infrastructure  
- **Employee Tracking**: All activities are logged with employee IDs
- **Access Control**: Tools require employee authentication
- **Audit Trail**: Complete logging of all MCP interactions

## 📊 Monitoring and Logging

### **Activity Logs**
All MCP operations are logged with:
- Employee ID
- Operation type
- Timestamp
- Query content
- Response metadata

### **Health Monitoring**
- Server health endpoint: `/health`
- Connection status: WebSocket client count
- Error tracking: Failed operations and reasons

### **Performance Metrics**
- Response times for each tool
- Document access patterns
- Popular queries and documents

## 🛡️ Error Handling

The MCP server implements comprehensive error handling:

### **Standard JSON-RPC Errors**
- `-32700`: Parse error
- `-32600`: Invalid Request  
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

### **Custom Error Codes**
- `404`: Document not found
- `500`: AI service unavailable
- `400`: Invalid employee ID

### **Graceful Degradation**
- Falls back to cached responses when AI is unavailable
- Continues serving documents even if summarization fails
- Maintains activity logging even during errors

## 📈 Future Enhancements

### **Planned Features**
- [ ] Multi-model support (GPT, Claude, Gemini)
- [ ] Advanced caching and performance optimization
- [ ] Real-time document sync with external systems
- [ ] Enhanced security with JWT authentication
- [ ] Streaming responses for large operations
- [ ] GraphQL-style query capabilities

### **Integration Opportunities**
- [ ] Slack/Teams bot integration
- [ ] Email system integration
- [ ] CRM and ERP system connections
- [ ] External knowledge base integration
- [ ] Multi-language support

---

## 📞 Support

For MCP-specific questions:
- **Technical Documentation**: This guide
- **API Reference**: Built-in `/tools/list` endpoint
- **Health Status**: `/health` endpoint
- **GitHub Issues**: [Report issues](https://github.com/Kenway45/MNC-Agent-Hub/issues)

---

**The MCP server transforms your Agent Hub into a powerful AI integration platform, enabling sophisticated document intelligence and seamless AI assistant connectivity.** 🚀