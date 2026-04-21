# SOLID BOMBER PRO - PRESTIGE EDITION

Professional SMS & Call Bombing Engine with a modern, high-performance Web Interface.

## 🚀 Improvements & Features
- **Modern Architecture**: Modular design with separate Engine, Services, and UI layers.
- **Prestige UI/UX**: Stunning Philippine-themed dashboard with "uiverse.io" style animations.
- **Enhanced Power**: Optimized async engine with increased concurrency and reduced delays.
- **Multi-Target Support**: Deploy payloads to multiple phone numbers simultaneously.
- **Real-Time Visuals**: Dynamic rocket explosion animations on successful hits.
- **High Volume**: Standardized 100-batch default intensity for maximum impact.
- **Performance**: Asynchronous execution with global concurrency limits (Semaphores).
- **Observability**: Structured logging and real-time WebUI status polling.

## 🛠 Deployment
- **Render.com**: Fully compatible via `render.yaml`.
- **Local**: 
  1. `pip install -r requirements.txt`
  2. Copy `.env.example` to `.env` and configure.
  3. `python app.py`

## 🧪 Testing
Run unit tests to verify core logic:
```bash
set PYTHONPATH=.
python tests/test_utils.py
python tests/test_engine.py
```

## 🔗 Repository
[https://github.com/ccelda-4chan/911](https://github.com/ccelda-4chan/911)
