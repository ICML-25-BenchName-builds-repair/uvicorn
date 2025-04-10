import asyncio
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server

async def app(scope, receive, send):
    assert scope["type"] == "websocket"
    assert "extensions" in scope
    assert "websocket.http.response" in scope["extensions"]

    # Pull up first recv message.
    message = await receive()
    assert message["type"] == "websocket.connect"

    await send(
        {
            "type": "websocket.http.response.start",
            "status": 403,
            "headers": [],
        }
    )
    await send({"type": "websocket.http.response.body", "body": b"hardbody"})

async def main():
    config = Config(app=app, ws="websockets", http="h11", lifespan="off", port=8000)
    server = Server(config=config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())