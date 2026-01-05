/**
 * Custom hook for audio device management
 */
import { useState, useEffect } from 'react';
import { voiceModulatorAPI } from '../services/api';

export const useAudioDevices = () => {
    const [devices, setDevices] = useState([]);
    const [inputDevices, setInputDevices] = useState([]);
    const [outputDevices, setOutputDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchDevices = async () => {
        try {
            setLoading(true);
            const response = await voiceModulatorAPI.getDevices();
            const allDevices = response.data;

            setDevices(allDevices);
            setInputDevices(allDevices.filter(d => d.max_input_channels > 0));
            setOutputDevices(allDevices.filter(d => d.max_output_channels > 0));

            setError(null);
        } catch (err) {
            console.error('Failed to fetch devices:', err);
            setError('Failed to load audio devices');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDevices();
    }, []);

    return { devices, inputDevices, outputDevices, loading, error, refetch: fetchDevices };
};
