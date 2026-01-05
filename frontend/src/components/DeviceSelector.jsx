/**
 * Device selector component for audio input/output
 */
import React from 'react';
import { useAudioDevices } from '../hooks/useAudioDevices';

const DeviceSelector = ({ inputDevice, outputDevice, onInputChange, onOutputChange }) => {
    const { inputDevices, outputDevices, loading, error } = useAudioDevices();

    if (loading) {
        return <div className="device-selector loading">Loading devices...</div>;
    }

    if (error) {
        return <div className="device-selector error">{error}</div>;
    }

    return (
        <div className="device-selector">
            <h3>🎤 Audio Devices</h3>

            <div className="device-select-group">
                <label>
                    <span className="device-label">Input Device (Microphone)</span>
                    <select
                        value={inputDevice ?? ''}
                        onChange={(e) => onInputChange(e.target.value ? parseInt(e.target.value) : null)}
                        className="device-select"
                    >
                        <option value="">Select input device...</option>
                        {inputDevices.map((device) => (
                            <option key={device.index} value={device.index}>
                                {device.name} ({device.max_input_channels} ch)
                            </option>
                        ))}
                    </select>
                </label>
            </div>

            <div className="device-select-group">
                <label>
                    <span className="device-label">Output Device (Speakers/Virtual Cable)</span>
                    <select
                        value={outputDevice ?? ''}
                        onChange={(e) => onOutputChange(e.target.value ? parseInt(e.target.value) : null)}
                        className="device-select"
                    >
                        <option value="">Select output device...</option>
                        {outputDevices.map((device) => (
                            <option key={device.index} value={device.index}>
                                {device.name} ({device.max_output_channels} ch)
                            </option>
                        ))}
                    </select>
                </label>
            </div>

            <div className="device-info">
                ℹ️ Use virtual audio cables (e.g., VB-Audio Virtual Cable) to route audio to your game/application
            </div>
        </div>
    );
};

export default DeviceSelector;
