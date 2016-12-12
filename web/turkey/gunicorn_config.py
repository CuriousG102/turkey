import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = ":8000"
timeout = 3600
