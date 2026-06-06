import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import Profile


_jwks_client: jwt.PyJWKClient | None = None


def _get_jwks_client() -> jwt.PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        supabase_url = settings.SUPABASE_URL.rstrip("/")
        if not supabase_url:
            raise exceptions.AuthenticationFailed("SUPABASE_URL is not configured")
        # Caches keys in-process; PyJWKClient handles its own TTL.
        _jwks_client = jwt.PyJWKClient(
            f"{supabase_url}/auth/v1/.well-known/jwks.json",
            cache_keys=True,
        )
    return _jwks_client


class SupabaseAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith(f"{self.keyword} "):
            return None

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            return None

        try:
            signing_key = _get_jwks_client().get_signing_key_from_jwt(token).key
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=["ES256", "RS256"],
                audience="authenticated",
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.PyJWKClientError as exc:
            raise exceptions.AuthenticationFailed(f"JWKS error: {exc}")
        except jwt.PyJWTError as exc:
            raise exceptions.AuthenticationFailed(f"Invalid token: {exc}")

        user_id = payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Token missing sub claim")

        email = payload.get("email", "")
        metadata = payload.get("user_metadata", {}) or {}

        profile, _ = Profile.objects.update_or_create(
            id=user_id,
            defaults={
                "email": email,
                "name": metadata.get("name", "") or metadata.get("full_name", ""),
                "role": metadata.get("role", ""),
            },
        )
        return (profile, token)

    def authenticate_header(self, request) -> str:  # type: ignore
        return self.keyword
