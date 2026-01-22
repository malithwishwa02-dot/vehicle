import sys
from pathlib import Path
# Ensure project root is on sys.path when running from scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.burner import ProfileBurner
import os

p = os.path.abspath('generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84')
print('Testing burner against', p)
try:
    b = ProfileBurner(p)
    b.ignite()
    print('Ignite completed')
    # small actions
    try:
        b.generate_history_entropy()
        b.inject_phantom_local_storage()
    except Exception as e:
        print('Runtime injection error:', e)
    finally:
        b.extinguish()
except Exception as e:
    print('Ignition error:', e)
