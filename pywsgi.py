"""
Production server configuration for FastAPI application using Gunicorn.
"""
from gunicorn.app.base import BaseApplication
from app.main import app
import multiprocessing

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
        "forwarded_allow_ips": "*"  # Allow forwarded requests
    }
    StandaloneApplication(app, options).run()
