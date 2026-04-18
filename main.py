import random

from playwright.sync_api import sync_playwright

bio_list_path = "bios_list.txt"

with open(bio_list_path, "r") as f:
    BIO_LIST = f.read().splitlines()

LINKEDIN_USERNAME = "abishan-arulselvan"

LINKEDIN_URL = f"https://www.linkedin.com/in/{LINKEDIN_USERNAME}/"
LINKEDIN_EDIT_BIO_URL = f"https://www.linkedin.com/in/{LINKEDIN_USERNAME}/edit/intro/"

BROWSER_STATE_PATH = "playwright/.auth/state.json"


def main():
    print("Hello from linkedin-bio-swapper!")

    # 1. Using playwright, navigate to linkedin.com, profile, and log in with the provided credentials.
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)

        # ADD LOGIC TO SEE IF STATE.JSON EXISTS, IF YES THEN LOAD THE COOKIES, ELSE PROCEED TO LOGIN.
        # ADD HERE

        context = browser.new_context(storage_state=BROWSER_STATE_PATH)
        page = context.new_page()

        print("Checking if user is already logged in...")
        if not page.get_by_role("button", name="Me", exact=True).is_visible():
            print("User is not logged in. Logging in...")

            # IMPLEMENT LOGIN LOGIC HERE. MAKE SURE TO SAVE THE COOKIES AFTER LOGIN SO THAT THE USER DOESN'T HAVE TO LOGIN EVERY TIME.
            return

        page.goto(LINKEDIN_EDIT_BIO_URL)

        # 2. Edit the bio, with a random bio from the list of bios.
        headline = page.get_by_test_id(
            "ui-core-tiptap-text-editor-wrapper"
        ).get_by_role("textbox")

        headline.clear()
        headline.fill(random.choice(BIO_LIST))

        # Linkedin forces you to input industry when changing the headline, so we need to select an industry as well.
        page.get_by_role("textbox", name="Industry*").click()
        page.get_by_role("textbox", name="Industry*").fill("cooking 👨🏼‍🍳")

        # 3. Save the changes.
        save_button = page.get_by_role("button", name="Save")
        save_button.click()

        page.wait_for_timeout(3000)

        storage = context.storage_state(path=BROWSER_STATE_PATH)


if __name__ == "__main__":
    main()
