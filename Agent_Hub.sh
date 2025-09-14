#!/bin/bash

# MNC Agent Hub Launcher
# Main startup script for the Agent Hub system

echo "========================================="
echo "       MNC Agent Hub System"
echo "========================================="
echo ""
echo "Starting Agent Hub with MCP Server..."
echo ""
echo "🌐 Access URLs:"
echo "• Main Hub: http://localhost:8888"
echo "• MCP Server: http://localhost:3001"
echo "• MCP WebSocket: ws://localhost:3001/mcp"
echo ""
echo "🚀 Features:"
echo "• Employee Portal - Document access & AI assistance"
echo "• Admin Dashboard - Management & analytics"
echo "• MCP Server - Standardized AI integration"
echo "• Real-time updates across all interfaces"
echo ""
echo "🤖 MCP Integration:"
echo "• 5 AI Tools: search, summarize, Q&A, analytics, tagging"
echo "• WebSocket & HTTP endpoints available"
echo "• Compatible with Claude, GPT, local LLMs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================="
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "agent_hub_env" ]; then
    source agent_hub_env/bin/activate
fi

# Start the Agent Hub server
python3 -m uvicorn app:app --host 0.0.0.0 --port 8889 --reload
