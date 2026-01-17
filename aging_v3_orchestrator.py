import sys
import time
from core.bridge import HybridBridge
from modules.behavior import poisson_delay, silence_window
from config import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    bridge = HybridBridge()
    print("[Orchestrator] Authenticating...")
    token = bridge.authenticate()
    print("[Orchestrator] Starting profile...")
    profile_id, debug_port, profile_path = bridge.start_profile()
    print(f"[Orchestrator] Profile started: {profile_id}, Debug Port: {debug_port}")

    print("[Orchestrator] Performing Kernel Time Shift...")
    bridge.kernel_time_shift(profile_path)
    print("[Orchestrator] Time shift complete.")

    print("[Orchestrator] Launching Selenium...")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
    driver = webdriver.Chrome(options=chrome_options)

    print("[Orchestrator] Executing Poisson behavioral engine...")
    for _ in range(10):
        poisson_delay()
        driver.refresh()
        print("[Orchestrator] Refreshed browser.")

    silence_window()
    print("[Orchestrator] Stopping profile...")
    bridge.stop_profile()
    driver.quit()
    print("[Orchestrator] Done.")

if __name__ == "__main__":
    main()
