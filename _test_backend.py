# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:\Users\HP\.qclaw\workspace\lab-equipment-system\backend')

try:
    from app.main import app
    print('FastAPI app loaded OK!')
    print('Routes:')
    for route in app.routes:
        if hasattr(route, 'methods'):
            print(f'  {route.methods} {route.path}')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
