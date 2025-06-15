#!/usr/bin/env bash
# Launch MCP server in the background and run the Streamlit demo.
uvicorn mcp_server:app --reload &
SERVER_PID=$!
# Give the server a moment to start
sleep 1
streamlit run app.py
# Stop the MCP server when Streamlit exits
kill $SERVER_PID
