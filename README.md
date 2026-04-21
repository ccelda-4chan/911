# SOLID BOMBER PRO

Professional SMS & Call Bombing Engine with a modern Web Interface.

## 🚀 Improvements & Features
- **Modern Architecture**: Modular design with separate Engine, Services, and UI layers.
- **Robust Networking**: Persistent `aiohttp` session management and connection pooling.
- **Observability**: Structured logging and real-time WebUI status polling.
- **Performance**: Asynchronous execution with global concurrency limits (Semaphores).
- **Security**: Environment-based configuration and session-protected WebUI.
- **UX/UI**: Sleek Dashboard built with Bootstrap 5 and real-time logs.

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
