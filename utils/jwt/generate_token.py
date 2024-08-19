import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET")
EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 1))


def generate_token() -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    payload = {"exp": exp}
    return jwt.encode(payload, SECRET, algorithm="HS256")


if __name__ == "__main__":
    generated_token = generate_token()
    print(f"Generated JWT Token: {generated_token}")
