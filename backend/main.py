"""
FastAPI backend for real-time voice modulator.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import json

from models import (
    AudioDevice, VoiceProfile, AudioConfig, ProcessingStatus,
    ProfileListResponse, SaveProfileRequest
)
from audio_processor import AudioProcessor
from voice_profiles import ProfileManager

# Initialize FastAPI app
app = FastAPI(
    title="Voice Modulator API",
    description="Real-time voice modulation for roleplay gaming",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize audio processor and profile manager
audio_processor = AudioProcessor()
profile_manager = ProfileManager()

# WebSocket connection manager
class ConnectionManager:
    """Manages active WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


# REST API Endpoints

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Voice Modulator API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/devices", response_model=List[AudioDevice])
async def get_audio_devices():
    """Get list of available audio devices.
    
    Returns:
        List of audio devices with their properties
    """
    try:
        devices = AudioProcessor.get_audio_devices()
        return devices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles", response_model=ProfileListResponse)
async def list_profiles():
    """List all available voice profiles.
    
    Returns:
        List of profile names
    """
    try:
        profiles = profile_manager.list_profiles()
        return ProfileListResponse(profiles=profiles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles/{profile_name}", response_model=VoiceProfile)
async def get_profile(profile_name: str):
    """Get a specific voice profile.
    
    Args:
        profile_name: Name of the profile to retrieve
        
    Returns:
        VoiceProfile configuration
    """
    profile = profile_manager.load_profile(profile_name)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_name}' not found")
    return profile


@app.post("/profiles")
async def save_profile(request: SaveProfileRequest):
    """Save a new voice profile.
    
    Args:
        request: SaveProfileRequest containing the profile
        
    Returns:
        Success message with saved profile path
    """
    try:
        filepath = profile_manager.save_profile(request.profile)
        return {
            "message": "Profile saved successfully",
            "profile_name": request.profile.name,
            "filepath": filepath
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/profiles/{profile_name}")
async def delete_profile(profile_name: str):
    """Delete a voice profile.
    
    Args:
        profile_name: Name of the profile to delete
        
    Returns:
        Success or error message
    """
    success = profile_manager.delete_profile(profile_name)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Profile '{profile_name}' not found or cannot be deleted (default profiles are protected)"
        )
    return {"message": f"Profile '{profile_name}' deleted successfully"}


@app.get("/status", response_model=ProcessingStatus)
async def get_status():
    """Get current processing status.
    
    Returns:
        Current status including latency and device info
    """
    status = audio_processor.get_status()
    return ProcessingStatus(**status)


@app.post("/config")
async def update_config(config: AudioConfig):
    """Update audio configuration.
    
    Args:
        config: New audio configuration
        
    Returns:
        Success message
    """
    try:
        audio_processor.update_config(config)
        
        # Start or stop processing based on enabled flag
        if config.enabled and audio_processor.stream is None:
            audio_processor.start()
        elif not config.enabled and audio_processor.stream is not None:
            audio_processor.stop()
        
        # Broadcast config update to all WebSocket clients
        await manager.broadcast({
            "type": "config_update",
            "data": config.model_dump()
        })
        
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/profile/apply")
async def apply_profile(profile: VoiceProfile):
    """Apply a voice profile to the audio processor.
    
    Args:
        profile: VoiceProfile to apply
        
    Returns:
        Success message
    """
    try:
        audio_processor.update_profile(profile)
        
        # Broadcast profile update to all WebSocket clients
        await manager.broadcast({
            "type": "profile_update",
            "data": profile.model_dump()
        })
        
        return {"message": "Profile applied successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket Endpoint

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication.
    
    Args:
        websocket: WebSocket connection
    """
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await websocket.send_json({
            "type": "status",
            "data": audio_processor.get_status()
        })
        
        # Status update task
        async def send_status_updates():
            while True:
                try:
                    await asyncio.sleep(1.0)  # Update every second
                    status = audio_processor.get_status()
                    await websocket.send_json({
                        "type": "status",
                        "data": status
                    })
                except:
                    break
        
        # Start status update task
        status_task = asyncio.create_task(send_status_updates())
        
        # Listen for messages from client
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "config_update":
                config = AudioConfig(**message["data"])
                audio_processor.update_config(config)
                
                if config.enabled and audio_processor.stream is None:
                    audio_processor.start()
                elif not config.enabled and audio_processor.stream is not None:
                    audio_processor.stop()
            
            elif message["type"] == "profile_update":
                profile = VoiceProfile(**message["data"])
                audio_processor.update_profile(profile)
            
            elif message["type"] == "get_status":
                status = audio_processor.get_status()
                await websocket.send_json({
                    "type": "status",
                    "data": status
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        status_task.cancel()
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
        if 'status_task' in locals():
            status_task.cancel()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    audio_processor.stop()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
