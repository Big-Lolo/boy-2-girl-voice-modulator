"""
Voice profile management system.
Handles saving, loading, and listing voice profiles.
"""
import json
import os
from pathlib import Path
from typing import List, Optional
from models import VoiceProfile


class ProfileManager:
    """Manages voice profiles stored as JSON files."""
    
    def __init__(self, profiles_dir: str = "profiles"):
        """Initialize profile manager.
        
        Args:
            profiles_dir: Directory to store profile files
        """
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        self._create_default_profiles()
    
    def _create_default_profiles(self):
        """Create default voice profiles if they don't exist."""
        default_dir = self.profiles_dir / "default"
        default_dir.mkdir(exist_ok=True)
        
        # Male to Female profile
        male_to_female = VoiceProfile(
            name="Male to Female",
            pitch_shift=6.0,
            formant_shift=0.85,
            resonance=30.0,
            brightness=2.0,
            timbre_shift=0.9,
            gender_strength=70.0,
            breath_noise=15.0
        )
        
        # Female to Male profile
        female_to_male = VoiceProfile(
            name="Female to Male",
            pitch_shift=-6.0,
            formant_shift=1.15,
            resonance=25.0,
            brightness=-2.0,
            timbre_shift=1.1,
            gender_strength=70.0,
            breath_noise=10.0
        )
        
        # Neutral/Robot profile
        neutral = VoiceProfile(
            name="Neutral Robot",
            pitch_shift=0.0,
            formant_shift=1.0,
            resonance=0.0,
            brightness=0.0,
            timbre_shift=1.0,
            gender_strength=0.0,
            breath_noise=0.0
        )
        
        # Deep Voice profile
        deep_voice = VoiceProfile(
            name="Deep Voice",
            pitch_shift=-8.0,
            formant_shift=1.2,
            resonance=40.0,
            brightness=-3.0,
            timbre_shift=1.15,
            gender_strength=80.0,
            breath_noise=5.0
        )
        
        # High Voice profile
        high_voice = VoiceProfile(
            name="High Voice",
            pitch_shift=8.0,
            formant_shift=0.8,
            resonance=35.0,
            brightness=3.0,
            timbre_shift=0.85,
            gender_strength=80.0,
            breath_noise=20.0
        )
        
        # Save default profiles
        for profile in [male_to_female, female_to_male, neutral, deep_voice, high_voice]:
            profile_path = default_dir / f"{self._sanitize_filename(profile.name)}.json"
            if not profile_path.exists():
                self.save_profile(profile, subdirectory="default")
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize profile name for use as filename.
        
        Args:
            name: Profile name
            
        Returns:
            Sanitized filename
        """
        return name.lower().replace(" ", "_").replace("→", "to")
    
    def save_profile(self, profile: VoiceProfile, subdirectory: Optional[str] = None) -> str:
        """Save a voice profile to JSON file.
        
        Args:
            profile: VoiceProfile to save
            subdirectory: Optional subdirectory within profiles directory
            
        Returns:
            Path to saved profile file
        """
        if subdirectory:
            save_dir = self.profiles_dir / subdirectory
            save_dir.mkdir(exist_ok=True)
        else:
            save_dir = self.profiles_dir
        
        filename = f"{self._sanitize_filename(profile.name)}.json"
        filepath = save_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile.model_dump(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_profile(self, profile_name: str, subdirectory: Optional[str] = None) -> Optional[VoiceProfile]:
        """Load a voice profile from JSON file.
        
        Args:
            profile_name: Name of the profile to load
            subdirectory: Optional subdirectory to search in
            
        Returns:
            VoiceProfile if found, None otherwise
        """
        if subdirectory:
            search_dir = self.profiles_dir / subdirectory
        else:
            search_dir = self.profiles_dir
        
        filename = f"{self._sanitize_filename(profile_name)}.json"
        filepath = search_dir / filename
        
        if not filepath.exists():
            # Try searching in all subdirectories
            for subdir in self.profiles_dir.rglob(filename):
                filepath = subdir
                break
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return VoiceProfile(**data)
        
        return None
    
    def list_profiles(self, subdirectory: Optional[str] = None) -> List[str]:
        """List all available voice profiles.
        
        Args:
            subdirectory: Optional subdirectory to list from
            
        Returns:
            List of profile names
        """
        if subdirectory:
            search_dir = self.profiles_dir / subdirectory
        else:
            search_dir = self.profiles_dir
        
        profiles = []
        
        # Search for all JSON files in the directory and subdirectories
        for filepath in search_dir.rglob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'name' in data:
                        profiles.append(data['name'])
            except (json.JSONDecodeError, KeyError):
                continue
        
        return sorted(profiles)
    
    def delete_profile(self, profile_name: str, subdirectory: Optional[str] = None) -> bool:
        """Delete a voice profile.
        
        Args:
            profile_name: Name of the profile to delete
            subdirectory: Optional subdirectory to search in
            
        Returns:
            True if deleted, False if not found
        """
        if subdirectory:
            search_dir = self.profiles_dir / subdirectory
        else:
            search_dir = self.profiles_dir
        
        filename = f"{self._sanitize_filename(profile_name)}.json"
        filepath = search_dir / filename
        
        if not filepath.exists():
            # Try searching in all subdirectories
            for subdir in self.profiles_dir.rglob(filename):
                filepath = subdir
                break
        
        if filepath.exists():
            # Don't delete default profiles
            if "default" in str(filepath):
                return False
            
            filepath.unlink()
            return True
        
        return False
