"""WebSocket routes for real-time joke streaming"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

from app.services.external_api import ExternalAPIService

router = APIRouter()

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@router.websocket("/ws/jokes/stream")
async def websocket_joke_stream(websocket: WebSocket):
    """WebSocket endpoint for streaming jokes"""
    await manager.connect(websocket)
    external_api = ExternalAPIService()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "get_joke":
                try:
                    joke_data = await external_api.get_random_joke()
                    await websocket.send_json({
                        "status": "success",
                        "joke": joke_data
                    })
                except Exception as e:
                    await websocket.send_json({
                        "status": "error",
                        "message": str(e)
                    })
            
            elif message.get("action") == "stream_jokes":
                count = message.get("count", 5)
                interval = message.get("interval", 2)
                
                for i in range(count):
                    try:
                        joke_data = await external_api.get_random_joke()
                        await websocket.send_json({
                            "status": "success",
                            "joke": joke_data,
                            "index": i + 1
                        })
                        if i < count - 1:
                            await asyncio.sleep(interval)
                    except Exception as e:
                        await websocket.send_json({
                            "status": "error",
                            "message": str(e)
                        })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
