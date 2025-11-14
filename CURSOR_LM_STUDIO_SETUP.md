# Connecting LM Studio with Cursor via MCP

This guide shows you how to connect LM Studio to Cursor so I (the AI assistant) can use your local LLMs.

## Prerequisites

✅ **LM Studio installed and running**
✅ **A model loaded in LM Studio**
✅ **MCP server configured** (already done!)
✅ **Cursor IDE** (you're using it now)

## Step 1: Start LM Studio Server

1. **Open LM Studio**
2. **Load a Model**
   - Go to the "Chat" or "Models" tab
   - Select and load a model (e.g., Llama 2, Mistral, etc.)
   - Wait for the model to load completely

3. **Enable Local Server**
   - Click on the **"Local Server"** tab (or go to Settings → Local Server)
   - Enable **"Serve on Local Host"**
   - Set port to **1234** (default)
   - Enable **"Enable CORS"** (important!)
   - Click **"Start Server"**

4. **Verify Server is Running**
   - You should see "Server is running" message
   - The status should show "Active"
   - You can test it by opening: `http://localhost:1234` in your browser

## Step 2: Verify MCP Server Configuration

The MCP server is already configured! Check `config/mcp_config.json`:

```json
{
  "lm_studio": {
    "enabled": true,
    "base_url": "http://localhost:1234"
  },
  "tools": {
    "enabled": [
      "lm_studio_generate",
      "lm_studio_chat",
      "lm_studio_list_models",
      "lm_studio_test_connection"
    ]
  }
}
```

## Step 3: Test MCP Server Connection

### Option A: Test with Python Script

Create a test file `test_lm_studio.py`:

```python
import asyncio
import sys
sys.path.insert(0, '.')

from src.tools.lm_studio_tools import LMStudioTools

async def test():
    tools = LMStudioTools()
    
    # Test connection
    print("Testing LM Studio connection...")
    status = await tools.test_connection()
    print(f"Status: {status}")
    
    # List models
    print("\nListing models...")
    models = await tools.list_models()
    print(f"Models: {models}")
    
    # Test generation
    if status["status"] == "connected":
        print("\nTesting text generation...")
        result = await tools.generate_text("Hello, world!", max_tokens=50)
        print(f"Generated: {result['text']}")
    
    await tools.close()

if __name__ == "__main__":
    asyncio.run(test())
```

Run it:

```cmd
python test_lm_studio.py
```

### Option B: Test MCP Server Directly

```cmd
python src\mcp_server.py
```

The server should start without errors if LM Studio is running.

## Step 4: Connect Cursor to MCP Server

### Method 1: Configure Cursor Settings (Recommended)

1. **Open Cursor Settings**
   - Press `Ctrl+,` (or `Cmd+,` on Mac)
   - Or go to File → Preferences → Settings

2. **Enable MCP**
   - Search for "MCP" in settings
   - Enable MCP integration if available

3. **Add MCP Server Configuration**

   Cursor uses a configuration file. Create or edit:

   **Windows:**
   ```
   %APPDATA%\Cursor\User\globalStorage\mcp.json
   ```

   **macOS:**
   ```
   ~/Library/Application Support/Cursor/User/globalStorage/mcp.json
   ```

   **Linux:**
   ```
   ~/.config/Cursor/User/globalStorage/mcp.json
   ```

   Add this configuration:

   ```json
   {
     "mcpServers": {
       "mcp-example-server": {
         "command": "python",
         "args": [
           "C:\\Users\\angiz\\OneDrive\\Desktop\\cursor\\src\\mcp_server.py"
         ],
         "cwd": "C:\\Users\\angiz\\OneDrive\\Desktop\\cursor",
         "env": {
           "PYTHONPATH": "C:\\Users\\angiz\\OneDrive\\Desktop\\cursor"
         }
       }
     }
   }
   ```

   **Important**: Replace the paths with your actual project path!

4. **Restart Cursor**
   - Close Cursor completely
   - Reopen Cursor
   - MCP server should connect automatically

### Method 2: Use Cursor's MCP Extension

1. **Install MCP Extension** (if available)
   - Open Extensions (Ctrl+Shift+X)
   - Search for "MCP" or "Model Context Protocol"
   - Install the extension

2. **Configure Extension**
   - Open extension settings
   - Add your MCP server configuration
   - Point to `src/mcp_server.py`

## Step 5: Verify Connection

Once connected, I (the AI assistant) should be able to:

1. **Test LM Studio Connection**
   - Ask me: "Test the LM Studio connection"
   - I'll use the `lm_studio_test_connection` tool

2. **List Available Models**
   - Ask me: "What models are available in LM Studio?"
   - I'll use the `lm_studio_list_models` tool

3. **Generate Text**
   - Ask me: "Generate some text using LM Studio with the prompt 'Tell me a joke'"
   - I'll use the `lm_studio_generate` tool

4. **Chat with LM Studio**
   - Ask me: "Have a conversation with LM Studio about Python programming"
   - I'll use the `lm_studio_chat` tool

## Troubleshooting

### Issue: "Cannot connect to LM Studio"

**Solutions:**
1. Make sure LM Studio is running
2. Verify the server is started (Local Server tab shows "Active")
3. Check the port is 1234 (default)
4. Ensure CORS is enabled
5. Test the API directly: `curl http://localhost:1234/v1/models`

### Issue: "MCP server not connecting in Cursor"

**Solutions:**
1. Check the paths in the configuration file are correct (use absolute paths)
2. Verify Python is in your PATH
3. Make sure the virtual environment is activated (if using one)
4. Check Cursor's logs for errors
5. Restart Cursor after configuration changes

### Issue: "Module not found" errors

**Solutions:**
1. Make sure you're in the project directory
2. Activate virtual environment: `venv\Scripts\activate.bat`
3. Install dependencies: `pip install -r requirements.txt`
4. Check PYTHONPATH in the configuration

### Issue: "LM Studio tools not appearing"

**Solutions:**
1. Verify `lm_studio.enabled` is `true` in `config/mcp_config.json`
2. Check tools are enabled in the config
3. Restart the MCP server
4. Check server logs for errors

## Quick Test Commands

Test LM Studio API directly:

```cmd
REM Test if server is running
curl http://localhost:1234/v1/models

REM Test text generation
curl -X POST http://localhost:1234/v1/completions -H "Content-Type: application/json" -d "{\"model\": \"your-model\", \"prompt\": \"Hello\", \"max_tokens\": 50}"
```

Test MCP server:

```cmd
python src\mcp_server.py
```

## What You Can Do Now

Once connected, you can ask me to:

- ✅ Generate text using your local LLM
- ✅ Have conversations with LM Studio
- ✅ List available models
- ✅ Test connections
- ✅ Use LM Studio for code generation, writing, analysis, etc.

## Example Prompts

Try these once everything is set up:

1. **"Test the LM Studio connection"**
2. **"What models do I have loaded in LM Studio?"**
3. **"Generate a Python function to calculate fibonacci numbers using LM Studio"**
4. **"Ask LM Studio to explain machine learning in simple terms"**
5. **"Use LM Studio to write a short story about AI"**

---

## Remote Access: Using LM Studio from iPhone via A-Shell

This section explains how to access LM Studio running on your computer from your iPhone using Tailscale (for secure networking) and A-Shell (for terminal access).

### Overview

With this setup, you can:
- ✅ Access LM Studio from your iPhone anywhere
- ✅ Use A-Shell to interact with LM Studio remotely
- ✅ Securely connect via Tailscale's encrypted VPN
- ✅ Test LM Studio API calls from your iPhone
- ✅ Use MCP tools remotely via A-Shell

**Architecture:**
```
iPhone → A-Shell → Tailscale VPN → Your Computer → LM Studio (localhost:1234)
```

### Prerequisites

- ✅ **Computer:** LM Studio running with local server enabled
- ✅ **iPhone:** A-Shell app installed (from App Store)
- ✅ **Both devices:** Tailscale installed and connected to the same account
- ✅ **Internet connection** on both devices

### Step 1: Install Tailscale

#### On Your Computer (Windows)

1. **Download Tailscale**
   - Visit [tailscale.com/download](https://tailscale.com/download)
   - Download and install the Windows version
   - Run the installer

2. **Sign In**
   - Open Tailscale app
   - Click "Sign in"
   - Choose authentication method (Google, Microsoft, GitHub, etc.)
   - Complete sign-in

3. **Get Your Tailscale IP**
   - Right-click Tailscale icon in system tray
   - Note your Tailscale IP (e.g., `100.64.1.2`)
   - Or run in CMD: `tailscale ip -4`

#### On Your iPhone

1. **Install Tailscale App**
   - Open App Store
   - Search for "Tailscale"
   - Install the official Tailscale app

2. **Sign In**
   - Open Tailscale app
   - Tap "Sign in"
   - Use the **same account** as your computer
   - Complete authentication

3. **Verify Connection**
   - App should show "Connected"
   - Find your computer in the device list
   - Note your computer's Tailscale IP address

### Step 2: Install A-Shell on iPhone

1. **Install A-Shell**
   - Open App Store on iPhone
   - Search for "A-Shell"
   - Install the app by Nicolas Holzschuch

2. **Open A-Shell**
   - Launch A-Shell
   - You'll see a terminal interface

3. **Verify Tools Available**
   - A-Shell comes with `curl` pre-installed
   - Check with: `which curl`

### Step 3: Configure LM Studio for Remote Access

1. **Start LM Studio Server** (on your computer)
   - Enable "Serve on Local Host"
   - Set port to `1234`
   - Enable "Enable CORS"
   - Click "Start Server"

2. **Note Your Computer's Tailscale IP**
   - From Tailscale app on computer or iPhone
   - Example: `100.64.1.2`

### Step 4: Access LM Studio from iPhone

#### Method 1: Direct API Access (Recommended)

If LM Studio accepts connections from Tailscale network:

1. **Open A-Shell on iPhone**

2. **Test Connection**
   ```bash
   # Replace 100.64.1.2 with your computer's Tailscale IP
   curl http://100.64.1.2:1234/v1/models
   ```

3. **List Available Models**
   ```bash
   curl http://100.64.1.2:1234/v1/models
   ```

4. **Generate Text**
   ```bash
   curl -X POST http://100.64.1.2:1234/v1/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "your-model-name",
       "prompt": "Hello, world!",
       "max_tokens": 50
     }'
   ```

5. **Chat Completion**
   ```bash
   curl -X POST http://100.64.1.2:1234/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "your-model-name",
       "messages": [
         {"role": "user", "content": "What is Python?"}
       ],
       "max_tokens": 100
     }'
   ```

#### Method 2: SSH Tunneling (If Direct Access Doesn't Work)

If LM Studio only accepts localhost connections:

1. **Enable SSH on Your Computer**

   **Windows:**
   - Open Settings → Apps → Optional Features
   - Add "OpenSSH Server"
   - Start service: `Start-Service sshd`
   - Set startup: `Set-Service -Name sshd -StartupType 'Automatic'`

2. **SSH into Your Computer from A-Shell**
   ```bash
   # Replace with your computer's Tailscale IP and username
   ssh username@100.64.1.2
   ```

3. **Access LM Studio via SSH**
   - Once connected via SSH, you can access LM Studio as if you're on the computer
   - Use `curl http://localhost:1234/v1/models` from SSH session

### Step 5: Update MCP Configuration for Remote Access

If you want to use MCP tools remotely, update the configuration:

1. **Update `config/mcp_config.json`** (on your computer)

   For direct access via Tailscale:
   ```json
   {
     "lm_studio": {
       "enabled": true,
       "base_url": "http://100.64.1.2:1234"
     }
   }
   ```

   **Note:** This allows remote access from your iPhone's Tailscale IP as well.

2. **Create Remote Access Script** (optional)

   Create `test_remote_lm_studio.py` on your computer:
   ```python
   import asyncio
   from src.tools.lm_studio_tools import LMStudioTools
   
   async def test():
       # Use Tailscale IP instead of localhost
       tools = LMStudioTools(base_url="http://100.64.1.2:1234")
       
       status = await tools.test_connection()
       print(f"Status: {status}")
       
       if status["status"] == "connected":
           result = await tools.generate_text("Hello from iPhone!", max_tokens=50)
           print(f"Generated: {result['text']}")
       
       await tools.close()
   
   asyncio.run(test())
   ```

### Step 6: Using A-Shell to Test MCP Connection

From A-Shell on iPhone, you can test the MCP server:

1. **SSH into Your Computer**
   ```bash
   ssh username@100.64.1.2
   ```

2. **Navigate to Project Directory**
   ```bash
   cd "C:\Users\angiz\OneDrive\Desktop\cursor"
   ```

3. **Test LM Studio Connection**
   ```bash
   python test_lm_studio.py
   ```

4. **Run MCP Server** (if needed)
   ```bash
   python src\mcp_server.py
   ```

### Troubleshooting Remote Access

#### Issue: Cannot connect to LM Studio from iPhone

**Solutions:**
1. ✅ Verify Tailscale is connected on both devices
2. ✅ Check your computer's Tailscale IP is correct
3. ✅ Ensure LM Studio server is running
4. ✅ Test connection: `curl http://100.64.1.2:1234/v1/models`
5. ✅ Check firewall settings on computer (allow port 1234)
6. ✅ Verify CORS is enabled in LM Studio

#### Issue: Connection timeout

**Solutions:**
1. ✅ Check internet connection on both devices
2. ✅ Verify Tailscale shows both devices as connected
3. ✅ Try pinging your computer from iPhone: `ping 100.64.1.2`
4. ✅ Restart Tailscale on both devices
5. ✅ Check LM Studio is still running

#### Issue: LM Studio only accepts localhost

**Solutions:**
1. ✅ Use SSH tunneling method (see Step 4, Method 2)
2. ✅ Or configure LM Studio to bind to `0.0.0.0` (if available)
3. ✅ Use SSH port forwarding from A-Shell

#### Issue: A-Shell curl not working

**Solutions:**
1. ✅ Update A-Shell to latest version
2. ✅ Check curl is installed: `which curl`
3. ✅ Try using full path: `/usr/bin/curl`
4. ✅ Test with simple request: `curl https://www.google.com`

### Security Considerations

1. **Tailscale Security**
   - ✅ Tailscale uses end-to-end encryption
   - ✅ Only devices in your Tailscale network can access
   - ✅ No exposed ports to public internet
   - ✅ Enable 2FA on Tailscale account

2. **Best Practices**
   - ✅ Keep Tailscale updated
   - ✅ Use strong authentication
   - ✅ Only allow trusted devices
   - ✅ Monitor connected devices regularly
   - ✅ Don't share Tailscale credentials

3. **LM Studio Security**
   - ✅ Don't expose LM Studio to public internet
   - ✅ Use Tailscale for secure access only
   - ✅ Consider API key authentication (if available)
   - ✅ Monitor API usage

### Quick Reference Commands

**From A-Shell on iPhone:**

```bash
# Test Tailscale connection
ping 100.64.1.2

# Test LM Studio connection
curl http://100.64.1.2:1234/v1/models

# Generate text
curl -X POST http://100.64.1.2:1234/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "model-name", "prompt": "Hello", "max_tokens": 50}'

# SSH into computer
ssh username@100.64.1.2

# Test from SSH session
curl http://localhost:1234/v1/models
```

**From Computer (Windows CMD):**

```cmd
REM Get Tailscale IP
tailscale ip -4

REM Test LM Studio locally
curl http://localhost:1234/v1/models

REM Check Tailscale status
tailscale status
```

### Example Use Cases

1. **Test LM Studio Remotely**
   - Use A-Shell to test LM Studio API from anywhere
   - Verify models are loaded
   - Test text generation

2. **Access MCP Tools Remotely**
   - SSH into computer
   - Run MCP server
   - Use LM Studio tools via MCP

3. **Debug Issues**
   - Access computer remotely
   - Check LM Studio logs
   - Test connections

4. **Mobile Development**
   - Test API endpoints from iPhone
   - Verify remote access works
   - Develop mobile integrations

---

**Need More Help?**

- Check [REMOTE_ACCESS.md](REMOTE_ACCESS.md) for detailed remote access guide
- See [INTEGRATIONS.md](INTEGRATIONS.md) for more integration options
- Tailscale documentation: [tailscale.com/kb](https://tailscale.com/kb)
- A-Shell documentation: Check App Store description

---

**Need Help?** Check the main [INTEGRATIONS.md](INTEGRATIONS.md) guide for more details.

**Ready to go!** Once LM Studio is running and Cursor is connected, I'll be able to use your local LLMs! 🚀

**Remote Access Ready!** Now you can access LM Studio from your iPhone using A-Shell and Tailscale! 📱

