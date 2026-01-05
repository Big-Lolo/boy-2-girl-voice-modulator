# Voice Modulator

🎤 **Real-time voice modulation application for roleplay gaming**

Transform your voice in real-time with professional pitch shifting, formant manipulation, and advanced audio processing. Perfect for roleplay gaming, voice acting, and creative audio projects.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Real-time Voice Processing**: Low-latency audio transformation (<100ms target)
- **Pitch Shifting**: Adjust voice pitch by ±12 semitones
- **Formant Manipulation**: Change vocal resonances for masculine/feminine character
- **Advanced Effects**: Resonance, brightness, timbre shifting, and breath noise
- **Dual Interface Modes**: Simple mode for quick adjustments, advanced mode for full control
- **Profile Management**: Save, load, and manage voice configurations
- **Device Selection**: Choose audio input/output devices
- **WebSocket Integration**: Real-time parameter updates with minimal latency
- **Modern UI**: Beautiful dark mode interface with smooth animations

## 📋 Prerequisites

- **Python 3.8+**: For the backend server
- **Node.js 16+**: For the frontend application
- **Virtual Audio Cable** (recommended): VB-Audio Virtual Cable or similar for routing audio

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Big-Lolo/boy-2-girl-voice-modulator.git
cd boy-2-girl-voice-modulator
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will open at `http://localhost:5173`

### 4. Configure Audio Devices

1. Open the application in your browser
2. Select your **microphone** as the input device
3. Select your **speakers or virtual audio cable** as the output device
4. Click **"Enable Processing"** to start voice modulation

## 🎛️ Usage Guide

### Simple Mode

Perfect for quick voice transformations:

1. **Quick Presets**: Click preset buttons for instant voice changes
   - Male to Female
   - Female to Male
   - Deep Voice
   - High Voice
   - Neutral

2. **Manual Adjustments**:
   - **Pitch Shift**: -12 to +12 semitones (±6 for gender change)
   - **Formant Shift**: 0.6 to 1.4 (0.8-0.9 for feminine, 1.1-1.2 for masculine)
   - **Resonance**: 0-100% (adds richness)
   - **Brightness**: -10 to +10 dB (high-frequency adjustment)

### Advanced Mode

Full control over all parameters:

- All simple mode controls
- **Timbre Shift**: 0.5 to 2.0
- **Gender Strength**: 0-100%
- **Breath Noise**: 0-100%
- **Buffer Size**: 128 to 2048 samples (affects latency)
- **Sample Rate**: 44.1kHz or 48kHz
- **Real-time Latency Monitor**

### Profile Management

Save and load your favorite voice configurations:

1. Adjust parameters to your liking
2. Enter a profile name in the "Save Current Settings" field
3. Click **"Save Profile"**
4. Load profiles from the list anytime
5. Default profiles are protected from deletion

## 🔧 Virtual Audio Cable Setup

For routing audio to games/applications:

1. Download and Install [VB-Audio Virtual Cable](https://vb-audio.com/Cable/)
2. In the Voice Modulator:
   - Set **Input**: Your physical microphone
   - Set **Output**: CABLE Input (VB-Audio Virtual Cable)
3. In your game/application:
   - Set **Microphone**: CABLE Output (VB-Audio Virtual Cable)

Your modulated voice will now be routed to your game!

## 📁 Project Structure

```
boy-2-girl-voice-modulator/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── audio_processor.py      # Audio processing engine
│   ├── voice_profiles.py       # Profile management
│   ├── models.py               # Pydantic models
│   ├── requirements.txt        # Python dependencies
│   └── profiles/               # Saved voice profiles
│       └── default/            # Default profiles
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API client
│   │   ├── App.jsx             # Main component
│   │   └── App.css             # Styles
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🎯 API Endpoints

### REST API

- `GET /devices` - List audio devices
- `GET /profiles` - List voice profiles
- `GET /profiles/{name}` - Get specific profile
- `POST /profiles` - Save new profile
- `DELETE /profiles/{name}` - Delete profile
- `POST /config` - Update audio configuration
- `POST /profile/apply` - Apply voice profile
- `GET /status` - Get processing status

### WebSocket

- `WS /ws` - Real-time status updates and parameter changes

## ⚡ Performance Tips

- **Lower Latency**: Reduce buffer size (256 or 128 samples)
- **Better Stability**: Increase buffer size (1024 or 2048 samples)
- **Optimal Starting Point**: 512 samples
- **Close Background Apps**: Reduce CPU usage for better performance
- Use a dedicated audio interface for professional results

## 🛠️ Troubleshooting

### High Latency
- Reduce buffer size in Advanced Mode
- Close other audio applications
- Disable unnecessary effects

### Audio Crackling
- Increase buffer size
- Reduce number of active effects
- Check CPU usage

### No Audio Output
- Verify input/output device selection
- Check device permissions
- Ensure virtual cable is installed correctly

### Connection Issues
- Check that backend is running on port 8000
- Verify CORS settings in backend
- Check browser console for errors

## 🔮 Future Enhancements

- [ ] Electron desktop application
- [ ] Additional effects (reverb, echo, compression)
- [ ] Community profile sharing
- [ ] Real-time waveform visualization
- [ ] ASIO driver support for ultra-low latency
- [ ] Multi-language UI support
- [ ] Voice morphing between profiles

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💬 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the console logs for error messages

## 🙏 Acknowledgments

- Built with FastAPI and React
- Audio processing using sounddevice and scipy
- Inspired by professional voice changers and audio processors

---

**Made with ❤️ for the roleplay gaming community**
