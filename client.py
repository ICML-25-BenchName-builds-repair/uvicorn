import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        headers = {
            "Connection": "upgrade",
            "Upgrade": "websocket",
            "Sec-WebSocket-Version": "13",
            "Sec-WebSocket-Key": "dGhlIHNhbXBsZSBub25jZQ==",
        }
        try:
            response = await client.get("http://localhost:8000", headers=headers)
            print(f"Status code: {response.status_code}")
            print(f"Headers: {response.headers}")
            print(f"Content: {response.content}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())