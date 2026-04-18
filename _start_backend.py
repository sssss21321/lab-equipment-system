# -*- coding: utf-8 -*-
"""启动后端服务"""
import subprocess
import sys
import os

backend_dir = r'C:\Users\HP\.qclaw\workspace\lab-equipment-system\backend'
os.chdir(backend_dir)

print('Starting backend...')
proc = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'app.main:app',
     '--host', '127.0.0.1', '--port', '8000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
print(f'Backend PID: {proc.pid}')
for line in proc.stdout:
    print(line.decode('utf-8', errors='replace'), end='')
