import sys
from playwright.sync_api import expect, sync_playwright, Playwright
from rich.console import Console
from rich.text import Text
import os
from dotenv import load_dotenv

load_dotenv()

SUCCESS_TEXT = r"""
 ____  _   _  ____ ____ _____ ____ ____  _ _ _ 
/ ___|| | | |/ ___/ ___| ____/ ___/ ___|| | | |
\___ \| | | | |  | |   |  _| \___ \___ \| | | |
 ___) | |_| | |__| |___| |___ ___) |__) |_|_|_|
|____/ \___/ \____\____|_____|____/____/(_|_|_)
"""
FIRST_CHECKBOX_SELECTOR = "#modal > div > div > div.modal-content > div > div.additional-wrapper > div:nth-child(2) > div.additional-services-container > label:nth-child(1) > div > div > input[type=checkbox]"
SECOND_CHECKBOX_SELECTOR = "#modal > div > div > div.modal-content > div > div.additional-wrapper > div:nth-child(3) > div.additional-services-container > label.form-control.blink.checked > div > div > input[type=checkbox]"
USERNAME_INPUT_SELECTOR = "#modal > div > div > div.modal-content > div > div > form > div:nth-child(1) > div > input"
PASSWORD_INPUT_SELECTOR = "#modal > div > div > div.modal-content > div > div > form > div:nth-child(2) > div > input"

def schedule_barber_appointment(playwright: Playwright, barber, day, time):
	console = Console()

	start_text = Text("Scheduling an Appointments for ")
	start_text.append(f"{barber} ", style="bold blue")
	start_text.append("at ")
	start_text.append(f"{day} - {time}", style="bold blue")
	console.print()
	console.print(start_text)

	browser = playwright.chromium.launch()
	page = browser.new_page()

	page.goto("https://vicecitybarbers.rs/zakazivanje/")

	page.get_by_text(barber).click()

	try:
		page.get_by_text(day, exact=True).click()
	except:
		page.locator('.arrow.right').click()
		page.get_by_text("Sre", exact=True).click()

	try:
		page.get_by_text(time).click()
	except:
		console.print(f"{time} appointment not Available", style="bold red")
		return

	page.get_by_text('Šišanje Mašinica', exact=True).click()
	expect(page.locator(FIRST_CHECKBOX_SELECTOR)).to_be_checked()

	page.get_by_text('Shaver', exact=True).click()
	expect(page.locator(SECOND_CHECKBOX_SELECTOR)).to_be_checked()

	page.get_by_role("button", name="Nastavi").click()

	username = os.getenv("USERNAME")
	password = os.getenv("PASSWORD")

	page.locator(USERNAME_INPUT_SELECTOR).fill(username)
	page.locator(PASSWORD_INPUT_SELECTOR).fill(password)
	page.get_by_role("button", name="Prijavi se").click()

	# Action to Schedule an Appointment
	page.get_by_role("button", name="Potvrdi zakazivanje").click()

	# expect(page.get_by_role("button", name="Potvrdi zakazivanje")).to_be_visible()

	console.print(SUCCESS_TEXT, style="bold green on black")
	success_text = Text("Scheduled Barber Appointment at ")
	success_text.append(f"{day} - {time}", style="bold green")
	success_text.append(" with ")
	success_text.append(f"{barber}", style="bold green")
	console.print(success_text)

with sync_playwright() as playwright:
	console = Console()

	barber = sys.argv[1]
	day = sys.argv[2]
	time = sys.argv[3]

	barber = "Višnja" if barber == "visnja" else barber
	day = day.capitalize()
	day = "Čet" if day == "Cet" else day

	schedule_barber_appointment(playwright, barber, day, time)
