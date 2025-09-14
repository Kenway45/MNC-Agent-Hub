"""
MNC Agent Hub - MCP (Model Context Protocol) Server
=====================================================

This module implements the MCP server for standardized AI model integration
with the Agent Hub document management system.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPMessageType(str, Enum):
    """MCP message types according to the protocol specification"""
    REQUEST = "request"
    RESPONSE = "response" 
    NOTIFICATION = "notification"
    ERROR = "error"

class MCPMethod(str, Enum):
    """MCP method types for different operations"""
    INITIALIZE = "initialize"
    PING = "ping"
    GET_RESOURCES = "resources/list"
    READ_RESOURCE = "resources/read"
    CALL_TOOL = "tools/call"
    LIST_TOOLS = "tools/list"
    GET_PROMPTS = "prompts/list"
    GET_PROMPT = "prompts/get"
    COMPLETE = "completion/complete"

class MCPCapabilities(BaseModel):
    """MCP server capabilities"""
    resources: bool = True
    tools: bool = True
    prompts: bool = True
    completion: bool = True
    logging: bool = True

class MCPResource(BaseModel):
    """MCP resource definition"""
    uri: str
    name: str
    description: str
    mimeType: Optional[str] = None

class MCPTool(BaseModel):
    """MCP tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPPrompt(BaseModel):
    """MCP prompt definition"""
    name: str
    description: str
    arguments: Optional[List[Dict[str, Any]]] = None

class MCPMessage(BaseModel):
    """Base MCP message structure"""
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPError(BaseModel):
    """MCP error structure"""
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None

class MCPServer:
    """
    MCP Server for Agent Hub AI Integration
    
    Provides standardized AI model communication following the MCP specification
    for document management, search, and analytics operations.
    """
    
    def __init__(self, host: str = "localhost", port: int = 3001):
        self.host = host
        self.port = port
        self.app = FastAPI(title="MNC Agent Hub MCP Server")
        self.capabilities = MCPCapabilities()
        self.clients: List[WebSocket] = []
        self.ollama_base_url = "http://localhost:11434"
        self.model_name = "deepseek-coder:6.7b"
        
        # Document store reference (would be injected from main app)
        self.docs = {}
        self.employee_log = []
        
        self.setup_routes()
        
    def setup_routes(self):
        """Setup FastAPI routes for MCP server"""
        
        @self.app.websocket("/mcp")
        async def mcp_websocket(websocket: WebSocket):
            await self.handle_websocket_connection(websocket)
            
        @self.app.post("/mcp/http")
        async def mcp_http(message: MCPMessage):
            return await self.handle_mcp_message(message.dict())
            
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    
    async def handle_websocket_connection(self, websocket: WebSocket):
        """Handle WebSocket MCP connections"""
        await websocket.accept()
        self.clients.append(websocket)
        
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                response = await self.handle_mcp_message(message)
                if response:
                    await websocket.send_text(json.dumps(response))
                    
        except WebSocketDisconnect:
            self.clients.remove(websocket)
            logger.info("MCP client disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            if websocket in self.clients:
                self.clients.remove(websocket)
    
    async def handle_mcp_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming MCP messages"""
        try:
            method = message.get("method")
            params = message.get("params", {})
            msg_id = message.get("id")
            
            logger.info(f"Handling MCP method: {method}")
            
            if method == MCPMethod.INITIALIZE:
                return await self.handle_initialize(msg_id, params)
            elif method == MCPMethod.PING:
                return await self.handle_ping(msg_id)
            elif method == MCPMethod.LIST_TOOLS:
                return await self.handle_list_tools(msg_id)
            elif method == MCPMethod.CALL_TOOL:
                return await self.handle_call_tool(msg_id, params)
            elif method == MCPMethod.GET_RESOURCES:
                return await self.handle_list_resources(msg_id)
            elif method == MCPMethod.READ_RESOURCE:
                return await self.handle_read_resource(msg_id, params)
            elif method == MCPMethod.GET_PROMPTS:
                return await self.handle_list_prompts(msg_id)
            elif method == MCPMethod.GET_PROMPT:
                return await self.handle_get_prompt(msg_id, params)
            elif method == MCPMethod.COMPLETE:
                return await self.handle_completion(msg_id, params)
            else:
                return self.create_error_response(msg_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            logger.error(f"Error handling MCP message: {e}")
            return self.create_error_response(message.get("id"), -32603, str(e))
    
    async def handle_initialize(self, msg_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": asdict(self.capabilities),
                "serverInfo": {
                    "name": "MNC Agent Hub MCP Server",
                    "version": "1.0.0",
                    "description": "Enterprise document management AI integration"
                }
            }
        }
    
    async def handle_ping(self, msg_id: Optional[Union[str, int]]) -> Dict[str, Any]:
        """Handle ping request"""
        return {
            "jsonrpc": "2.0", 
            "id": msg_id,
            "result": {"status": "pong"}
        }
    
    async def handle_list_tools(self, msg_id: Optional[Union[str, int]]) -> Dict[str, Any]:
        """List available MCP tools"""
        tools = [
            MCPTool(
                name="search_documents",
                description="Search through company documents using AI-powered relevance scoring",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "employee_id": {"type": "string", "description": "Employee making the request"},
                        "max_results": {"type": "integer", "default": 10}
                    },
                    "required": ["query", "employee_id"]
                }
            ),
            MCPTool(
                name="summarize_document", 
                description="Generate AI-powered summary of a specific document",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_id": {"type": "string", "description": "Document ID to summarize"},
                        "max_sentences": {"type": "integer", "default": 3, "minimum": 1, "maximum": 10}
                    },
                    "required": ["doc_id"]
                }
            ),
            MCPTool(
                name="answer_question",
                description="Answer questions about company documents using context-aware AI",
                inputSchema={
                    "type": "object", 
                    "properties": {
                        "question": {"type": "string", "description": "Question to answer"},
                        "employee_id": {"type": "string", "description": "Employee asking the question"},
                        "context_docs": {"type": "array", "items": {"type": "string"}, "description": "Optional specific document IDs for context"}
                    },
                    "required": ["question", "employee_id"]
                }
            ),
            MCPTool(
                name="get_analytics",
                description="Get system analytics and employee activity data", 
                inputSchema={
                    "type": "object",
                    "properties": {
                        "metric_type": {"type": "string", "enum": ["system", "employee", "documents", "queries"]},
                        "employee_id": {"type": "string", "description": "Optional specific employee ID"},
                        "date_range": {"type": "string", "description": "Optional date range filter"}
                    },
                    "required": ["metric_type"]
                }
            ),
            MCPTool(
                name="auto_tag_document",
                description="Automatically generate tags for a document using AI analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Document content to analyze"},
                        "title": {"type": "string", "description": "Document title"},
                        "category": {"type": "string", "description": "Document category"}
                    },
                    "required": ["content"]
                }
            )
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id, 
            "result": {
                "tools": [tool.dict() for tool in tools]
            }
        }
    
    async def handle_call_tool(self, msg_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution requests"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "search_documents":
                result = await self.search_documents_tool(arguments)
            elif tool_name == "summarize_document":
                result = await self.summarize_document_tool(arguments)
            elif tool_name == "answer_question":
                result = await self.answer_question_tool(arguments)
            elif tool_name == "get_analytics": 
                result = await self.get_analytics_tool(arguments)
            elif tool_name == "auto_tag_document":
                result = await self.auto_tag_document_tool(arguments)
            else:
                return self.create_error_response(msg_id, -32602, f"Unknown tool: {tool_name}")
            
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return self.create_error_response(msg_id, -32603, f"Tool execution failed: {str(e)}")
    
    async def search_documents_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search documents tool implementation"""
        query = args["query"]
        employee_id = args["employee_id"] 
        max_results = args.get("max_results", 10)
        
        # Log the search
        self.log_employee_activity(employee_id, "search", query)
        
        # Perform search with relevance scoring
        results = []
        search_terms = query.lower().split()
        
        for doc_id, doc in self.docs.items():
            score = 0
            text_content = (doc.get("title", "") + " " + doc.get("text", "") + " " + " ".join(doc.get("tags", []))).lower()
            
            for term in search_terms:
                if term in text_content:
                    score += text_content.count(term)
            
            if score > 0:
                results.append({
                    "id": doc_id,
                    "title": doc.get("title", ""),
                    "score": score,
                    "tags": doc.get("tags", []),
                    "category": doc.get("category", "")
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:max_results]
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results)
        }
    
    async def summarize_document_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Document summarization tool implementation"""
        doc_id = args["doc_id"]
        max_sentences = args.get("max_sentences", 3)
        
        if doc_id not in self.docs:
            raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
        
        doc = self.docs[doc_id]
        content = doc.get("text", "")
        
        # Generate summary using Ollama
        summary = await self.call_ollama_for_summary(content, max_sentences)
        
        return {
            "document_id": doc_id,
            "document_title": doc.get("title", ""),
            "summary": summary.get("summary", ""),
            "key_points": summary.get("action_items", []),
            "max_sentences": max_sentences
        }
    
    async def answer_question_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Question answering tool implementation"""
        question = args["question"]
        employee_id = args["employee_id"]
        context_docs = args.get("context_docs", [])
        
        # Log the question
        self.log_employee_activity(employee_id, "question", question)
        
        # Build context from documents
        context = ""
        used_docs = []
        
        # Use specific docs if provided, otherwise use all docs
        docs_to_use = context_docs if context_docs else list(self.docs.keys())
        
        for doc_id in docs_to_use:
            if doc_id in self.docs:
                doc = self.docs[doc_id]
                context += f"Document {doc_id}: {doc.get('title', '')}\n{doc.get('text', '')}\n\n"
                used_docs.append(doc_id)
        
        # Get answer from Ollama
        answer = await self.call_ollama_for_answer(question, context)
        
        return {
            "question": question,
            "answer": answer,
            "context_documents": used_docs,
            "employee_id": employee_id
        }
    
    async def get_analytics_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analytics tool implementation"""
        metric_type = args["metric_type"]
        employee_id = args.get("employee_id")
        
        if metric_type == "system":
            return {
                "total_documents": len(self.docs),
                "total_queries": len(self.employee_log),
                "active_employees": len(set(log.get("employee_id") for log in self.employee_log)),
                "timestamp": datetime.utcnow().isoformat()
            }
        elif metric_type == "employee" and employee_id:
            employee_queries = [log for log in self.employee_log if log.get("employee_id") == employee_id]
            return {
                "employee_id": employee_id,
                "total_queries": len(employee_queries),
                "query_types": {},
                "last_activity": max([log.get("timestamp") for log in employee_queries], default=None)
            }
        elif metric_type == "documents":
            return {
                "documents": [
                    {
                        "id": doc_id,
                        "title": doc.get("title", ""),
                        "category": doc.get("category", ""),
                        "tags": doc.get("tags", [])
                    }
                    for doc_id, doc in self.docs.items()
                ]
            }
        else:
            return {"error": f"Invalid metric type: {metric_type}"}
    
    async def auto_tag_document_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-tagging tool implementation"""
        content = args["content"]
        title = args.get("title", "")
        category = args.get("category", "")
        
        # Simple keyword-based tagging (can be enhanced with ML)
        text_lower = (title + " " + content + " " + category).lower()
        tags = []
        
        tag_keywords = {
            "policy": ["policy", "procedure", "rule", "regulation"],
            "hr": ["employee", "staff", "human", "resource", "personnel"],
            "security": ["security", "privacy", "confidential", "password", "access"],
            "compliance": ["compliance", "audit", "legal", "requirement"],
            "process": ["process", "workflow", "procedure", "step"],
            "guideline": ["guideline", "guide", "standard", "best practice"],
            "technical": ["technical", "system", "software", "hardware"],
            "training": ["training", "education", "learning", "development"]
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
        
        if not tags:
            tags.append("general")
        
        return {
            "suggested_tags": tags,
            "confidence": len(tags) / len(tag_keywords),  # Simple confidence score
            "analysis": f"Generated {len(tags)} tags based on content analysis"
        }
    
    async def handle_list_resources(self, msg_id: Optional[Union[str, int]]) -> Dict[str, Any]:
        """List available MCP resources"""
        resources = []
        
        for doc_id, doc in self.docs.items():
            resources.append(MCPResource(
                uri=f"document://{doc_id}",
                name=doc.get("title", f"Document {doc_id}"),
                description=f"Company document: {doc.get('category', 'General')}",
                mimeType="text/plain"
            ))
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "resources": [resource.dict() for resource in resources]
            }
        }
    
    async def handle_read_resource(self, msg_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific resource"""
        uri = params.get("uri", "")
        
        if uri.startswith("document://"):
            doc_id = uri.replace("document://", "")
            if doc_id in self.docs:
                doc = self.docs[doc_id]
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "text/plain", 
                                "text": doc.get("text", "")
                            }
                        ]
                    }
                }
        
        return self.create_error_response(msg_id, -32602, f"Resource not found: {uri}")
    
    async def handle_list_prompts(self, msg_id: Optional[Union[str, int]]) -> Dict[str, Any]:
        """List available MCP prompts"""
        prompts = [
            MCPPrompt(
                name="document_summary",
                description="Generate a comprehensive summary of a company document",
                arguments=[
                    {"name": "doc_id", "description": "Document ID to summarize", "required": True},
                    {"name": "length", "description": "Summary length (short/medium/long)", "required": False}
                ]
            ),
            MCPPrompt(
                name="search_assistant",
                description="Help employees find relevant documents and information",
                arguments=[
                    {"name": "query", "description": "What the employee is looking for", "required": True},
                    {"name": "context", "description": "Additional context about the request", "required": False}
                ]
            ),
            MCPPrompt(
                name="compliance_check",
                description="Check document compliance with company policies",
                arguments=[
                    {"name": "doc_content", "description": "Document content to check", "required": True},
                    {"name": "policy_type", "description": "Type of policy to check against", "required": False}
                ]
            )
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "prompts": [prompt.dict() for prompt in prompts]
            }
        }
    
    async def handle_get_prompt(self, msg_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a specific prompt"""
        name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        if name == "document_summary":
            doc_id = arguments.get("doc_id", "")
            length = arguments.get("length", "medium")
            
            if doc_id in self.docs:
                doc = self.docs[doc_id]
                prompt_text = f"""Please provide a {length} summary of this document:

Title: {doc.get('title', 'Untitled')}
Category: {doc.get('category', 'General')}

Content:
{doc.get('text', '')}

Please focus on the key points and actionable information."""
                
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "description": f"Summary prompt for document {doc_id}",
                        "messages": [
                            {
                                "role": "user",
                                "content": {
                                    "type": "text",
                                    "text": prompt_text
                                }
                            }
                        ]
                    }
                }
        
        return self.create_error_response(msg_id, -32602, f"Prompt not found: {name}")
    
    async def handle_completion(self, msg_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle completion requests"""
        prompt = params.get("prompt", "")
        max_tokens = params.get("maxTokens", 1000)
        
        # Use Ollama for completion
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_predict": max_tokens
                        }
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "completion": {
                                "type": "text",
                                "text": result.get("response", "")
                            }
                        }
                    }
        except Exception as e:
            logger.error(f"Ollama completion error: {e}")
        
        return self.create_error_response(msg_id, -32603, "Completion service unavailable")
    
    async def call_ollama_for_summary(self, content: str, max_sentences: int) -> Dict[str, Any]:
        """Call Ollama for document summarization"""
        prompt = f"""You MUST respond ONLY with valid JSON with two fields: 
{{"summary": "<concise summary>", "action_items": ["item1","item2"]}}. 
Summary should be concise and up to {max_sentences} sentences. Document:

{content}"""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get("response", "")
                    
                    # Try to parse JSON from response
                    try:
                        import re
                        json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
                        if json_match:
                            return json.loads(json_match.group(1))
                    except:
                        pass
                    
                    return {"summary": response_text, "action_items": []}
        except Exception as e:
            logger.error(f"Ollama summary error: {e}")
        
        return {"summary": "AI service unavailable", "action_items": []}
    
    async def call_ollama_for_answer(self, question: str, context: str) -> str:
        """Call Ollama for question answering"""
        prompt = f"Answer this question based on the company documents: {question}\n\nDocuments:\n{context}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "AI service unavailable")
        except Exception as e:
            logger.error(f"Ollama answer error: {e}")
        
        return "AI service is currently unavailable. Please try again later."
    
    def log_employee_activity(self, employee_id: str, query_type: str, query: str):
        """Log employee activity"""
        self.employee_log.append({
            "query_id": f"mcp_{len(self.employee_log)}",
            "employee_id": employee_id,
            "query": query,
            "query_type": query_type,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mcp"
        })
    
    def create_error_response(self, msg_id: Optional[Union[str, int]], code: int, message: str) -> Dict[str, Any]:
        """Create MCP error response"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    def set_document_store(self, docs: Dict[str, Any], employee_log: List[Dict[str, Any]]):
        """Set references to document store and employee log"""
        self.docs = docs
        self.employee_log = employee_log
    
    async def start_server(self):
        """Start the MCP server"""
        import uvicorn
        logger.info(f"Starting MCP server on {self.host}:{self.port}")
        await uvicorn.run(self.app, host=self.host, port=self.port)

# Global MCP server instance
mcp_server = MCPServer()

# FastAPI app for integration
app = mcp_server.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3001)