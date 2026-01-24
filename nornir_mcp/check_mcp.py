
import sys
import json
import urllib.request
import urllib.error


def check_get_interfaces(host="localhost", port=8000, device="SW1"):
    # Append a static session ID to satisfy the MCP server requirement
    url = f"http://{host}:{port}/mcp?sessionId=cli-verify-session"
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_interfaces",
            "arguments": {
                "device_name": device
            }
        },
        "id": 1
    }
    

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
    )
    
    print(f"Sending request to {url}:")
    print(json.dumps(payload, indent=2))
    print("-" * 40)
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = response.read().decode("utf-8")
            print("Response Status:", response.status)
            try:
                parsed = json.loads(resp_data)
                print("Response Body:")
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("Response Body (Raw):")
                print(resp_data)
                
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Connection Error: {e.reason}")
        print("Make sure the Docker container is running and port 8000 is mapped.")

if __name__ == "__main__":
    device = sys.argv[1] if len(sys.argv) > 1 else "SW1"
    check_get_interfaces(device=device)
