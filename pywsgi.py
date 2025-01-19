"""
Production server configuration for FastAPI application using Gunicorn on Linux
and Uvicorn on Windows.
"""
import platform
from app.main import app  # Import your FastAPI app

if platform.system() == "Windows":
    # Use Uvicorn on Windows
    import uvicorn

    if __name__ == "__main__":
        uvicorn.run(
            "app.main:app",  # Pass the application as an import string
            host="0.0.0.0",
            port=8000,
            workers=2,  # Number of workers
            reload=False,  # Set to True if in development
        )
else:
    # Use Gunicorn on Linux
    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    if __name__ == "__main__":
        options = {
            "bind": "0.0.0.0:8000",  # Bind to all interfaces
            "workers": 2,
            "worker_class": "uvicorn.workers.UvicornWorker",
            "timeout": 120,
            "reload": False,
            "forwarded_allow_ips": "*",  # Allow forwarded requests
        }
        StandaloneApplication(app, options).run()
