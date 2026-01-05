/**
 * Custom hook for WebSocket connection management
 */
import { useEffect, useRef, useState } from 'react';
import { createWebSocket } from '../services/api';

export const useWebSocket = (onMessage) => {
    const wsRef = useRef(null);
    const [isConnected, setIsConnected] = useState(false);
    const [latency, setLatency] = useState(0);

    useEffect(() => {
        const connectWebSocket = () => {
            try {
                const ws = createWebSocket();

                ws.onopen = () => {
                    console.log('WebSocket connected');
                    setIsConnected(true);
                };

                ws.onmessage = (event) => {
                    const message = JSON.parse(event.data);
                    if (onMessage) {
                        onMessage(message);
                    }

                    // Update latency if status message
                    if (message.type === 'status' && message.data.latency_ms !== undefined) {
                        setLatency(message.data.latency_ms);
                    }
                };

                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };

                ws.onclose = () => {
                    console.log('WebSocket disconnected');
                    setIsConnected(false);

                    // Reconnect after 3 seconds
                    setTimeout(connectWebSocket, 3000);
                };

                wsRef.current = ws;
            } catch (error) {
                console.error('Failed to create WebSocket:', error);
                setTimeout(connectWebSocket, 3000);
            }
        };

        connectWebSocket();

        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [onMessage]);

    const sendMessage = (message) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(message));
        }
    };

    return { sendMessage, isConnected, latency };
};
