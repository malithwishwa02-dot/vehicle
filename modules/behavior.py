import random
import math
import time
from config import settings

def poisson_delay():
    delay = -math.log(1.0 - random.random()) / settings.POISSON_LAMBDA
    time.sleep(delay)
    return delay

def silence_window():
    print(f"[Silence Window] Waiting {settings.SILENCE_WINDOW} seconds before handover...")
    time.sleep(settings.SILENCE_WINDOW)
