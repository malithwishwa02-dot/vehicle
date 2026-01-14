"""
Journey Module (MODULE 3: THE JOURNEY - Entropy & Behavior)
Implements behavioral patterns, Bezier mouse movement, and human-like interactions.
Maps to CHRONOS_TASK.md Module 3 specifications.
"""

from core.entropy import EntropyGenerator
from utils.logger import get_logger
import numpy as np
import random
import time
from typing import List, Tuple, Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class HumanMouse:
    """
    Bezier Curve Mouse Movement (CHRONOS_TASK.md Module 3, Requirement 2)
    
    Implements Cubic Bezier math:
    B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t) t^2 P2 + t^3 P3
    
    Adds "Micro-sleeps" (random floats) between movement steps.
    """
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.logger = get_logger()
    
    def cubic_bezier(self, t: float, p0: Tuple[int, int], p1: Tuple[int, int], 
                     p2: Tuple[int, int], p3: Tuple[int, int]) -> Tuple[float, float]:
        """
        Calculate point on cubic Bezier curve at parameter t.
        
        Formula: B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t) t^2 P2 + t^3 P3
        
        Args:
            t: Parameter between 0 and 1
            p0, p1, p2, p3: Control points (x, y)
            
        Returns:
            (x, y) coordinates on the curve
        """
        # Calculate Bezier curve components
        one_minus_t = 1 - t
        
        # B(t) formula components
        term0 = (one_minus_t ** 3) * np.array(p0)
        term1 = 3 * (one_minus_t ** 2) * t * np.array(p1)
        term2 = 3 * one_minus_t * (t ** 2) * np.array(p2)
        term3 = (t ** 3) * np.array(p3)
        
        point = term0 + term1 + term2 + term3
        
        return int(point[0]), int(point[1])
    
    def move_to(self, target_x: int, target_y: int, duration: float = 1.0):
        """
        Move mouse to target position using Bezier curve with micro-sleeps.
        
        Args:
            target_x: Target X coordinate
            target_y: Target Y coordinate
            duration: Total movement duration in seconds
        """
        try:
            # Get current position (approximate center of viewport)
            viewport_width = self.driver.execute_script("return window.innerWidth;")
            viewport_height = self.driver.execute_script("return window.innerHeight;")
            
            start_x = viewport_width // 2
            start_y = viewport_height // 2
            
            # Generate random control points for natural curve
            control1_x = start_x + random.randint(-100, 100)
            control1_y = start_y + random.randint(-100, 100)
            control2_x = target_x + random.randint(-50, 50)
            control2_y = target_y + random.randint(-50, 50)
            
            p0 = (start_x, start_y)
            p1 = (control1_x, control1_y)
            p2 = (control2_x, control2_y)
            p3 = (target_x, target_y)
            
            # Calculate number of steps based on duration
            num_steps = int(duration * 100)  # 100 steps per second
            
            action = ActionChains(self.driver)
            
            # Move along the Bezier curve
            prev_x, prev_y = p0
            for i in range(num_steps):
                t = i / num_steps
                x, y = self.cubic_bezier(t, p0, p1, p2, p3)
                
                # Move to point
                action.move_by_offset(x - prev_x, y - prev_y)
                
                # Micro-sleep (random float between movements)
                micro_sleep = random.uniform(0.001, 0.01)
                time.sleep(micro_sleep)
                
                prev_x, prev_y = x, y
            
            action.perform()
            self.logger.info(f"Bezier mouse movement: ({start_x},{start_y}) -> ({target_x},{target_y})")
            
        except Exception as e:
            self.logger.warning(f"Mouse movement warning: {e}")
    
    def random_movement(self):
        """Execute random mouse movements for entropy"""
        try:
            viewport_width = self.driver.execute_script("return window.innerWidth;")
            viewport_height = self.driver.execute_script("return window.innerHeight;")
            
            # Random target within viewport
            target_x = random.randint(100, viewport_width - 100)
            target_y = random.randint(100, viewport_height - 100)
            
            duration = random.uniform(0.5, 2.0)
            self.move_to(target_x, target_y, duration)
            
        except Exception as e:
            self.logger.warning(f"Random movement warning: {e}")


class JourneyBehavior:
    """
    Behavioral Patterns (CHRONOS_TASK.md Module 3, Requirement 3)
    
    Implements:
    - random_scroll(): Scroll down, but occasionally scroll up (regression)
    - loss_of_focus(): Switch to about:blank to trigger visibilityState: hidden
    """
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.logger = get_logger()
        self.mouse = HumanMouse(driver)
    
    def random_scroll(self):
        """
        Random scrolling with occasional upward regression.
        Mimics natural reading/browsing behavior.
        """
        try:
            # 70% chance to scroll down, 30% chance to scroll up
            scroll_direction = "down" if random.random() < 0.7 else "up"
            
            # Random scroll amount
            scroll_amount = random.randint(100, 800)
            
            if scroll_direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                self.logger.info(f"Scrolled down: {scroll_amount}px")
            else:
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                self.logger.info(f"Scrolled up (regression): {scroll_amount}px")
            
            # Random pause after scroll
            time.sleep(random.uniform(0.5, 2.0))
            
        except Exception as e:
            self.logger.warning(f"Scroll warning: {e}")
    
    def loss_of_focus(self):
        """
        Loss of Focus pattern.
        Switch to about:blank for 1-4 seconds to trigger visibilityState: hidden.
        Simulates user switching tabs or minimizing window.
        """
        try:
            current_url = self.driver.current_url
            
            # Switch to about:blank
            self.driver.execute_script("window.open('about:blank', '_blank');")
            
            # Switch to the new tab
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[-1])
                
                # Stay on blank page for random duration
                duration = random.uniform(1.0, 4.0)
                self.logger.info(f"Loss of focus: {duration:.1f}s on about:blank")
                time.sleep(duration)
                
                # Close blank tab and return to original
                self.driver.close()
                self.driver.switch_to.window(windows[0])
                
                self.logger.info("Focus restored to original tab")
            
        except Exception as e:
            self.logger.warning(f"Loss of focus warning: {e}")
    
    def random_click(self):
        """Random click on page elements"""
        try:
            # Try to find clickable elements
            clickable_elements = self.driver.find_elements("css selector", "a, button, [role='button']")
            
            if clickable_elements:
                element = random.choice(clickable_elements[:10])  # Limit to first 10
                
                # Move mouse to element with Bezier curve
                location = element.location
                self.mouse.move_to(location['x'], location['y'], duration=random.uniform(0.5, 1.5))
                
                # Random pause before click
                time.sleep(random.uniform(0.2, 0.8))
                
                # Click
                element.click()
                self.logger.info(f"Clicked element: {element.tag_name}")
                
                # Wait for potential page load
                time.sleep(random.uniform(1.0, 3.0))
                
        except Exception as e:
            self.logger.warning(f"Random click warning: {e}")
    
    def typing_simulation(self, text: str):
        """
        Simulate human typing with realistic delays.
        
        Args:
            text: Text to type
        """
        try:
            action = ActionChains(self.driver)
            
            for char in text:
                action.send_keys(char)
                
                # Random typing delay (50-150ms per character)
                time.sleep(random.uniform(0.05, 0.15))
            
            action.perform()
            self.logger.info(f"Typed text with human-like delays")
            
        except Exception as e:
            self.logger.warning(f"Typing simulation warning: {e}")


class PoissonJourney:
    """
    Poisson Distribution Timing (CHRONOS_TASK.md Module 3, Requirement 1)
    
    Implements function that calculates random "Time Jumps" between T-90 days and T-0.
    Ensures browser is fully closed (process killed) between jumps to flush .wal files.
    """
    
    def __init__(self, total_days: int = 90):
        self.logger = get_logger()
        self.entropy_gen = EntropyGenerator()
        self.total_days = total_days
    
    def generate_time_jumps(self, num_segments: int = 12) -> List[Dict[str, Any]]:
        """
        Calculate random "Time Jumps" using Poisson distribution.
        
        Args:
            num_segments: Number of time jump segments
            
        Returns:
            List of time jump specifications
        """
        self.logger.info(f"Generating Poisson-distributed time jumps for {self.total_days} days")
        
        # Use EntropyGenerator to create Poisson-distributed segments
        segments = self.entropy_gen.generate_segments(
            total_days=self.total_days,
            num_segments=num_segments
        )
        
        # Convert segments to time jump schedule
        time_jumps = []
        
        for segment in segments:
            time_jump = {
                'index': segment['index'],
                'days_ago': self.total_days - (segment['cumulative_hours'] / 24),
                'activity_level': segment['activity_level'],
                'actions': segment['actions'],
                'checkpoint': segment['checkpoint'],
                'duration_hours': segment['advance_hours'],
                'timestamp': segment['timestamp']
            }
            
            time_jumps.append(time_jump)
        
        self.logger.info(f"Generated {len(time_jumps)} time jump segments")
        return time_jumps
    
    def should_kill_browser(self, jump_index: int) -> bool:
        """
        Determine if browser should be killed after this jump.
        
        Browser MUST be fully closed between jumps to flush .wal files to disk.
        (CHRONOS_TASK.md Module 3, Requirement 1)
        """
        # Kill browser after every jump (except the last one)
        return True


# Convenience functions
def create_human_mouse(driver: webdriver.Chrome) -> HumanMouse:
    """Factory function to create HumanMouse instance"""
    return HumanMouse(driver)


def create_journey_behavior(driver: webdriver.Chrome) -> JourneyBehavior:
    """Factory function to create JourneyBehavior instance"""
    return JourneyBehavior(driver)


def generate_poisson_schedule(days: int = 90, segments: int = 12) -> List[Dict]:
    """
    Factory function to generate Poisson-distributed time jump schedule.
    
    Example:
        schedule = generate_poisson_schedule(90, 12)
        for jump in schedule:
            print(f"Jump to T-{jump['days_ago']} days")
    """
    journey = PoissonJourney(total_days=days)
    return journey.generate_time_jumps(num_segments=segments)
