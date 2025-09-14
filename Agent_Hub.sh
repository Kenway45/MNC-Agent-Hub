#!/bin/bash

# MNC Agent Hub Launcher
# Main startup script for the Agent Hub system

echo "========================================="
echo "       MNC Agent Hub System"
echo "========================================="
echo ""
echo "Starting Agent Hub..."
echo "Access URL: http://localhost:8888"
echo ""
echo "Features:"
echo "• Employee Portal - Document access & AI assistance"
echo "• Admin Dashboard - Management & analytics"
echo "• Real-time updates across interfaces"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Start the Agent Hub server
python3 -m uvicorn app:app --host 0.0.0.0 --port 8888 --reload