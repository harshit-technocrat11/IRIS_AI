from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build

def test_connection():

    creds = Credentials.from_authorized_user_file("token.json")

    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", maxResults=3).execute()
    messages = results.get("messages", [])
    
    print(f"Success! Found {len(messages)} recent emails.\n{messages}")


if __name__ == "__main__":
    test_connection()
