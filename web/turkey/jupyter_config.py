import os

# Allow all IP addresses to use the service and run it on port 8888.
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888

# Don't load the browser on startup.
c.NotebookApp.open_browser = False
c.NotebookApp.certfile = '/usr/src/app/mycert.pem'
c.NotebookApp.keyfile = '/usr/src/app/mykey.key'
c.NotebookApp.password = os.getenv('NOTEBOOK_PASS_HASH', None)
