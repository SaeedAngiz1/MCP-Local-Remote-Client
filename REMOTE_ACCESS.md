# Remote Access to LM Studio via Tailscale and A-Shell

This guide explains how to set up remote access to LM Studio running on your computer from your iPhone or Android device using Tailscale (for secure networking) and A-Shell (iOS) or Termux (Android) for terminal access.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step 1: Install Tailscale](#step-1-install-tailscale)
- [Step 2: Configure Tailscale](#step-2-configure-tailscale)
- [Step 3: Set Up LM Studio](#step-3-set-up-lm-studio)
- [Step 4: Install Terminal Apps](#step-4-install-terminal-apps)
- [Step 5: Access LM Studio Remotely](#step-5-access-lm-studio-remotely)
- [Step 6: Create MCP Integration](#step-6-create-mcp-integration)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Alternative Methods](#alternative-methods)

---

## Overview

This setup allows you to:
- Access LM Studio running on your computer from anywhere
- Use your iPhone or Android device to interact with local LLMs
- Securely connect via Tailscale's encrypted VPN
- Control LM Studio through terminal commands
- Integrate with MCP for AI assistant access

**Architecture:**
```
iPhone/Android → Tailscale VPN → Your Computer → LM Studio (localhost:1234)
```

---

## Prerequisites

Before starting, ensure you have:

- ✅ **Computer Requirements:**
  - LM Studio installed and running
  - Internet connection
  - Administrator/root access (for Tailscale installation)

- ✅ **Mobile Device Requirements:**
  - iPhone or Android device
  - Internet connection
  - App Store or Google Play Store access

- ✅ **Accounts:**
  - Tailscale account (free tier works)
  - Apple ID (for iOS) or Google Account (for Android)

---

## Step 1: Install Tailscale

### On Your Computer

#### Windows

1. **Download Tailscale**
   - Visit [tailscale.com/download](https://tailscale.com/download)
   - Download the Windows installer
   - Run the installer and follow the setup wizard

2. **Sign In**
   - Click "Sign in" in the Tailscale app
   - Choose your authentication method (Google, Microsoft, GitHub, etc.)
   - Complete the sign-in process

3. **Verify Connection**
   - The Tailscale icon should appear in your system tray
   - Right-click the icon to see your device's Tailscale IP address
   - Note this IP address (e.g., `100.x.x.x`)

#### macOS

1. **Install via Homebrew** (recommended):
   ```bash
   brew install tailscale
   ```

2. **Or Download Installer:**
   - Visit [tailscale.com/download](https://tailscale.com/download)
   - Download the macOS installer
   - Open the `.dmg` file and drag Tailscale to Applications

3. **Start Tailscale:**
   ```bash
   sudo tailscale up
   ```

4. **Sign In:**
   - Follow the authentication link in the terminal
   - Complete sign-in in your browser

#### Linux

1. **Install Tailscale:**
   ```bash
   # For Ubuntu/Debian
   curl -fsSL https://tailscale.com/install.sh | sh
   
   # Or for other distributions, see tailscale.com/download
   ```

2. **Start Tailscale:**
   ```bash
   sudo tailscale up
   ```

3. **Sign In:**
   - Follow the authentication link
   - Complete sign-in process

4. **Check Status:**
   ```bash
   tailscale status
   tailscale ip -4
   ```

### On Your Mobile Device

#### iPhone/iPad

1. **Install Tailscale App**
   - Open the App Store
   - Search for "Tailscale"
   - Install the official Tailscale app

2. **Sign In**
   - Open the Tailscale app
   - Tap "Sign in"
   - Use the same account you used on your computer
   - Complete authentication

3. **Verify Connection**
   - The app should show "Connected"
   - Note your computer's Tailscale IP address

#### Android

1. **Install Tailscale App**
   - Open Google Play Store
   - Search for "Tailscale"
   - Install the official Tailscale app

2. **Sign In**
   - Open the Tailscale app
   - Tap "Log in"
   - Use the same account as your computer
   - Complete authentication

3. **Verify Connection**
   - Check that your computer appears in the device list
   - Note your computer's Tailscale IP address

---

## Step 2: Configure Tailscale

### Verify Network Connectivity

#### On Your Computer

1. **Check Tailscale IP:**
   ```bash
   # Windows (PowerShell)
   tailscale ip -4
   
   # macOS/Linux
   tailscale ip -4
   ```

2. **Test Connectivity:**
   ```bash
   # Ping your mobile device's Tailscale IP
   ping <mobile-device-ip>
   ```

#### On Your Mobile Device

1. **Find Your Computer's IP:**
   - Open Tailscale app
   - Find your computer in the device list
   - Note the IP address (starts with `100.`)

2. **Test Connection:**
   - Use a network tool app to ping your computer
   - Or proceed to terminal access

### Configure Firewall (If Needed)

#### Windows

1. **Allow Tailscale in Firewall:**
   - Open Windows Defender Firewall
   - Ensure Tailscale is allowed through firewall
   - Or temporarily disable firewall for testing

#### macOS

```bash
# Allow Tailscale through firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/Tailscale.app
```

#### Linux

```bash
# If using UFW
sudo ufw allow 41641/udp  # Tailscale
sudo ufw allow 22/tcp     # SSH (if needed)
```

---

## Step 3: Set Up LM Studio

### Configure LM Studio for Remote Access

1. **Open LM Studio**
   - Launch LM Studio on your computer

2. **Enable Local Server:**
   - Go to **Settings** → **Local Server** tab
   - Enable **"Serve on Local Host"**
   - Set port to `1234` (default)
   - Enable **"Enable CORS"** (important for remote access)
   - Click **"Start Server"**

3. **Verify Server is Running:**
   - Open a browser on your computer
   - Navigate to `http://localhost:1234`
   - You should see the LM Studio API interface

4. **Test API Endpoint:**
   ```bash
   # On your computer, test the API
   curl http://localhost:1234/v1/models
   ```

### Configure LM Studio to Accept Remote Connections

**Important**: By default, LM Studio only accepts localhost connections. To allow Tailscale connections:

1. **Check LM Studio Settings:**
   - Some versions allow binding to `0.0.0.0` (all interfaces)
   - Check if there's a "Bind to" or "Listen on" setting
   - If available, set to `0.0.0.0` or your Tailscale IP

2. **Alternative: Use SSH Tunneling** (see Step 5)

---

## Step 4: Install Terminal Apps

### iPhone/iPad: Install A-Shell

1. **Install A-Shell:**
   - Open the App Store
   - Search for "A-Shell"
   - Install the app by Nicolas Holzschuch

2. **Open A-Shell:**
   - Launch the app
   - You'll see a terminal interface

3. **Install Required Tools** (optional):
   ```bash
   # A-Shell comes with curl, but you may need to install additional tools
   # Check available commands with:
   which curl
   which ssh
   ```

### Android: Install Termux

1. **Install Termux:**
   - Open Google Play Store
   - Search for "Termux"
   - Install the official Termux app
   - **Note**: If Termux is not available, try F-Droid

2. **Open Termux:**
   - Launch the app
   - Grant necessary permissions

3. **Update Packages:**
   ```bash
   pkg update
   pkg upgrade
   ```

4. **Install Required Tools:**
   ```bash
   pkg install curl openssh
   ```

---

## Step 5: Access LM Studio Remotely

### Method 1: Direct API Access (If LM Studio Allows Remote Connections)

#### On iPhone (A-Shell)

1. **Get Your Computer's Tailscale IP:**
   - Open Tailscale app
   - Find your computer
   - Note the IP (e.g., `100.64.1.2`)

2. **Test Connection:**
   ```bash
   # In A-Shell, test the connection
   curl http://100.64.1.2:1234/v1/models
   ```

3. **Make API Calls:**
   ```bash
   # Generate text
   curl -X POST http://100.64.1.2:1234/v1/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "your-model",
       "prompt": "Hello, world!",
       "max_tokens": 50
     }'
   ```

#### On Android (Termux)

1. **Get Your Computer's Tailscale IP:**
   - Open Tailscale app
   - Find your computer
   - Note the IP address

2. **Test Connection:**
   ```bash
   curl http://100.64.1.2:1234/v1/models
   ```

3. **Make API Calls:**
   ```bash
   # Same as iPhone example above
   curl -X POST http://100.64.1.2:1234/v1/completions \
     -H "Content-Type: application/json" \
     -d '{"model": "your-model", "prompt": "Hello!", "max_tokens": 50}'
   ```

### Method 2: SSH Tunneling (Recommended)

If LM Studio only accepts localhost connections, use SSH tunneling:

#### Set Up SSH on Your Computer

**Windows:**

1. **Enable OpenSSH Server:**
   - Open Settings → Apps → Optional Features
   - Add "OpenSSH Server"
   - Start the service:
     ```powershell
     Start-Service sshd
     Set-Service -Name sshd -StartupType 'Automatic'
     ```

2. **Configure SSH:**
   - Edit `C:\ProgramData\ssh\sshd_config`
   - Ensure `PasswordAuthentication yes` (or use SSH keys)
   - Restart service: `Restart-Service sshd`

**macOS/Linux:**

SSH is usually pre-installed. Ensure it's running:

```bash
# Check if SSH is running
sudo systemctl status ssh  # Linux
# or
sudo launchctl list | grep sshd  # macOS

# Start SSH if needed
sudo systemctl start ssh  # Linux
sudo systemctl enable ssh  # Linux
```

#### Create SSH Tunnel from Mobile Device

**On iPhone (A-Shell):**

1. **SSH into Your Computer:**
   ```bash
   # Replace with your computer's Tailscale IP and username
   ssh username@100.64.1.2
   ```

2. **Create Port Forward (Alternative - if A-Shell supports it):**
   ```bash
   # Some versions of A-Shell support port forwarding
   # Check documentation for your version
   ```

**On Android (Termux):**

1. **Create SSH Tunnel:**
   ```bash
   # Forward local port 1234 to remote LM Studio
   ssh -L 1234:localhost:1234 username@100.64.1.2 -N
   ```

2. **In Another Termux Session, Access LM Studio:**
   ```bash
   # Now LM Studio is accessible on localhost:1234
   curl http://localhost:1234/v1/models
   ```

### Method 3: Using MCP Integration (Best for AI Assistants)

See Step 6 below for MCP integration, which provides a cleaner interface.

---

## Step 6: Create MCP Integration

Create an MCP tool that connects to LM Studio via Tailscale.

### Update LM Studio Tools for Remote Access

Edit `src/tools/lm_studio_tools.py`:

```python
"""
LM Studio Integration Tools with Remote Access Support
"""

import httpx
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class LMStudioTools:
    """Tools for interacting with LM Studio (local or remote)"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize LM Studio tools
        
        Args:
            base_url: Base URL of LM Studio server
                     Defaults to localhost or Tailscale IP from config
        """
        if base_url is None:
            # Try to get from environment or config
            base_url = os.getenv(
                "LM_STUDIO_URL",
                os.getenv("TAILSCALE_LM_STUDIO_URL", "http://localhost:1234")
            )
        
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
        logger.info(f"LM Studio Tools initialized with URL: {base_url}")
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 100,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate text using LM Studio (works with remote access)"""
        try:
            # Get available models
            models_response = await self.client.get(f"{self.base_url}/v1/models")
            models = models_response.json()
            
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
        
        except httpx.ConnectError:
            logger.error(f"Cannot connect to LM Studio at {self.base_url}")
            raise Exception(
                f"Cannot connect to LM Studio. "
                f"Ensure it's running and accessible at {self.base_url}. "
                f"If using Tailscale, verify the connection."
            )
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
    
    # ... (rest of the methods from INTEGRATIONS.md)
```

### Configuration for Remote Access

Update `config/mcp_config.json`:

```json
{
  "lm_studio": {
    "base_url": "http://100.64.1.2:1234",
    "enabled": true,
    "remote_access": {
      "enabled": true,
      "tailscale_ip": "100.64.1.2",
      "port": 1234
    }
  }
}
```

### Environment Variables

Create `.env` file (optional):

```env
# LM Studio Configuration
LM_STUDIO_URL=http://100.64.1.2:1234
TAILSCALE_LM_STUDIO_URL=http://100.64.1.2:1234

# Or use localhost if accessing via SSH tunnel
# LM_STUDIO_URL=http://localhost:1234
```

### Test Remote MCP Connection

1. **On Your Mobile Device:**
   - Ensure Tailscale is connected
   - Note your computer's Tailscale IP

2. **Update MCP Configuration:**
   - Set the Tailscale IP in config
   - Restart MCP server

3. **Test from Mobile:**
   ```bash
   # If you have MCP client on mobile (future feature)
   # Or test via API
   curl http://100.64.1.2:1234/v1/models
   ```

---

## Troubleshooting

### Tailscale Connection Issues

**Problem**: Devices not connecting

**Solutions**:
- Ensure both devices are signed in to the same Tailscale account
- Check Tailscale status: `tailscale status`
- Restart Tailscale on both devices
- Verify internet connectivity on both devices
- Check Tailscale admin console: [admin.tailscale.com](https://admin.tailscale.com)

### LM Studio Not Accessible

**Problem**: Cannot connect to LM Studio from mobile device

**Solutions**:
- Verify LM Studio server is running on your computer
- Check if LM Studio is bound to `localhost` only (use SSH tunnel if so)
- Test connection from computer first: `curl http://localhost:1234/v1/models`
- Try accessing via Tailscale IP: `curl http://100.64.1.2:1234/v1/models`
- Check firewall settings on your computer
- Verify Tailscale IP is correct

### SSH Connection Issues

**Problem**: Cannot SSH into computer

**Solutions**:
- Verify SSH service is running on your computer
- Check SSH port (default: 22) is open in firewall
- Ensure username is correct
- Try password authentication if key-based auth fails
- Check SSH logs on your computer

### A-Shell/Termux Issues

**Problem**: Terminal app not working

**Solutions**:
- **A-Shell**: Update to latest version from App Store
- **Termux**: Run `pkg update && pkg upgrade`
- Grant necessary permissions to the app
- Check if curl/ssh are installed: `which curl`

### API Timeout Issues

**Problem**: Requests timing out

**Solutions**:
- Increase timeout in HTTP client
- Check network latency via Tailscale
- Ensure LM Studio model is loaded and ready
- Try smaller requests first
- Check LM Studio logs for errors

---

## Security Considerations

### Tailscale Security

✅ **Tailscale provides:**
- End-to-end encryption
- Automatic key rotation
- No exposed ports to internet
- Access control via Tailscale admin console

### Best Practices

1. **Use Strong Authentication:**
   - Enable 2FA on Tailscale account
   - Use SSH keys instead of passwords

2. **Limit Access:**
   - Only allow necessary devices in Tailscale network
   - Use Tailscale ACLs to restrict access if needed

3. **LM Studio Security:**
   - Don't expose LM Studio to public internet
   - Use Tailscale for secure access only
   - Consider API key authentication if available

4. **Monitor Access:**
   - Check Tailscale admin console regularly
   - Review connected devices
   - Remove unused devices

5. **Keep Software Updated:**
   - Update Tailscale regularly
   - Update LM Studio
   - Update mobile apps

---

## Alternative Methods

### Method 1: ngrok (Alternative to Tailscale)

If you prefer ngrok for tunneling:

```bash
# Install ngrok
# On your computer
ngrok http 1234

# Use the provided URL on mobile device
```

**Note**: ngrok exposes services to public internet (less secure than Tailscale).

### Method 2: Cloudflare Tunnel

Similar to ngrok but using Cloudflare:

```bash
# Install cloudflared
cloudflared tunnel --url http://localhost:1234
```

### Method 3: WireGuard VPN

Set up your own WireGuard VPN (more complex but more control).

### Method 4: Direct Port Forwarding

If you have a static IP and router access:
- Forward port 1234 to your computer
- Access via public IP (not recommended for security)

---

## Quick Reference

### Tailscale Commands

```bash
# Check status
tailscale status

# Get IP address
tailscale ip -4

# Ping device
tailscale ping <device-name>

# Check connection
tailscale ping <tailscale-ip>
```

### LM Studio API Endpoints

```bash
# List models
curl http://<ip>:1234/v1/models

# Generate text
curl -X POST http://<ip>:1234/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "model-name", "prompt": "Hello", "max_tokens": 50}'

# Chat completion
curl -X POST http://<ip>:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "model-name", "messages": [{"role": "user", "content": "Hello"}]}'
```

### SSH Tunnel Command

```bash
# Forward local port to remote LM Studio
ssh -L 1234:localhost:1234 username@<tailscale-ip> -N
```

---

## Additional Resources

- [Tailscale Documentation](https://tailscale.com/kb/)
- [LM Studio Documentation](https://lmstudio.ai/docs)
- [A-Shell GitHub](https://github.com/holzschu/a-shell)
- [Termux Wiki](https://wiki.termux.com/)
- [MCP Documentation](https://modelcontextprotocol.io)

---

**Last Updated**: 2025-01-27

**Note**: This setup provides secure remote access to LM Studio. Always follow security best practices and keep your software updated.

