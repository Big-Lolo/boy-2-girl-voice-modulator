/**
 * Profile Manager - Save, load, and manage voice profiles
 */
import React, { useState, useEffect } from 'react';
import { voiceModulatorAPI } from '../services/api';

const ProfileManager = ({ currentProfile, onLoadProfile }) => {
    const [profiles, setProfiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [newProfileName, setNewProfileName] = useState('');
    const [message, setMessage] = useState(null);

    useEffect(() => {
        loadProfiles();
    }, []);

    const loadProfiles = async () => {
        try {
            const response = await voiceModulatorAPI.listProfiles();
            setProfiles(response.data.profiles);
        } catch (error) {
            console.error('Failed to load profiles:', error);
            showMessage('Failed to load profiles', 'error');
        }
    };

    const saveProfile = async () => {
        if (!newProfileName.trim()) {
            showMessage('Please enter a profile name', 'error');
            return;
        }

        try {
            setLoading(true);
            const profileToSave = {
                ...currentProfile,
                name: newProfileName
            };

            await voiceModulatorAPI.saveProfile(profileToSave);
            showMessage(`Profile "${newProfileName}" saved successfully!`, 'success');
            setNewProfileName('');
            await loadProfiles();
        } catch (error) {
            console.error('Failed to save profile:', error);
            showMessage('Failed to save profile', 'error');
        } finally {
            setLoading(false);
        }
    };

    const loadProfile = async (profileName) => {
        try {
            setLoading(true);
            const response = await voiceModulatorAPI.getProfile(profileName);
            onLoadProfile(response.data);
            showMessage(`Profile "${profileName}" loaded!`, 'success');
        } catch (error) {
            console.error('Failed to load profile:', error);
            showMessage('Failed to load profile', 'error');
        } finally {
            setLoading(false);
        }
    };

    const deleteProfile = async (profileName) => {
        if (!confirm(`Are you sure you want to delete "${profileName}"?`)) {
            return;
        }

        try {
            setLoading(true);
            await voiceModulatorAPI.deleteProfile(profileName);
            showMessage(`Profile "${profileName}" deleted`, 'success');
            await loadProfiles();
        } catch (error) {
            console.error('Failed to delete profile:', error);
            showMessage('Failed to delete profile (default profiles are protected)', 'error');
        } finally {
            setLoading(false);
        }
    };

    const showMessage = (text, type) => {
        setMessage({ text, type });
        setTimeout(() => setMessage(null), 3000);
    };

    return (
        <div className="profile-manager">
            <h3>💾 Profile Manager</h3>

            {message && (
                <div className={`message ${message.type}`}>
                    {message.text}
                </div>
            )}

            <div className="save-profile-section">
                <h4>Save Current Settings</h4>
                <div className="save-profile-form">
                    <input
                        type="text"
                        placeholder="Profile name..."
                        value={newProfileName}
                        onChange={(e) => setNewProfileName(e.target.value)}
                        className="profile-name-input"
                        onKeyPress={(e) => e.key === 'Enter' && saveProfile()}
                    />
                    <button
                        onClick={saveProfile}
                        disabled={loading || !newProfileName.trim()}
                        className="save-button"
                    >
                        {loading ? 'Saving...' : 'Save Profile'}
                    </button>
                </div>
            </div>

            <div className="load-profile-section">
                <h4>Load Profile</h4>
                {profiles.length === 0 ? (
                    <div className="no-profiles">No profiles available</div>
                ) : (
                    <div className="profile-list">
                        {profiles.map((profileName) => (
                            <div key={profileName} className="profile-item">
                                <span className="profile-name">{profileName}</span>
                                <div className="profile-actions">
                                    <button
                                        onClick={() => loadProfile(profileName)}
                                        disabled={loading}
                                        className="load-button"
                                    >
                                        Load
                                    </button>
                                    {!profileName.includes('to') && !profileName.includes('Robot') && !profileName.includes('Voice') && (
                                        <button
                                            onClick={() => deleteProfile(profileName)}
                                            disabled={loading}
                                            className="delete-button"
                                        >
                                            Delete
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
                <button
                    onClick={loadProfiles}
                    className="refresh-button"
                    disabled={loading}
                >
                    🔄 Refresh List
                </button>
            </div>
        </div>
    );
};

export default ProfileManager;
