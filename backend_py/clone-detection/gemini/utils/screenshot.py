import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def _shot(url: str, out_path: Path, nav_timeout_ms=15000):
    async with async_playwright() as p:
        # Try multiple browser launch strategies
        browser = None
        
        # Strategy 1: Try bundled Chromium first (most reliable after installation)
        try:
            browser = await p.chromium.launch(
                headless=True,  # Use default headless mode
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-first-run',
                    '--disable-default-apps',
                    '--disable-sync',
                    '--disable-translate',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-device-discovery-notifications',
                    '--disable-ipc-flooding-protection',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
                ]
            )
            print("[DEBUG] Using bundled Chromium successfully")
        except Exception as e:
            print(f"[DEBUG] Bundled Chromium failed: {e}")
            
            # Strategy 2: Try system Chrome with new headless mode
            try:
                browser = await p.chromium.launch(
                    channel="chrome",
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-extensions',
                        '--no-first-run',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
                    ]
                )
                print("[DEBUG] Using system Chrome successfully")
            except Exception as e2:
                print(f"[DEBUG] System Chrome failed: {e2}")
                
                # Strategy 3: Try Chrome with explicit new headless argument
                try:
                    browser = await p.chromium.launch(
                        channel="chrome",
                        headless=True,
                        args=[
                            '--headless=new',  # Force new headless mode via argument
                            '--no-sandbox',
                            '--disable-dev-shm-usage',
                            '--disable-gpu',
                            '--disable-web-security',
                            '--disable-features=VizDisplayCompositor',
                            '--disable-blink-features=AutomationControlled',
                            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
                        ]
                    )
                    print("[DEBUG] Using system Chrome with explicit new headless successfully")
                except Exception as e3:
                    print(f"[DEBUG] Chrome with explicit new headless failed: {e3}")
                    
                    # Strategy 4: Last resort - try any remaining options
                    print(f"[DEBUG] All browser strategies failed")
                    print(f"  - Bundled Chromium: {e}")
                    print(f"  - System Chrome: {e2}")
                    print(f"  - Chrome new headless: {e3}")
                    
                    # Check if Playwright browsers are installed
                    import subprocess
                    import sys
                    try:
                        result = subprocess.run([sys.executable, "-m", "playwright", "install", "--dry-run"], 
                                              capture_output=True, text=True, timeout=10)
                        if "chromium" not in result.stdout.lower():
                            print("\n💡 SOLUTION: Run 'playwright install chromium' to install browsers")
                        else:
                            print("\n💡 Browsers seem to be installed. This might be a Chrome version compatibility issue.")
                    except:
                        print("\n💡 SOLUTION: Run 'playwright install chromium' to install browsers")
                    
                    raise Exception(f"All browser launch strategies failed. Chrome may need update or there may be a compatibility issue.")
        
        context = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Set longer timeouts for complex sites
        page.set_default_navigation_timeout(nav_timeout_ms)
        page.set_default_timeout(nav_timeout_ms)
        
        # Add stealth JavaScript to hide automation detection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)
        
        # Add error handling for navigation with retries
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                print(f"[DEBUG] Navigation attempt {attempt + 1}/{max_retries + 1}")
                await page.goto(url, wait_until="domcontentloaded", timeout=nav_timeout_ms)
                # Wait a bit more for dynamic content to load
                await page.wait_for_timeout(3000)
                break
            except Exception as nav_error:
                if attempt == max_retries:
                    await browser.close()
                    raise Exception(f"Failed to navigate to {url} after {max_retries + 1} attempts: {nav_error}")
                else:
                    print(f"[DEBUG] Navigation attempt {attempt + 1} failed: {nav_error}")
                    await page.wait_for_timeout(2000)  # Wait before retry
        
        # Add error handling for screenshot - take BOTH screenshots
        try:
            # Take full page screenshot (shot1.png)
            shot1_path = out_path.parent / "shot1.png"
            await page.screenshot(path=str(shot1_path), full_page=True)
            
            # Take viewport screenshot (shot2.png) 
            shot2_path = out_path.parent / "shot2.png"
            await page.screenshot(path=str(shot2_path), full_page=False)
            
            # Also keep the original shot.png as viewport for compatibility
            await page.screenshot(path=str(out_path), full_page=False)
            
            print(f"[DEBUG] Screenshots saved: full={shot1_path}, viewport={shot2_path}")
        except Exception as screenshot_error:
            await browser.close()
            raise Exception(f"Failed to take screenshots: {screenshot_error}")
        
        title = await page.title()
        html = await page.content()
        await browser.close()
        return title, html

def take_screenshot(url: str, out_path: Path, nav_timeout_ms=15000):
    return asyncio.run(_shot(url, out_path, nav_timeout_ms))
