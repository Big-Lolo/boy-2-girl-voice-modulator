/**
 * Advanced Mode - Full voice modulation controls
 */
import React from 'react';
import ParameterControl from './ParameterControl';

const AdvancedMode = ({ profile, onProfileChange, config, onConfigChange, latency }) => {
    const updateParameter = (key, value) => {
        onProfileChange({
            ...profile,
            [key]: value
        });
    };

    const updateConfig = (key, value) => {
        onConfigChange({
            ...config,
            [key]: value
        });
    };

    const bufferSizes = [128, 256, 512, 1024, 2048];

    return (
        <div className="advanced-mode">
            <h3>⚙️ Advanced Mode</h3>

            <div className="advanced-section">
                <h4>Voice Parameters</h4>

                <ParameterControl
                    label="Pitch Shift"
                    value={profile.pitch_shift}
                    onChange={(val) => updateParameter('pitch_shift', val)}
                    min={-12}
                    max={12}
                    step={0.5}
                    unit=" semitones"
                    description="Changes the pitch of your voice"
                    recommendation="±6 semitones for gender change"
                />

                <ParameterControl
                    label="Formant Shift"
                    value={profile.formant_shift}
                    onChange={(val) => updateParameter('formant_shift', val)}
                    min={0.6}
                    max={1.4}
                    step={0.05}
                    description="Adjusts vocal resonances"
                    recommendation="0.8-0.9 for feminine, 1.1-1.2 for masculine"
                />

                <ParameterControl
                    label="Resonance"
                    value={profile.resonance}
                    onChange={(val) => updateParameter('resonance', val)}
                    min={0}
                    max={100}
                    step={1}
                    unit="%"
                    description="Adds richness and depth"
                    recommendation="20-40%"
                />

                <ParameterControl
                    label="Brightness"
                    value={profile.brightness}
                    onChange={(val) => updateParameter('brightness', val)}
                    min={-10}
                    max={10}
                    step={0.5}
                    unit=" dB"
                    description="High-frequency boost/cut"
                    recommendation="±3 dB"
                />

                <ParameterControl
                    label="Timbre Shift"
                    value={profile.timbre_shift}
                    onChange={(val) => updateParameter('timbre_shift', val)}
                    min={0.5}
                    max={2.0}
                    step={0.05}
                    description="Changes the overall tonal quality"
                    recommendation="0.8-1.2 for natural results"
                />

                <ParameterControl
                    label="Gender Strength"
                    value={profile.gender_strength}
                    onChange={(val) => updateParameter('gender_strength', val)}
                    min={0}
                    max={100}
                    step={1}
                    unit="%"
                    description="Intensity of gender transformation"
                    recommendation="50-80% for balanced results"
                />

                <ParameterControl
                    label="Breath Noise"
                    value={profile.breath_noise}
                    onChange={(val) => updateParameter('breath_noise', val)}
                    min={0}
                    max={100}
                    step={1}
                    unit="%"
                    description="Adds breathiness to the voice"
                    recommendation="10-30% for natural breath"
                />
            </div>

            <div className="advanced-section">
                <h4>Audio Configuration</h4>

                <div className="config-group">
                    <label>
                        <span>Buffer Size (samples)</span>
                        <select
                            value={config.buffer_size}
                            onChange={(e) => updateConfig('buffer_size', parseInt(e.target.value))}
                            className="config-select"
                        >
                            {bufferSizes.map((size) => (
                                <option key={size} value={size}>
                                    {size} samples
                                </option>
                            ))}
                        </select>
                    </label>
                    <div className="config-info">
                        Lower = less latency but higher CPU usage. Start with 512.
                    </div>
                </div>

                <div className="config-group">
                    <label>
                        <span>Sample Rate (Hz)</span>
                        <select
                            value={config.sample_rate}
                            onChange={(e) => updateConfig('sample_rate', parseInt(e.target.value))}
                            className="config-select"
                        >
                            <option value={44100}>44100 Hz (CD Quality)</option>
                            <option value={48000}>48000 Hz (Professional)</option>
                        </select>
                    </label>
                </div>

                {latency !== undefined && (
                    <div className="latency-display">
                        <h4>Performance</h4>
                        <div className={`latency-value ${latency > 100 ? 'high' : latency > 50 ? 'medium' : 'low'}`}>
                            <span className="latency-label">Latency:</span>
                            <span className="latency-number">{latency.toFixed(1)} ms</span>
                        </div>
                        <div className="latency-info">
                            {latency < 30 && "🟢 Excellent - Imperceptible delay"}
                            {latency >= 30 && latency < 70 && "🟡 Good - Minimal perceptible delay"}
                            {latency >= 70 && latency < 100 && "🟠 Acceptable - Noticeable but usable"}
                            {latency >= 100 && "🔴 High - Consider reducing buffer size or effects"}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdvancedMode;
