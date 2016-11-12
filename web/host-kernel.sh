#!/usr/bin/env bash
python /usr/src/app/turkey/manage.py shell_plus --kernel&
sleep 30s;
cat /root/.local/share/jupyter/runtime/$(ls /root/.local/share/jupyter/runtime/);
