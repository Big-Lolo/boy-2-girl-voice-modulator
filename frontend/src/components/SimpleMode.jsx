/**
 * Simple Mode - Essential voice modulation controls
 */
import React from 'react';
import ParameterControl from './ParameterControl';

const SimpleMode = ({ profile, onProfileChange }) => {
    const updateParameter = (key, value) => {
        onProfileChange({
            ...profile,
            [key]: value
        });
    };

    const presets = [
        { name: 'Male to Female', pitch: 6, formant: 0.85 },
        { name: 'Female to Male', pitch: -6, formant: 1.15 },
        { name: 'Deep Voice', pitch: -8, formant: 1.2 },
        { name: 'High Voice', pitch: 8, formant: 0.8 },
        { name: 'Neutral', pitch: 0, formant: 1.0 },
    ];

    const applyPreset = (preset) => {
        onProfileChange({
            ...profile,
            pitch_shift: preset.pitch,
            formant_shift: preset.formant,
            resonance: 30,
            brightness: preset.pitch > 0 ? 2 : -2,
            timbre_shift: preset.formant,
            gender_strength: 70,
            breath_noise: 15
        });
    };

    return (
        <div className="simple-mode">
            <h3>🎚️ Simple Mode</h3>

            <div className="presets">
                <label>Quick Presets:</label>
                <div className="preset-buttons">
                    {presets.map((preset) => (
                        <button
                            key={preset.name}
                            onClick={() => applyPreset(preset)}
                            className="preset-button"
                        >
                            {preset.name}
                        </button>
                    ))}
                </div>
            </div>

            <ParameterControl
                label="Pitch Shift"
                value={profile.pitch_shift}
                onChange={(val) => updateParameter('pitch_shift', val)}
                min={-12}
                max={12}
                step={0.5}
                unit=" semitones"
                description="Changes the pitch of your voice (higher/lower)"
                recommendation="±6 semitones for gender change, ±3 for subtle adjustments"
            />

            <ParameterControl
                label="Formant Shift"
                value={profile.formant_shift}
                onChange={(val) => updateParameter('formant_shift', val)}
                min={0.6}
                max={1.4}
                step={0.05}
                description="Adjusts vocal resonances (masculine/feminine character)"
                recommendation="0.8-0.9 for more feminine, 1.1-1.2 for more masculine"
            />

            <ParameterControl
                label="Resonance"
                value={profile.resonance}
                onChange={(val) => updateParameter('resonance', val)}
                min={0}
                max={100}
                step={1}
                unit="%"
                description="Adds richness and depth to the voice"
                recommendation="20-40% for natural sound, higher for more effect"
            />

            <ParameterControl
                label="Brightness"
                value={profile.brightness}
                onChange={(val) => updateParameter('brightness', val)}
                min={-10}
                max={10}
                step={0.5}
                unit=" dB"
                description="Adjusts high-frequency content (brightness/warmth)"
                recommendation="±3 dB for subtle changes, avoid extreme values"
            />
        </div>
    );
};

export default SimpleMode;
