from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5000/")
    page.get_by_role("link", name="Forms", exact=True).click()
    page.get_by_role("link", name="New form").click()
    page.get_by_label("Email").click()
    page.get_by_label("Email").fill("test@test.pl")
    page.get_by_label("Email").press("Tab")
    page.get_by_label("Password").fill("1234")
    page.get_by_role("button", name="Login").click()
    page.get_by_label("Title").click()
    page.locator("html").click()
    page.get_by_role("button", name="Create").click()
    page.get_by_label("Title").click()
    page.get_by_label("Title").fill("test")
    page.get_by_label("Description").click()
    page.get_by_label("Description").fill("test")
    page.get_by_role("button", name="Create").click()

    # form = Forms.query.filter_by(title='test').first()
    # print(form)


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
