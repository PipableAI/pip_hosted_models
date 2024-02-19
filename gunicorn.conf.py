# Gunicorn configuration file
import multiprocessing

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "0.0.0.0:3200"
timeout = 1200
worker_class = "uvicorn.workers.UvicornWorker"
workers = 1
# workers = (multiprocessing.cpu_count() * 2) + 1
