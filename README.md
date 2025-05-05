[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/nrjchnd-voipbin-mcp-badge.png)](https://mseep.ai/app/nrjchnd-voipbin-mcp)

# VoIPBin MCP Server

A Model Context Protocol (MCP) server implementation for the VoIPBin API, enabling AI models to interact with VoIP services.

## Disclaimer

This software is provided "as is" without any warranties, either express or implied. The author makes no guarantees about the completeness, reliability, or accuracy of this software. Any use of this software is at your own risk. The author shall not be liable for any damages arising from the use of this software.

## Overview

This MCP server provides a standardized interface for AI models to interact with VoIPBin's API services. It implements the Model Context Protocol specification and supports both SSE and stdio transport types.

## Features

- Full VoIPBin API integration through MCP protocol
- Support for both stdio and SSE transport modes
- Comprehensive tool definitions with proper annotations
- Type-safe request/response handling
- Asynchronous HTTP requests
- Proper error handling and validation
- Docker support for easy deployment

## Available Tools

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
- `get_billing_history`: Retrieve billing history with optional date filtering

## Setup

### Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Update the `.env` file with your VoIPBin API credentials:
```
VOIPBIN_API_URL=https://api.voipbin.net/v1.0
VOIPBIN_API_KEY=your-api-key-here
PORT=8000
```

### Docker Setup

1. Build and run using Docker Compose:
```bash
# Build and start the container
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the container
docker-compose down
```

2. Or build and run using Docker directly:
```bash
# Build the image
docker build -t voipbin-mcp-server .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e VOIPBIN_API_KEY=your-api-key-here \
  -e VOIPBIN_API_URL=https://api.voipbin.net/v1.0 \
  voipbin-mcp-server
```

## Running the Server

### Local Development

#### Standard I/O Mode
```bash
python src/main.py --transport stdio
```

#### SSE Mode
```bash
python src/main.py --transport sse --port 8000
```

### Docker

The server runs in SSE mode by default when using Docker. The container exposes port 8000 for SSE connections.

## Tool Usage Examples

### Creating a Call
```json
{
  "name": "create_call",
  "arguments": {
    "body": {
      "phone_number": "+1234567890",
      "agent_id": "agent_123",
      "campaign_id": "campaign_456"
    }
  }
}
```

### Getting Call Details
```json
{
  "name": "get_call",
  "arguments": {
    "call_id": "call_789"
  }
}
```

### Creating a Conference
```json
{
  "name": "create_conference",
  "arguments": {
    "body": {
      "name": "Team Meeting",
      "participants": ["+1234567890", "+0987654321"]
    }
  }
}
```

### Sending a Chat Message
```json
{
  "name": "send_chat_message",
  "arguments": {
    "chat_id": "chat_123",
    "body": {
      "message": "Hello, how can I help you today?"
    }
  }
}
```

## Tool Annotations

Each tool includes annotations that provide metadata about its behavior:

- `readOnlyHint`: Indicates if the tool only reads data
- `destructiveHint`: Indicates if the tool modifies or deletes data
- `idempotentHint`: Indicates if repeated calls have the same effect as a single call
- `openWorldHint`: Indicates if the tool operates in an open world context

## Error Handling

The server includes comprehensive error handling:
- Invalid API credentials
- Network connectivity issues
- Invalid request parameters
- Rate limiting
- Server errors

## Development

### Adding New Tools

To add a new tool:

1. Add the tool definition in the `list_tools()` function
2. Implement the tool handler in the `voipbin_tool()` function
3. Update the documentation

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Security

- API keys are stored securely in environment variables
- All requests are authenticated
- HTTPS is enforced for API communication
- Input validation is performed on all requests
- Docker container runs as non-root user
- Health checks ensure container is running properly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that is short and to the point. It lets people do anything they want with the code as long as they provide attribution back to you and don't hold you liable.

### What you can do with this code:
- Use it commercially
- Modify it
- Distribute it
- Use it privately
- Sublicense it

### What you must do:
- Include the original copyright notice
- Include the license text
- Provide clear attribution to the original source
- Maintain attribution in any derivative works

### What you cannot do:
- Hold the author liable for damages
- Remove or obscure the attribution
- Claim the work as your own

For more information about the MIT License, visit [choosealicense.com/licenses/mit/](https://choosealicense.com/licenses/mit/). 