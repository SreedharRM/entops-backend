# quick script (scripts/init_db.py)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from db.models import init_db
init_db()
print("✅ Database initialized")
