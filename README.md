# +Nine-11 | DISPATCH CONSOLE v2.0.0-PRO

A professional, multi-functional tactical toolkit designed for network stress analysis, signal distribution, and intelligence gathering. Optimized for high-concurrency environments and Render.com Free Tier.

## 🚀 Key Modules

### 📡 Signal Dispatch (Bomber)
- **High Intensity**: Parallel signal load distribution for multiple target nodes (Phone numbers).
- **Global Coverage**: Optimized for PH-region carriers (Globe, Smart, DITO, Maya, Grab).
- **Customizable**: Choose specific signal carriers and intensity levels.

### ⚡ Network Stress Analysis (L7 Flood)
- **Layer 7 Optimization**: High-concurrency HTTP/S flooding for resource testing.
- **Uptime Monitoring**: Real-time target status visualization (Online/Offline).
- **Performance Visualization**: Live Packets Per Second (PPS) counter.

### 📍 Location Verification (IP Tracker)
- **Stealth Tracking**: Generate professional verification links to redirect targets to any destination.
- **Intel Capture**: Log visitor IP, User-Agent, Referer, and approximate Geo-location.
- **Real-time Monitoring**: Integrated click logs and verification database.

### 🔍 Intelligence Inquiry (OSINT)
- **IP Trace**: Detailed lookup of IP addresses, including ISP, ASN, and geographic data.
- **Carrier Logic**: Philippine mobile number carrier and network prefix identification.

## 🛠️ Security & Features
- **Tactical Dispatch UI**: High-contrast, dark-themed console with tabbed interface.
- **Abort Operation**: Real-time stop command for all active tasks.
- **Stealth Mode**: Disguised feature names to hide original intent (Signal vs. Bomber).
- **Connection Pooling**: Optimized `aiohttp` sessions for maximum performance.

## ☁️ Deployment on Render.com

This project is pre-configured for **one-click deployment** on Render's Free Tier.

1.  **Fork** this repository to your GitHub account.
2.  In the **Render Dashboard**, create a new **Blueprint**.
3.  Connect your forked repository.
4.  Render will automatically build and start the service based on `render.yaml`.

**Free Tier Note**: Instances spin down after inactivity. Access the `/health` endpoint to keep the service warm or use a monitoring tool like `UptimeRobot`.

## ⚙️ Configuration
The application uses the following environment variables (defined in `render.yaml`):
- `RENDER`: Set to `true` for production optimizations.
- `SESSION_SECRET`: Key for Flask session security.

---
*Developed for educational and authorized testing purposes only.*
