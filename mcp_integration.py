"""
MCP Integration Module for MNC Agent Hub
========================================

This module provides integration between the main Agent Hub application
and the MCP server for standardized AI communication.
"""

import asyncio
import threading
import logging
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from mcp_server import MCPServer, mcp_server

logger = logging.getLogger(__name__)

class MCPIntegration:
    """
    MCP Integration Manager
    
    Handles the lifecycle and integration of the MCP server
    with the main Agent Hub application.
    """
    
    def __init__(self, main_app: FastAPI):
        self.main_app = main_app
        self.mcp_server = mcp_server
        self.mcp_thread: Optional[threading.Thread] = None
        self.is_running = False
        
    def setup_integration(self, docs: Dict[str, Any], employee_log: List[Dict[str, Any]]):
        """
        Setup MCP integration with document store
        
        Args:
            docs: Document store dictionary
            employee_log: Employee activity log list
        """
        # Connect MCP server to data stores
        self.mcp_server.set_document_store(docs, employee_log)
        logger.info("MCP server connected to document store")
        
        # Add MCP endpoints to main app
        self.add_mcp_endpoints()
        
    def add_mcp_endpoints(self):
        """Add MCP-related endpoints to the main application"""
        
        @self.main_app.get("/mcp/status")
        async def mcp_status():
            """Get MCP server status"""
            return {
                "status": "running" if self.is_running else "stopped",
                "host": self.mcp_server.host,
                "port": self.mcp_server.port,
                "capabilities": self.mcp_server.capabilities.dict(),
                "connected_clients": len(self.mcp_server.clients),
                "endpoints": {
                    "websocket": f"ws://{self.mcp_server.host}:{self.mcp_server.port}/mcp",
                    "http": f"http://{self.mcp_server.host}:{self.mcp_server.port}/mcp/http",
                    "health": f"http://{self.mcp_server.host}:{self.mcp_server.port}/health"
                }
            }
        
        @self.main_app.post("/mcp/test-tool")
        async def test_mcp_tool(tool_request: dict):
            """Test MCP tool execution"""
            try:
                # Create MCP message format
                message = {
                    "jsonrpc": "2.0",
                    "id": "test-request",
                    "method": "tools/call",
                    "params": tool_request
                }
                
                # Execute through MCP server
                response = await self.mcp_server.handle_mcp_message(message)
                return response
                
            except Exception as e:
                logger.error(f"MCP tool test error: {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": "test-request",
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
    
    def start_mcp_server(self):
        """Start the MCP server in a separate thread"""
        if not self.is_running:
            def run_mcp_server():
                try:
                    uvicorn.run(
                        self.mcp_server.app,
                        host=self.mcp_server.host,
                        port=self.mcp_server.port,
                        log_level="info"
                    )
                except Exception as e:
                    logger.error(f"MCP server error: {e}")
            
            self.mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
            self.mcp_thread.start()
            self.is_running = True
            logger.info(f"MCP server started on {self.mcp_server.host}:{self.mcp_server.port}")
    
    def stop_mcp_server(self):
        """Stop the MCP server"""
        if self.is_running:
            # Note: In production, you'd want a more graceful shutdown
            self.is_running = False
            logger.info("MCP server stopped")
    
    def get_mcp_client_info(self):
        """Get information about connected MCP clients"""
        return {
            "total_clients": len(self.mcp_server.clients),
            "server_info": {
                "name": "MNC Agent Hub MCP Server",
                "version": "1.0.0",
                "host": self.mcp_server.host,
                "port": self.mcp_server.port
            }
        }

# Context manager for MCP server lifecycle
@asynccontextmanager
async def mcp_lifespan(app: FastAPI):
    """
    Async context manager for MCP server lifecycle
    
    Use this with FastAPI lifespan parameter for automatic
    MCP server startup and shutdown.
    """
    # Startup
    mcp_integration = getattr(app.state, 'mcp_integration', None)
    if mcp_integration:
        mcp_integration.start_mcp_server()
        yield
        # Shutdown
        mcp_integration.stop_mcp_server()
    else:
        yield

def create_mcp_client_example():
    """
    Example MCP client code for testing
    
    Returns:
        Dict containing example client usage
    """
    return {
        "websocket_client_example": {
            "description": "Connect to MCP server via WebSocket",
            "code": """
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
                    "name": "Test Client",
                    "version": "1.0.0"
                }
            }
        }
        
        await websocket.send(json.dumps(init_message))
        response = await websocket.recv()
        print("Initialize response:", response)
        
        # List available tools
        tools_message = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "tools/list"
        }
        
        await websocket.send(json.dumps(tools_message))
        response = await websocket.recv()
        print("Tools response:", response)

asyncio.run(mcp_client())
            """
        },
        "http_client_example": {
            "description": "Call MCP server via HTTP",
            "code": """
import requests

# Test tool call via HTTP
tool_request = {
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

response = requests.post(
    "http://localhost:3001/mcp/http",
    json=tool_request
)

print("Response:", response.json())
            """
        },
        "available_tools": [
            {
                "name": "search_documents",
                "description": "Search through company documents using AI-powered relevance scoring",
                "example": {
                    "name": "search_documents",
                    "arguments": {
                        "query": "security policy",
                        "employee_id": "emp_001",
                        "max_results": 5
                    }
                }
            },
            {
                "name": "summarize_document",
                "description": "Generate AI-powered summary of a specific document",
                "example": {
                    "name": "summarize_document",
                    "arguments": {
                        "doc_id": "doc_001",
                        "max_sentences": 3
                    }
                }
            },
            {
                "name": "answer_question",
                "description": "Answer questions about company documents using context-aware AI",
                "example": {
                    "name": "answer_question",
                    "arguments": {
                        "question": "What is our vacation policy?",
                        "employee_id": "emp_001"
                    }
                }
            },
            {
                "name": "get_analytics",
                "description": "Get system analytics and employee activity data",
                "example": {
                    "name": "get_analytics",
                    "arguments": {
                        "metric_type": "system"
                    }
                }
            },
            {
                "name": "auto_tag_document",
                "description": "Automatically generate tags for a document using AI analysis",
                "example": {
                    "name": "auto_tag_document",
                    "arguments": {
                        "content": "This document outlines our security procedures...",
                        "title": "Security Guidelines",
                        "category": "policy"
                    }
                }
            }
        ]
    }