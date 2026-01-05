/**
 * Main App Component - Voice Modulator Application
 */
import React, { useState, useEffect } from 'react';
import { voiceModulatorAPI } from './services/api';
import { useWebSocket } from './hooks/useWebSocket';
import DeviceSelector from './components/DeviceSelector';
import SimpleMode from './components/SimpleMode';
import AdvancedMode from './components/AdvancedMode';
import ProfileManager from './components/ProfileManager';
import './App.css';

function App() {
    const [mode, setMode] = useState('simple'); // 'simple' or 'advanced'
    const [isEnabled, setIsEnabled] = useState(false);

    const [config, setConfig] = useState({
        input_device: null,
        output_device: null,
        buffer_size: 512,
        sample_rate: 48000,
        enabled: false
    });

    const [profile, setProfile] = useState({
        name: 'Current',
        pitch_shift: 0.0,
        formant_shift: 1.0,
        resonance: 0.0,
        brightness: 0.0,
        timbre_shift: 1.0,
        gender_strength: 50.0,
        breath_noise: 0.0
    });

    const [status, setStatus] = useState(null);

    // WebSocket connection
    const { sendMessage, isConnected, latency } = useWebSocket((message) => {
        if (message.type === 'status') {
            setStatus(message.data);
        } else if (message.type === 'config_update') {
            setConfig(message.data);
        } else if (message.type === 'profile_update') {
            setProfile(message.data);
        }
    });

    // Apply configuration changes
    useEffect(() => {
        const applyConfig = async () => {
            try {
                const configToSend = {
                    ...config,
                    enabled: isEnabled
                };
                await voiceModulatorAPI.updateConfig(configToSend);
            } catch (error) {
                console.error('Failed to update config:', error);
            }
        };

        if (config.input_device !== null && config.output_device !== null) {
            applyConfig();
        }
    }, [config, isEnabled]);

    // Apply profile changes
    useEffect(() => {
        const applyProfile = async () => {
            try {
                await voiceModulatorAPI.applyProfile(profile);
            } catch (error) {
                console.error('Failed to apply profile:', error);
            }
        };

        applyProfile();
    }, [profile]);

    const toggleEnabled = async () => {
        if (!config.input_device || !config.output_device) {
            alert('Please select both input and output devices first!');
            return;
        }

        try {
            const newEnabled = !isEnabled;
            setIsEnabled(newEnabled);

            const configToSend = {
                ...config,
                enabled: newEnabled
            };
            await voiceModulatorAPI.updateConfig(configToSend);
        } catch (error) {
            console.error('Failed to toggle processing:', error);
            alert('Failed to start audio processing. Check console for errors.');
            setIsEnabled(false);
        }
    };

    return (
        <div className="app">
            <header className="app-header">
                <h1>🎤 Voice Modulator</h1>
                <p className="subtitle">Real-time voice transformation for roleplay gaming</p>
                <div className="connection-status">
                    <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                        {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
                    </span>
                </div>
            </header>

            <main className="app-main">
                <div className="control-panel">
                    <DeviceSelector
                        inputDevice={config.input_device}
                        outputDevice={config.output_device}
                        onInputChange={(device) => setConfig({ ...config, input_device: device })}
                        onOutputChange={(device) => setConfig({ ...config, output_device: device })}
                    />

                    <div className="enable-section">
                        <button
                            onClick={toggleEnabled}
                            className={`enable-button ${isEnabled ? 'enabled' : 'disabled'}`}
                            disabled={!config.input_device || !config.output_device}
                        >
                            {isEnabled ? '⏸️ Disable Processing' : '▶️ Enable Processing'}
                        </button>
                        {isEnabled && (
                            <div className="processing-indicator">
                                <span className="pulse-dot"></span>
                                Processing Active
                            </div>
                        )}
                    </div>

                    <div className="mode-selector">
                        <button
                            onClick={() => setMode('simple')}
                            className={`mode-button ${mode === 'simple' ? 'active' : ''}`}
                        >
                            Simple Mode
                        </button>
                        <button
                            onClick={() => setMode('advanced')}
                            className={`mode-button ${mode === 'advanced' ? 'active' : ''}`}
                        >
                            Advanced Mode
                        </button>
                    </div>

                    {mode === 'simple' ? (
                        <SimpleMode
                            profile={profile}
                            onProfileChange={setProfile}
                        />
                    ) : (
                        <AdvancedMode
                            profile={profile}
                            onProfileChange={setProfile}
                            config={config}
                            onConfigChange={setConfig}
                            latency={status?.latency_ms ?? latency}
                        />
                    )}

                    <ProfileManager
                        currentProfile={profile}
                        onLoadProfile={setProfile}
                    />
                </div>

                <footer className="app-footer">
                    <div className="footer-info">
                        <span>💡 <strong>Tip:</strong> Use virtual audio cables to route audio to your games/applications</span>
                    </div>
                    {status && (
                        <div className="status-bar">
                            <span>Latency: {(status.latency_ms || 0).toFixed(1)}ms</span>
                            {status.input_device && <span>Input: {status.input_device}</span>}
                            {status.output_device && <span>Output: {status.output_device}</span>}
                        </div>
                    )}
                </footer>
            </main>
        </div>
    );
}

export default App;
