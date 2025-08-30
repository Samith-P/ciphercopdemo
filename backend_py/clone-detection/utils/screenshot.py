import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def _shot(url: str, out_path: Path, nav_timeout_ms=15000):
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")  # use system Chrome
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
