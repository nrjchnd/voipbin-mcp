# VoIPBin MCP Server - AI Integration Guide

This guide explains how to integrate the VoIPBin MCP Server with AI models like Claude and OpenAI.

## Overview

The VoIPBin MCP Server provides a standardized interface for AI models to interact with VoIP functionality through the Model Context Protocol (MCP). This allows AI models to make calls, manage agents, handle campaigns, and perform other VoIP operations in a secure and controlled manner.

## Integration Methods

### 1. Using the MCP CLI

The simplest way to integrate with the server is using the MCP CLI:

```bash
# Install the MCP CLI
pip install "mcp[cli]"

# Run the server in development mode
mcp dev src/main.py

# Install the server in Claude Desktop
mcp install src/main.py --name "VoIPBin Server"
```

### 2. Direct Integration with Claude

To integrate directly with Claude:

1. Start the MCP server:
```bash
python src/main.py
```

2. Configure Claude to use the MCP server by adding the following to your Claude configuration:
```json
{
  "mcp_servers": [
    {
      "name": "voipbin",
      "url": "http://localhost:8000/mcp",
      "transport": "sse"
    }
  ]
}
```

3. Example Claude prompt:
```
You can now use the VoIPBin API through the MCP server. For example:
- List all active calls
- Create a new campaign
- Send a chat message
```

### 3. Integration with OpenAI

To integrate with OpenAI:

1. Start the MCP server:
```bash
python src/main.py
```

2. Configure your OpenAI application to use the MCP server:
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/mcp",
    api_key="your-api-key"
)
```

3. Example usage:
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a VoIP assistant. Use the available tools to help manage calls and campaigns."},
        {"role": "user", "content": "List all active calls"}
    ]
)
```

## Available Tools

The server provides the following tools for AI models to use:

### Call Management
- `get_calls`: Retrieve a list of calls with optional filtering
- `get_call`: Get details of a specific call
- `create_call`: Create a new call
- `end_call`: End an active call

### Agent Management
- `get_agents`: Retrieve a list of agents
- `get_agent`: Get details of a specific agent
- `update_agent_status`: Update an agent's status

### Campaign Management
- `get_campaigns`: Retrieve a list of campaigns
- `get_campaign`: Get details of a specific campaign
- `create_campaign`: Create a new campaign

### Recording Management
- `get_recordings`: Retrieve a list of call recordings
- `get_recording`: Get details of a specific recording

### Queue Management
- `get_queues`: Retrieve a list of call queues
- `get_queue`: Get details of a specific queue

### Conference Management
- `get_conferences`: Retrieve a list of active conferences
- `create_conference`: Create a new conference

### Chat Management
- `get_chats`: Retrieve a list of chat conversations
- `send_chat_message`: Send a message in a chat conversation

### Billing Management
- `get_billing_info`: Retrieve current billing information
- `get_billing_history`: Retrieve billing history

## Security Considerations

1. API Key Management:
   - Store the VoIPBin API key securely in environment variables
   - Never expose the API key in logs or error messages
   - Use the `.env` file for local development

2. Access Control:
   - The MCP server should be deployed behind a secure proxy
   - Implement rate limiting for API calls
   - Monitor and log all API access

3. Data Protection:
   - All API responses are logged for debugging
   - Sensitive data is filtered from logs
   - Use HTTPS for all API communications

## Monitoring and Debugging

The server provides detailed logging for monitoring and debugging:

1. Log Levels:
   - DEBUG: Detailed information for debugging
   - INFO: General operational information
   - ERROR: Error messages and exceptions

2. Log Format:
   ```
   %(asctime)s - %(name)s - %(levelname)s - %(message)s
   ```

3. Health Check:
   - Endpoint: `/health`
   - Returns server status and timestamp
   - Use for monitoring server availability

## Example Usage

### Making a Call
```python
# Using the MCP server
response = await mcp.call_tool("create_call", {
    "body": {
        "phone_number": "+1234567890",
        "agent_id": "agent_123",
        "campaign_id": "campaign_456"
    }
})
```

### Managing Agents
```python
# Get agent status
agent_status = await mcp.call_tool("get_agent", {
    "agent_id": "agent_123"
})

# Update agent status
await mcp.call_tool("update_agent_status", {
    "agent_id": "agent_123",
    "body": {
        "status": "available"
    }
})
```

### Campaign Management
```python
# Create a new campaign
campaign = await mcp.call_tool("create_campaign", {
    "body": {
        "name": "Sales Campaign Q1",
        "description": "Q1 2024 sales campaign",
        "start_date": "2024-01-01",
        "end_date": "2024-03-31"
    }
})
```

## Troubleshooting

1. Connection Issues:
   - Check if the server is running
   - Verify the port (8000) is not blocked
   - Check network connectivity

2. API Errors:
   - Verify the VoIPBin API key is valid
   - Check API rate limits
   - Review server logs for detailed error messages

3. SSE Connection:
   - Test the SSE endpoint: `curl http://localhost:8000/sse`
   - Check for heartbeat messages
   - Verify client can maintain connection

## Support

For issues or questions:
1. Check the server logs for detailed error messages
2. Review the VoIPBin API documentation
3. Contact support with the relevant log entries 