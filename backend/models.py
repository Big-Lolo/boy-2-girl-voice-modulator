"""
Pydantic models for voice modulator API.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class AudioDevice(BaseModel):
    """Represents an audio device."""
    index: int
    name: str
    max_input_channels: int
    max_output_channels: int
    default_sample_rate: float


class VoiceProfile(BaseModel):
    """Voice modulation profile configuration."""
    name: str = Field(..., description="Profile name")
    pitch_shift: float = Field(0.0, ge=-12.0, le=12.0, description="Pitch shift in semitones")
    formant_shift: float = Field(1.0, ge=0.6, le=1.4, description="Formant shift multiplier")
    resonance: float = Field(0.0, ge=0.0, le=100.0, description="Resonance percentage")
    brightness: float = Field(0.0, ge=-10.0, le=10.0, description="Brightness in dB")
    timbre_shift: float = Field(1.0, ge=0.5, le=2.0, description="Timbre shift multiplier")
    gender_strength: float = Field(50.0, ge=0.0, le=100.0, description="Gender transformation strength")
    breath_noise: float = Field(0.0, ge=0.0, le=100.0, description="Breath noise percentage")


class AudioConfig(BaseModel):
    """Audio processing configuration."""
    input_device: Optional[int] = Field(None, description="Input device index")
    output_device: Optional[int] = Field(None, description="Output device index")
    buffer_size: int = Field(512, description="Buffer size in samples")
    sample_rate: int = Field(48000, description="Sample rate in Hz")
    enabled: bool = Field(False, description="Processing enabled")


class ProcessingStatus(BaseModel):
    """Current processing status."""
    enabled: bool
    latency_ms: float
    input_device: Optional[str]
    output_device: Optional[str]
    cpu_usage: float


class WebSocketMessage(BaseModel):
    """WebSocket message structure."""
    type: str  # "config_update", "status", "error"
    data: dict


class ProfileListResponse(BaseModel):
    """Response for profile listing."""
    profiles: List[str]


class SaveProfileRequest(BaseModel):
    """Request to save a profile."""
    profile: VoiceProfile
