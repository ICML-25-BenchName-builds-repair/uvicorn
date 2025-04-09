import asyncio
import uvicorn
from uvicorn.config import Config
from uvicorn._types import Scope, ASGIReceiveCallable, ASGISendCallable
import httpx
from contextlib import asynccontextmanager

async def app(scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
    assert scope["type"] == "websocket"
    assert "extensions" in scope
    assert "websocket.http.response" in scope["extensions"]

    # Pull up first recv message.
    message = await receive()
    assert message["type"] == "websocket.connect"

    # Send HTTP response start
    await send({
        "type": "websocket.http.response.start",
        "status": 403,
        "headers": [],
    })
    # Send HTTP response body
    await send({"type": "websocket.http.response.body", "body": b"hardbody"})

@asynccontextmanager
async def run_server(config):
    server_task = asyncio.create_task(uvicorn.Server(config).serve())
    await asyncio.sleep(0.1)  # Give the server time to start
    try:
        yield
    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

async def test_websocket_response():
    config = Config(
        app=app,
        lifespan="off",
        port=8000,
    )
    
    async with run_server(config):
        # Try to connect with websocket client
        url = "ws://127.0.0.1:8000"
        
        # Use httpx to make a websocket request
        headers = {
            "connection": "upgrade",
            "upgrade": "websocket",
            "Sec-WebSocket-Key": "x3JJHMbDL1EzLkh9GBhXDw==",
            "Sec-WebSocket-Version": "13",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url.replace("ws:", "http:"), headers=headers)
                print(f"Status code: {response.status_code}")
                print(f"Headers: {response.headers}")
                print(f"Content: {response.content}")
        except httpx.RemoteProtocolError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_response())