"""
State Architect: Injects complex, provider-specific Local Storage keys for Stripe, Shopify, Adyen, etc.
"""
import uuid
import base64
import json
from datetime import datetime

def generate_stripe_keys():
    return {
        "stripe_mid": str(uuid.uuid4()),
        "stripe_sid": str(uuid.uuid4()),
        "stripe_machine_id": str(uuid.uuid4()),
        "stripe_user_id": str(uuid.uuid4()),
    }

def generate_shopify_keys():
    return {
        "shopify_y": str(uuid.uuid4()),
        "shopify_s": str(uuid.uuid4()),
        "shopify_checkout_token": str(uuid.uuid4()),
    }

def generate_kla_id():
    payload = {"ts": int(datetime.now().timestamp())}
    return base64.b64encode(json.dumps(payload).encode()).decode()

def generate_all():
    keys = {}
    keys.update(generate_stripe_keys())
    keys.update(generate_shopify_keys())
    keys["__kla_id"] = generate_kla_id()
    return keys

if __name__ == "__main__":
    print(json.dumps(generate_all(), indent=2))
