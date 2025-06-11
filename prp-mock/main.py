import jwt
import json
import httpx
import urllib.parse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configuration (fill with your values)
KEYCLOAK_SERVER_INTERNAL = "http://host.docker.internal:8080"
KEYCLOAK_SERVER_EXTERNAL = "http://localhost:8080"
REALM = "prp"
CLIENT_ID = "prpId"
CLIENT_SECRET = None  # Omit if public client
REDIRECT_URI = "http://localhost:8000/callback"

@app.get("/callback", response_class=HTMLResponse)
async def callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        return f"<h1>Error</h1><p>{error}</p>"

    if not code:
        return "<h1>No code received</h1>"

    # Exchange code for token
    token_url = f"{KEYCLOAK_SERVER_INTERNAL}/realms/{REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
    }
    if CLIENT_SECRET:
        data["client_secret"] = CLIENT_SECRET

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data=data)
        token_data = resp.json()

    # Optional: get the Keycloak public key and verify signature
    decoded = jwt.decode(token_data["access_token"], options={"verify_signature": False})
    pretty_token = json.dumps(decoded, indent=4)
    return f"""
    <h1>Token Response</h1>
    <pre>{pretty_token}</pre>
    """



@app.get("/", response_class=HTMLResponse)
def home():
    auth_url = (
        f"{KEYCLOAK_SERVER_EXTERNAL}/realms/{REALM}/protocol/openid-connect/auth"
        f"?client_id={CLIENT_ID}&response_type=code&scope=openid"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    )
    return f"""
    <html>
    <body>
        <h2>PRP</h2>
        <a href="{auth_url}">
            <button>Login</button>
        </a>
    </body>
    </html>
    """