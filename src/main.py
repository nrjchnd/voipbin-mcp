"""
VoIPBin MCP Server

A Model Context Protocol (MCP) server implementation for the VoIPBin API.
This server enables AI models to interact with VoIP services through a standardized interface.

Author:
    nrjchnd (nrjchnd@gmail.com)
    GitHub: https://github.com/nrjchnd
"""

import os
from dotenv import load_dotenv
import httpx
from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
import json
import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("voipbin_mcp")

# Load environment variables
load_dotenv()

# Configuration
VOIPBIN_API_URL = os.getenv("VOIPBIN_API_URL", "https://api.voipbin.net/v1.0")
API_KEY = os.getenv("VOIPBIN_API_KEY")

logger.info(f"Starting VoIPBin MCP Server with API URL: {VOIPBIN_API_URL}")

# Create FastAPI app for SSE
app = FastAPI(title="VoIPBin MCP Server")

# Create MCP server
mcp = FastMCP("VoIPBin MCP Server")

async def make_voipbin_request(
    endpoint: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    path_params: Optional[Dict[str, str]] = None
) -> str:
    logger.debug(f"Making {method} request to {endpoint}")
    logger.debug(f"Parameters: {params}")
    logger.debug(f"Body: {body}")
    logger.debug(f"Path params: {path_params}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "VoIPBin MCP Server"
    }
    
    async with httpx.AsyncClient() as client:
        url = f"{VOIPBIN_API_URL}/{endpoint}"
        if path_params:
            url = url.format(**path_params)
            
        logger.debug(f"Full URL: {url}")
        
        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=body,
                headers=headers
            )
            response.raise_for_status()
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"Error making request: {str(e)}")
            raise

# Call Management Tools
@mcp.tool()
async def get_calls(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of calls with optional filtering"""
    logger.info("Getting calls list")
    return await make_voipbin_request("calls", "GET", params=params)

@mcp.tool()
async def get_call(call_id: str) -> str:
    """Get details of a specific call"""
    logger.info(f"Getting call details for ID: {call_id}")
    return await make_voipbin_request("calls/{call_id}", "GET", path_params={"call_id": call_id})

@mcp.tool()
async def create_call(body: Dict[str, Any]) -> str:
    """Create a new call"""
    logger.info(f"Creating new call with body: {body}")
    return await make_voipbin_request("calls", "POST", body=body)

@mcp.tool()
async def end_call(call_id: str) -> str:
    """End an active call"""
    logger.info(f"Ending call with ID: {call_id}")
    return await make_voipbin_request("calls/{call_id}/end", "POST", path_params={"call_id": call_id})

# Agent Management Tools
@mcp.tool()
async def get_agents(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of agents"""
    logger.info("Getting agents list")
    return await make_voipbin_request("agents", "GET", params=params)

@mcp.tool()
async def get_agent(agent_id: str) -> str:
    """Get details of a specific agent"""
    logger.info(f"Getting agent details for ID: {agent_id}")
    return await make_voipbin_request("agents/{agent_id}", "GET", path_params={"agent_id": agent_id})

@mcp.tool()
async def update_agent_status(agent_id: str, body: Dict[str, Any]) -> str:
    """Update an agent's status"""
    logger.info(f"Updating agent {agent_id} status with body: {body}")
    return await make_voipbin_request("agents/{agent_id}/status", "PUT", path_params={"agent_id": agent_id}, body=body)

# Campaign Management Tools
@mcp.tool()
async def get_campaigns(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of campaigns"""
    logger.info("Getting campaigns list")
    return await make_voipbin_request("campaigns", "GET", params=params)

@mcp.tool()
async def get_campaign(campaign_id: str) -> str:
    """Get details of a specific campaign"""
    logger.info(f"Getting campaign details for ID: {campaign_id}")
    return await make_voipbin_request("campaigns/{campaign_id}", "GET", path_params={"campaign_id": campaign_id})

@mcp.tool()
async def create_campaign(body: Dict[str, Any]) -> str:
    """Create a new campaign"""
    logger.info(f"Creating new campaign with body: {body}")
    return await make_voipbin_request("campaigns", "POST", body=body)

# Recording Management Tools
@mcp.tool()
async def get_recordings(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of call recordings"""
    logger.info("Getting recordings list")
    return await make_voipbin_request("recordings", "GET", params=params)

@mcp.tool()
async def get_recording(recording_id: str) -> str:
    """Get details of a specific recording"""
    logger.info(f"Getting recording details for ID: {recording_id}")
    return await make_voipbin_request("recordings/{recording_id}", "GET", path_params={"recording_id": recording_id})

# Queue Management Tools
@mcp.tool()
async def get_queues(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of call queues"""
    logger.info("Getting queues list")
    return await make_voipbin_request("queues", "GET", params=params)

@mcp.tool()
async def get_queue(queue_id: str) -> str:
    """Get details of a specific queue"""
    logger.info(f"Getting queue details for ID: {queue_id}")
    return await make_voipbin_request("queues/{queue_id}", "GET", path_params={"queue_id": queue_id})

# Conference Management Tools
@mcp.tool()
async def get_conferences(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of active conferences"""
    logger.info("Getting conferences list")
    return await make_voipbin_request("conferences", "GET", params=params)

@mcp.tool()
async def create_conference(body: Dict[str, Any]) -> str:
    """Create a new conference"""
    logger.info(f"Creating new conference with body: {body}")
    return await make_voipbin_request("conferences", "POST", body=body)

# Chat Management Tools
@mcp.tool()
async def get_chats(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve a list of chat conversations"""
    logger.info("Getting chats list")
    return await make_voipbin_request("chats", "GET", params=params)

@mcp.tool()
async def send_chat_message(chat_id: str, body: Dict[str, Any]) -> str:
    """Send a message in a chat conversation"""
    logger.info(f"Sending message to chat {chat_id} with body: {body}")
    return await make_voipbin_request("chats/{chat_id}/messages", "POST", path_params={"chat_id": chat_id}, body=body)

# Billing Management Tools
@mcp.tool()
async def get_billing_info() -> str:
    """Retrieve current billing information"""
    logger.info("Getting billing information")
    return await make_voipbin_request("billing", "GET")

@mcp.tool()
async def get_billing_history(params: Optional[Dict[str, Any]] = None) -> str:
    """Retrieve billing history"""
    logger.info("Getting billing history")
    return await make_voipbin_request("billing/history", "GET", params=params)

# Health check endpoint
@app.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# SSE endpoint
@app.get("/sse")
async def sse_endpoint(request: Request):
    logger.info(f"New SSE connection from {request.client.host}")
    async def event_stream():
        try:
            while True:
                # Send a heartbeat every 30 seconds
                heartbeat = {
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                }
                logger.debug(f"Sending heartbeat: {heartbeat}")
                yield "data: " + json.dumps(heartbeat) + "\n\n"
                await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"Error in SSE stream: {str(e)}")
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

# Add MCP routes to FastAPI app
@app.post("/mcp/call_tool")
async def call_tool(request: Request):
    """Handle MCP tool calls"""
    body = await request.json()
    logger.debug(f"Received tool call request: {body}")
    return await mcp.handle_call_tool(body)

@app.get("/mcp/list_tools")
async def list_tools():
    """List available MCP tools"""
    logger.debug("Listing available tools")
    return await mcp.handle_list_tools()

@app.get("/mcp/list_resources")
async def list_resources():
    """List available MCP resources"""
    logger.debug("Listing available resources")
    return await mcp.handle_list_resources()

@app.get("/mcp/list_prompts")
async def list_prompts():
    """List available MCP prompts"""
    logger.debug("Listing available prompts")
    return await mcp.handle_list_prompts()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting VoIPBin MCP Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug") 