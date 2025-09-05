import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def _shot(url: str, out_path: Path, nav_timeout_ms=15000):
    async with async_playwright() as p:
        # Try multiple browser launch strategies
        browser = None
        
        # Strategy 1: Try system Chrome first (more likely to work)
        try:
            browser = await p.chromium.launch(
                channel="chrome",
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            print("[DEBUG] Using system Chrome successfully")
        except Exception as e:
            print(f"[DEBUG] System Chrome failed: {e}")
            
            # Strategy 2: Fallback to bundled Chromium
            try:
                browser = await p.chromium.launch(
                    headless=True,  # Use new headless mode
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor'
                    ]
                )
                print("[DEBUG] Using bundled Chromium successfully")
            except Exception as e2:
                print(f"[DEBUG] Bundled Chromium failed: {e2}")
                raise Exception(f"Both browser strategies failed: Chrome={e}, Chromium={e2}")
        
        context = await browser.new_context(viewport={"width": 1366, "height": 768})
        page = await context.new_page()
        page.set_default_navigation_timeout(nav_timeout_ms)
        await page.goto(url)
        await page.screenshot(path=str(out_path), full_page=True)
        title = await page.title()
        html = await page.content()
        await browser.close()
        return title, html

def take_screenshot(url: str, out_path: Path, nav_timeout_ms=15000):
    return asyncio.run(_shot(url, out_path, nav_timeout_ms))
