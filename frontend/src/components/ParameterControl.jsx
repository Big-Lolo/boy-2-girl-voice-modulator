/**
 * Reusable parameter control component with slider and input
 */
import React from 'react';

const ParameterControl = ({
    label,
    value,
    onChange,
    min,
    max,
    step = 0.1,
    description,
    recommendation,
    unit = ''
}) => {
    return (
        <div className="parameter-control">
            <div className="parameter-header">
                <label className="parameter-label">{label}</label>
                <input
                    type="number"
                    className="parameter-number-input"
                    value={value}
                    onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
                    min={min}
                    max={max}
                    step={step}
                />
            </div>

            <input
                type="range"
                className="parameter-slider"
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                min={min}
                max={max}
                step={step}
            />

            <div className="parameter-value-display">
                <span>{value.toFixed(2)}{unit}</span>
            </div>

            {description && (
                <div className="parameter-description">
                    {description}
                </div>
            )}

            {recommendation && (
                <div className="parameter-recommendation">
                    💡 <strong>Recommended:</strong> {recommendation}
                </div>
            )}
        </div>
    );
};

export default ParameterControl;
