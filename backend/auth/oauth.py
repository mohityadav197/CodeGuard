"""Registers the GitHub OAuth client (Authlib) used for user login."""

from authlib.integrations.starlette_client import OAuth

from backend.config import settings

oauth = OAuth()
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "read:user user:email repo"},
)
