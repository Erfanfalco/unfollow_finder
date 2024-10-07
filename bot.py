import os
import time
import instaloader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = 'admin'
PWD = '12345678'


def setup_driver():
    chrome_service = Service('chromedriver.exe')  # Update this path
    driver = webdriver.Chrome(service=chrome_service)
    return driver


def complete_checkpoint(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "button"))
    ).click()

    # Add additional steps if required (e.g., solving CAPTCHA)
    print("Checkpoint completed. Please check your browser.")


web = instaloader.Instaloader()
driver = setup_driver()

print("#\n[ -- ] Logging in ...")
try:
    web.login(USERNAME, PWD)

    if web.checkpoint_required():
        checkpoint_url = web.checkpoint_url()
        complete_checkpoint(driver, checkpoint_url)

        # Wait for the user to complete the checkpoint
        input("Press Enter after completing the checkpoint...")

        # Retry the login attempt
        web.login(USERNAME, PWD)

    else:
        print("\n[ OK ] Successfully logged in as", USERNAME)

except instaloader.exceptions.TwoFactorAuthRequiredException:
    print("\n[ ! ] Two Factor Authentication Detected")
    CODE = input("[ -- ] Type down your 2FA code or simply deactivate it: ")
    web.two_factor_login(CODE)

finally:
    print("\n[ OK ] Logged in as", USERNAME + "\n")


profile = instaloader.Profile.from_username(web.context, USERNAME)

if not os.path.exists("_metadata"):  # Create a folder to store metadata
    os.mkdir("_metadata")

# Followers (users that I follow)
try:  # Retrieving
    with open(f"_metadata/{USERNAME}_followers.txt", "r") as file:
        following = file.read().splitlines()

    print("[ OK ] Retrieved following list from file.")

except FileNotFoundError:  # Creating
    print("[ -- ] Retrieving followers ...")
    start_time = time.time()
    following = [followee.username for followee in profile.get_followees()]

    with open(f"_metadata/{USERNAME}_followers.txt", "w") as file:
        for followee in following:
            file.write(followee + "\n")

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    print(f"[ OK ] Retrieved {len(following)} followers in {elapsed} seconds.")

# Followers (users that follow me)
try:  # Retrieving
    with open(f"_metadata/{USERNAME}_followers.txt", "r") as file:
        followers = file.read().splitlines()

    print("[ OK ] Retrieved followers list from file.\n")

except FileNotFoundError:  # Creating
    print("[ -- ] Retrieving followers ...")
    start_time = time.time()
    followers = [follower.username for follower in profile.get_followers()]

    with open(f"_metadata/{USERNAME}_followers.txt", "w") as file:
        for follower in followers:
            file.write(follower + "\n")

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    print(f"[ OK ] Retrieved {len(followers)} followers in {elapsed} seconds.\n")

# Unfollowers (users that I follow but do not follow me back)
unfollowers = [user for user in following if user not in followers]
print(f"[ OK ] {len(unfollowers)} users that you follow, but do not follow you back.")

with open(f"_metadata/{USERNAME}_unfollowers.txt", "w") as file:
    for unfollower in unfollowers:
        file.write(unfollower + "\n")

# Non-followers (users who follow you but you don't follow back)
none_followers = [user for user in followers if user not in following]
print(f"[ OK ] {len(none_followers)} users who follow you, but you do not follow them back.")

with open(f"_metadata/{USERNAME}_none_followers.txt", "w") as file:
    for none_follower in none_followers:
        file.write(none_follower + "\n")

print("\n[ OK ] All done.")
print("[ ! ] Check the _metadata folder for the results.")
