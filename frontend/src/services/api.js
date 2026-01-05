/**
 * API client for voice modulator backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const voiceModulatorAPI = {
    // Device management
    getDevices: () => api.get('/devices'),

    // Profile management
    listProfiles: () => api.get('/profiles'),
    getProfile: (profileName) => api.get(`/profiles/${profileName}`),
    saveProfile: (profile) => api.post('/profiles', { profile }),
    deleteProfile: (profileName) => api.delete(`/profiles/${profileName}`),

    // Configuration
    updateConfig: (config) => api.post('/config', config),
    applyProfile: (profile) => api.post('/profile/apply', profile),
    getStatus: () => api.get('/status'),
};

export const createWebSocket = () => {
    return new WebSocket(`${WS_BASE_URL}/ws`);
};

export default api;
