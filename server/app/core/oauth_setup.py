from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/contacts.readonly",
]


# run script : uv run python app\core\oauth_setup.py


def main():
    flow= InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
    creds=flow.run_local_server(port=8080)

    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())
    print("\n✅ SUCCESS: token.json generated!")

if __name__ == "__main__":
    main()
