"""Direct localStorage injector for testing persistence.
Usage: python inject_localstorage_direct.py --profile generated_profiles/37ab... --domain https://www.google.com --headless false
"""
import argparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ap = argparse.ArgumentParser()
ap.add_argument('--profile', required=True)
ap.add_argument('--domain', default='https://www.google.com')
ap.add_argument('--headless', choices=['true','false'], default='false')
args = ap.parse_args()

opts = Options()
opts.add_argument(f"--user-data-dir={args.profile}")
opts.add_argument('--profile-directory=Default')
if args.headless == 'true':
    opts.add_argument('--headless=new')

print('Launching Chrome attached to profile', args.profile)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
try:
    driver.get(args.domain)
    time.sleep(2)
    data = {
        "cart_abandoned": "false",
        "previous_purchases": "3",
        "user_trust_score": "0.95",
        "stripe_mid": "guid_12345_mock",
        "has_logged_in": "true"
    }
    for k,v in data.items():
        driver.execute_script(f"window.localStorage.setItem('{k}', '{v}');")
    print('Injected localStorage keys')
    time.sleep(2)
finally:
    driver.quit()
    print('Driver closed')
