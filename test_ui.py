from playwright.sync_api import sync_playwright
import os

def test_local_app():
    with sync_playwright() as p:
        # Launch a Chromium browser
        browser = p.chromium.launch(headless=False) # Set headless=True to run without UI
        page = browser.new_page()
        
        # Get the absolute path to your local index.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_url = f"file://{os.path.join(current_dir, 'index.html')}"
        
        print(f"Opening {file_url}...")
        page.goto(file_url)
        
        # Wait for the search bar to appear
        page.wait_for_selector("#searchInput")
        
        # Type something into the search bar
        print("Typing 'Rajkumar' into the search bar...")
        page.locator("#searchInput").fill("Rajkumar")
        
        # Wait a moment so you can see it happen (optional)
        page.wait_for_timeout(2000)
        
        # Take a screenshot to prove it worked
        screenshot_path = "test_screenshot.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # You could also assert that certain elements appear on the page
        # Example: assert page.locator(".teacher-name").first.is_visible()
        
        browser.close()

if __name__ == "__main__":
    test_local_app()
