import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")

def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    print("domain is: ", domain)
    print("api_key is: ", api_key)
    return requests.post(
		f"https://api.mailgun.net/v3/{domain}/messages",
		auth=("api", api_key),
		data={"from": "Stores App <postmaster@domain>",
			"to": [to],
			"subject": subject,
			"text": body})

def send_user_registration_email(to, username):
    # avoid using DB Models here 
    return send_simple_message(to, "Successfully signed up", f"Hi {username}! You have successfully signed up to Stores.")
