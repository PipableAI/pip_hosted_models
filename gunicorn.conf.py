# Gunicorn configuration file
import multiprocessing

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "0.0.0.0:3200"
timeout = 180
worker_class = "uvicorn.workers.UvicornWorker"
workers = 2
# workers = (multiprocessing.cpu_count() * 2) + 1
