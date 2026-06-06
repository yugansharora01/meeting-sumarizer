import base64
import hashlib
import hmac

def verify_request_from_recall(
    secret: str,
    headers: dict[str, str],
    payload: str | None,
) -> None:
    """
    Verify a Recall/Svix webhook request.

    Raises:
        ValueError: If verification fails.
    """

    msg_id = headers.get("webhook-id") or headers.get("svix-id")
    msg_timestamp = headers.get("webhook-timestamp") or headers.get("svix-timestamp")
    msg_signature = headers.get("webhook-signature") or headers.get("svix-signature")

    if not secret or not secret.startswith("whsec_"):
        raise ValueError(f"Verification secret ({secret}) is missing or invalid")

    if not msg_id or not msg_timestamp or not msg_signature:
        raise ValueError(
            f"Missing webhook ID ({msg_id}), "
            f"timestamp ({msg_timestamp}), "
            f"or signature ({msg_signature})"
        )

    # Decode secret
    prefix = "whsec_"
    base64_part = secret[len(prefix) :] if secret.startswith(prefix) else secret
    key = base64.b64decode(base64_part)

    payload_str = payload or ""

    # Create signed content
    to_sign = f"{msg_id}.{msg_timestamp}.{payload_str}"

    expected_sig = base64.b64encode(
        hmac.new(
            key,
            to_sign.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    ).decode("utf-8")

    # Verify signatures
    passed_sigs = msg_signature.split(" ")

    for versioned_sig in passed_sigs:
        try:
            version, signature = versioned_sig.split(",", 1)
        except ValueError:
            continue

        if version != "v1":
            continue

        sig_bytes = base64.b64decode(signature)
        expected_sig_bytes = base64.b64decode(expected_sig)

        if hmac.compare_digest(expected_sig_bytes, sig_bytes):
            return

    raise ValueError("No matching signature found")
