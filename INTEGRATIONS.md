# MCP Integrations Guide

This comprehensive guide provides step-by-step instructions for integrating various tools and services with the Model Context Protocol (MCP).

## Table of Contents

- [LM Studio](#lm-studio)
- [Docker Desktop](#docker-desktop)
- [Obsidian with Local REST API Plugin](#obsidian-with-local-rest-api-plugin)
- [Marcel Marais' Obsidian-MCP-Server](#marcel-marais-obsidian-mcp-server)
- [Logseq](#logseq)
- [Cursor](#cursor)
- [Claude Sonnet](#claude-sonnet)
- [Cloud Server Setup](#cloud-server-setup)
- [Troubleshooting](#troubleshooting)

---

## LM Studio

LM Studio is a platform for running local language models on your computer.

### Prerequisites

- LM Studio installed ([download here](https://lmstudio.ai/))
- Python 3.9+ installed
- MCP server implementation

### Integration Steps

#### 1. Install and Configure LM Studio

1. **Download and Install LM Studio**
   - Visit [lmstudio.ai](https://lmstudio.ai/)
   - Download and install LM Studio for your operating system

2. **Load a Model**
   - Open LM Studio
   - Download a language model (e.g., Llama 2, Mistral)
   - Load the model in LM Studio

3. **Enable Local Server**
   - In LM Studio, go to **Settings** → **Local Server**
   - Enable **"Serve on Local Host"**
   - Set the port (default: `1234`)
   - Enable **"Enable CORS"** to allow cross-origin requests
   - Click **"Start Server"**

4. **Verify Server is Running**
   - Open a browser and navigate to `http://localhost:1234`
   - You should see the LM Studio API interface

#### 2. Create MCP Tool for LM Studio

Create a new tool file `src/tools/lm_studio_tools.py`:

```python
"""
LM Studio Integration Tools
"""

import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LMStudioTools:
    """Tools for interacting with LM Studio"""
    
    def __init__(self, base_url: str = "http://localhost:1234"):
        """
        Initialize LM Studio tools
        
        Args:
            base_url: Base URL of LM Studio server
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 100,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate text using LM Studio
        
        Args:
            prompt: Input prompt
            model: Model name (optional, uses default if not specified)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        try:
            # Get available models
            models_response = await self.client.get(f"{self.base_url}/v1/models")
            models = models_response.json()
            
            # Use first model if none specified
            if not model and models.get("data"):
                model = models["data"][0]["id"]
            
            # Generate completion
            response = await self.client.post(
                f"{self.base_url}/v1/completions",
                json={
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            
            result = response.json()
            return {
                "text": result.get("choices", [{}])[0].get("text", ""),
                "model": model,
                "usage": result.get("usage", {})
            }
        
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
    
    async def chat_completion(
        self,
        messages: list,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate chat completion using LM Studio
        
        Args:
            messages: List of message dictionaries
            model: Model name (optional)
            temperature: Sampling temperature
            
        Returns:
            Chat completion response
        """
        try:
            # Get available models
            models_response = await self.client.get(f"{self.base_url}/v1/models")
            models = models_response.json()
            
            if not model and models.get("data"):
                model = models["data"][0]["id"]
            
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature
                }
            )
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}")
            raise
    
    async def list_models(self) -> list:
        """List available models in LM Studio"""
        try:
            response = await self.client.get(f"{self.base_url}/v1/models")
            models = response.json()
            return models.get("data", [])
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
```

#### 3. Register LM Studio Tools in MCP Server

Add to `src/mcp_server.py`:

```python
from .tools.lm_studio_tools import LMStudioTools

# In __init__:
self.lm_studio = LMStudioTools()

# In _register_tools, add:
if self._is_tool_enabled("lm_studio_generate"):
    tools.append(Tool(
        name="lm_studio_generate",
        description="Generate text using LM Studio",
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Input prompt"},
                "max_tokens": {"type": "integer", "description": "Max tokens"},
                "temperature": {"type": "number", "description": "Temperature"}
            },
            "required": ["prompt"]
        }
    ))

# In call_tool handler:
elif name == "lm_studio_generate":
    result = await self.lm_studio.generate_text(
        arguments["prompt"],
        max_tokens=arguments.get("max_tokens", 100),
        temperature=arguments.get("temperature", 0.7)
    )
    return [{"text": result["text"]}]
```

### Configuration

Add to `config/mcp_config.json`:

```json
{
  "lm_studio": {
    "base_url": "http://localhost:1234",
    "enabled": true
  },
  "tools": {
    "enabled": [
      "lm_studio_generate",
      "lm_studio_chat"
    ]
  }
}
```

### Testing

```bash
# Start LM Studio server first
# Then test the integration
python examples/client_example.py
```

---

## Docker Desktop

Docker Desktop allows you to run MCP servers in containerized environments.

### Prerequisites

- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop/))
- Basic Docker knowledge

### Integration Steps

#### 1. Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY examples/ ./examples/

# Expose MCP server port
EXPOSE 8000

# Run MCP server
CMD ["python", "src/mcp_server.py"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    container_name: mcp-server
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - MCP_HOST=0.0.0.0
      - MCP_PORT=8000
    restart: unless-stopped
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

#### 3. Build and Run

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

#### 4. Using MCP Toolkit in Docker Desktop

1. Open Docker Desktop
2. Navigate to **Extensions** → **MCP Toolkit**
3. Configure your MCP servers
4. Connect clients to containerized servers

### Configuration

For Docker-specific settings, create `config/docker_config.json`:

```json
{
  "docker": {
    "network": "mcp-network",
    "image": "mcp-server:latest",
    "ports": {
      "host": 8000,
      "container": 8000
    }
  }
}
```

---

## Obsidian with Local REST API Plugin

Integrate MCP with Obsidian notes using the Local REST API plugin.

### Prerequisites

- Obsidian installed ([download here](https://obsidian.md/))
- Local REST API plugin installed

### Integration Steps

#### 1. Install Local REST API Plugin

1. Open Obsidian
2. Go to **Settings** → **Community Plugins**
3. Click **Browse** and search for "Local REST API"
4. Install and enable the plugin
5. Go to plugin settings and note:
   - **API Port** (default: `27123`)
   - **API Key** (generate if needed)

#### 2. Create Obsidian Tools

Create `src/tools/obsidian_tools.py`:

```python
"""
Obsidian Integration Tools
"""

import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ObsidianTools:
    """Tools for interacting with Obsidian via Local REST API"""
    
    def __init__(self, base_url: str = "http://localhost:27123", api_key: Optional[str] = None):
        """
        Initialize Obsidian tools
        
        Args:
            base_url: Base URL of Obsidian Local REST API
            api_key: API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)
    
    async def get_note(self, vault: str, file_path: str) -> Dict[str, Any]:
        """
        Get a note from Obsidian
        
        Args:
            vault: Vault name
            file_path: Path to the note file
            
        Returns:
            Note content
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/vault/{vault}/file/{file_path}"
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error getting note: {str(e)}")
            raise
    
    async def create_note(self, vault: str, file_path: str, content: str) -> Dict[str, Any]:
        """
        Create a new note in Obsidian
        
        Args:
            vault: Vault name
            file_path: Path for the new note
            content: Note content
            
        Returns:
            Creation result
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/vault/{vault}/file/{file_path}",
                json={"content": content}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            raise
    
    async def search_notes(self, vault: str, query: str) -> list:
        """
        Search notes in Obsidian
        
        Args:
            vault: Vault name
            query: Search query
            
        Returns:
            List of matching notes
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/vault/{vault}/search",
                params={"query": query}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error searching notes: {str(e)}")
            raise
    
    async def list_vaults(self) -> list:
        """List available Obsidian vaults"""
        try:
            response = await self.client.get(f"{self.base_url}/vaults")
            return response.json()
        except Exception as e:
            logger.error(f"Error listing vaults: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
```

#### 3. Register Obsidian Tools

Add to MCP server configuration and register tools similar to LM Studio integration.

### Configuration

Add to `config/mcp_config.json`:

```json
{
  "obsidian": {
    "base_url": "http://localhost:27123",
    "api_key": "your_api_key_here",
    "default_vault": "MyVault",
    "enabled": true
  }
}
```

---

## Marcel Marais' Obsidian-MCP-Server

Use the dedicated Obsidian MCP server by Marcel Marais.

### Prerequisites

- Node.js installed
- Obsidian with Local REST API plugin
- Git

### Integration Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/MarcelMarais/obsidian-mcp-server.git
cd obsidian-mcp-server
```

#### 2. Install Dependencies

```bash
npm install
```

#### 3. Configure Environment

Create `.env` file:

```env
OBSIDIAN_API_KEY=your_obsidian_api_key
OBSIDIAN_API_BASE_URL=http://localhost:27123
OBSIDIAN_VAULT_PATH=/path/to/your/vault
```

#### 4. Start the Server

```bash
npm start
```

#### 5. Connect to MCP Client

Configure your MCP client (e.g., Claude Desktop) to connect to this server:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "node",
      "args": ["/path/to/obsidian-mcp-server/index.js"],
      "env": {
        "OBSIDIAN_API_KEY": "your_key",
        "OBSIDIAN_API_BASE_URL": "http://localhost:27123"
      }
    }
  }
}
```

### Resources

- [GitHub Repository](https://github.com/MarcelMarais/obsidian-mcp-server)
- [MCP Servers Directory](https://www.mcp-servers.info/)

---

## Logseq

Integrate MCP with Logseq knowledge base.

### Prerequisites

- Logseq installed ([download here](https://logseq.com/))
- Logseq API enabled

### Integration Steps

#### 1. Enable Local API in Logseq

1. Open Logseq
2. Go to **Settings** → **Advanced**
3. Enable **"Enable local API server"**
4. Note the API port (default: `3000`)

#### 2. Create Logseq Tools

Create `src/tools/logseq_tools.py`:

```python
"""
Logseq Integration Tools
"""

import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LogseqTools:
    """Tools for interacting with Logseq"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        """
        Initialize Logseq tools
        
        Args:
            base_url: Base URL of Logseq API
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_page(self, page_name: str) -> Dict[str, Any]:
        """Get a page from Logseq"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/page",
                params={"name": page_name}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error getting page: {str(e)}")
            raise
    
    async def create_page(self, page_name: str, content: str) -> Dict[str, Any]:
        """Create a new page in Logseq"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/page",
                json={"name": page_name, "content": content}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error creating page: {str(e)}")
            raise
    
    async def search(self, query: str) -> list:
        """Search Logseq pages"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/search",
                params={"q": query}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
```

### Configuration

Add to `config/mcp_config.json`:

```json
{
  "logseq": {
    "base_url": "http://localhost:3000",
    "enabled": true
  }
}
```

---

## Cursor

Integrate MCP with Cursor IDE.

### Prerequisites

- Cursor installed ([download here](https://cursor.so/))
- MCP server running

### Integration Steps

#### 1. Configure MCP in Cursor

1. Open Cursor
2. Go to **Settings** → **Tools & Integrations** → **MCP**
3. Click **"Add MCP Server"**
4. Configure server:
   - **Name**: Your server name
   - **Command**: `python`
   - **Args**: `["src/mcp_server.py"]`
   - **Working Directory**: Project root

#### 2. Alternative: Use Cursor Settings File

Edit Cursor settings (JSON):

```json
{
  "mcp": {
    "servers": [
      {
        "name": "mcp-server",
        "command": "python",
        "args": ["src/mcp_server.py"],
        "cwd": "/path/to/mcp-project"
      }
    ]
  }
}
```

#### 3. Test Integration

1. Open a file in Cursor
2. Use Cursor's AI features
3. MCP tools should be available in the AI context

### Resources

- [Cursor Documentation](https://cursor.so/docs)

---

## Claude Sonnet

Integrate MCP with Claude Desktop (Claude Sonnet).

### Prerequisites

- Claude Desktop installed
- MCP server running

### Integration Steps

#### 1. Locate Configuration File

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

#### 2. Edit Configuration

Add MCP server configuration:

```json
{
  "mcpServers": {
    "mcp-example-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/mcp-project/src/mcp_server.py"
      ],
      "cwd": "/absolute/path/to/mcp-project",
      "env": {
        "PYTHONPATH": "/absolute/path/to/mcp-project"
      }
    },
    "obsidian": {
      "command": "node",
      "args": [
        "/path/to/obsidian-mcp-server/index.js"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "your_key",
        "OBSIDIAN_API_BASE_URL": "http://localhost:27123"
      }
    }
  }
}
```

#### 3. Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen Claude Desktop
3. MCP servers should be connected

#### 4. Verify Connection

- Check Claude Desktop logs for MCP connection status
- Try using MCP tools in a conversation

### Troubleshooting

- **Server not connecting**: Check file paths are absolute
- **Import errors**: Ensure PYTHONPATH is set correctly
- **Permission errors**: Check file permissions

---

## Cloud Server Setup

Deploy MCP server on cloud infrastructure.

### Prerequisites

- Cloud provider account (AWS, Azure, GCP, DigitalOcean, etc.)
- SSH access to server
- Basic server administration knowledge

### Integration Steps

#### 1. Choose Cloud Provider

Popular options:
- **AWS EC2**
- **DigitalOcean Droplet**
- **Google Cloud Compute Engine**
- **Azure Virtual Machine**
- **Linode**

#### 2. Provision Server

**Example: DigitalOcean**

1. Create a new Droplet
2. Choose Ubuntu 22.04 LTS
3. Select size (minimum 2GB RAM recommended)
4. Add SSH key
5. Create droplet

#### 3. Server Setup

```bash
# SSH into server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install -y python3 python3-pip python3-venv git

# Install Node.js (if needed)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Clone your MCP project
git clone https://github.com/yourusername/mcp-project.git
cd mcp-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 4. Configure Firewall

```bash
# Allow SSH
ufw allow 22/tcp

# Allow MCP server port
ufw allow 8000/tcp

# Enable firewall
ufw enable
```

#### 5. Set Up Process Manager

**Using systemd:**

Create `/etc/systemd/system/mcp-server.service`:

```ini
[Unit]
Description=MCP Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/mcp-project
Environment="PATH=/path/to/mcp-project/venv/bin"
ExecStart=/path/to/mcp-project/venv/bin/python src/mcp_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl enable mcp-server
systemctl start mcp-server
systemctl status mcp-server
```

#### 6. Configure Reverse Proxy (Optional)

**Using Nginx:**

```bash
apt install -y nginx
```

Create `/etc/nginx/sites-available/mcp-server`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:

```bash
ln -s /etc/nginx/sites-available/mcp-server /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 7. Set Up SSL (Optional)

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

### Configuration

Update `config/mcp_config.json` for cloud deployment:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "security": {
    "api_key_required": true,
    "allowed_ips": []
  }
}
```

### Monitoring

Set up monitoring with tools like:
- **PM2** (for Node.js)
- **Supervisor** (for Python)
- **systemd** (built-in)
- **Cloud provider monitoring**

---

## Troubleshooting

### Common Issues

#### LM Studio Not Connecting

- **Issue**: Cannot connect to LM Studio API
- **Solution**: 
  - Verify LM Studio server is running
  - Check port number (default: 1234)
  - Ensure CORS is enabled
  - Check firewall settings

#### Obsidian API Errors

- **Issue**: 401 Unauthorized
- **Solution**:
  - Verify API key is correct
  - Check API key in Obsidian plugin settings
  - Ensure plugin is enabled

#### Docker Container Issues

- **Issue**: Container won't start
- **Solution**:
  - Check Docker logs: `docker-compose logs`
  - Verify port mappings
  - Check volume mounts
  - Ensure Docker Desktop is running

#### Claude Desktop Not Connecting

- **Issue**: MCP server not appearing
- **Solution**:
  - Use absolute paths in config
  - Check JSON syntax
  - Verify Python path
  - Check Claude Desktop logs

#### Cloud Server Connection Issues

- **Issue**: Cannot access server remotely
- **Solution**:
  - Check firewall rules
  - Verify security groups
  - Test with curl: `curl http://your-server-ip:8000`
  - Check server logs

### Getting Help

- Check tool-specific documentation
- Review MCP server logs
- Test API endpoints directly
- Verify network connectivity
- Check authentication credentials

---

## Additional Resources

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Servers Directory](https://www.mcp-servers.info/)
- [Claude Desktop MCP Guide](https://claude.ai/docs/mcp)

---

**Last Updated**: 2025-01-27

