#!/usr/bin/env bash
# Launch MCP server and ticket server in the background then run the Streamlit demo.
uvicorn mcp_server:app --reload &
MCP_PID=$!
uvicorn ticket_server:app --port 9000 --reload &
TICKET_PID=$!
# Give the servers a moment to start
sleep 1
streamlit run app.py
# Stop servers when Streamlit exits
kill $MCP_PID
kill $TICKET_PID
