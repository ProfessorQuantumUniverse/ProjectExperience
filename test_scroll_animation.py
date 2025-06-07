import asyncio
from playwright.async_api import async_playwright, Playwright

async def run_test(playwright: Playwright):
    print("Launching browser...")
    browser = await playwright.firefox.launch()
    page = await browser.new_page()

    console_errors = []
    page.on("console", lambda msg: console_errors.append(f"Console [{msg.type}]: {msg.text}") if msg.type == "error" else None)

    print(f"Loading file:///app/index.html...")
    await page.goto("file:///app/index.html", wait_until="networkidle")
    print("Page loaded.")

    if console_errors:
        print("\\nInitial Console Errors:")
        for error in console_errors:
            print(error)
        # Clear console errors for next steps if needed, or just report them once
        # console_errors = []
    else:
        print("\\nNo initial console errors found.")

    section_modell_selector = "section#modell"
    footer_selector = "footer.site-footer"
    is_visible_class = "is-visible"

    # Test section#modell
    print(f"\\nScrolling to {section_modell_selector}...")
    section_modell = page.locator(section_modell_selector)
    await section_modell.scroll_into_view_if_needed()
    # Wait for potential transition
    await page.wait_for_timeout(1000) # 1 second for transition + observer callback

    section_classes = await section_modell.get_attribute("class")
    section_test_passed = is_visible_class in section_classes if section_classes else False
    print(f"Classes on {section_modell_selector}: {section_classes}")
    print(f"Test for {section_modell_selector}: {'PASSED' if section_test_passed else 'FAILED'}")

    # Test footer.site-footer
    print(f"\\nScrolling to {footer_selector}...")
    footer_element = page.locator(footer_selector)
    await footer_element.scroll_into_view_if_needed()
    # Wait for potential transition
    await page.wait_for_timeout(1000) # 1 second for transition + observer callback

    footer_classes = await footer_element.get_attribute("class")
    footer_test_passed = is_visible_class in footer_classes if footer_classes else False
    print(f"Classes on {footer_selector}: {footer_classes}")
    print(f"Test for {footer_selector}: {'PASSED' if footer_test_passed else 'FAILED'}")

    await browser.close()
    print("\\nBrowser closed.")

    print("\\nFinal Console Errors (if any new ones appeared during scrolling):")
    if console_errors:
        for error in console_errors:
            print(error)
    else:
        print("No console errors recorded during test execution.")

    return section_test_passed and footer_test_passed, console_errors

async def main():
    async with async_playwright() as playwright:
        success, errors = await run_test(playwright)
        print(f"\\nOverall test success: {success}")
        if errors:
            print("Errors were encountered during the test.")

if __name__ == "__main__":
    asyncio.run(main())
