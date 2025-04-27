import logging
import os
from typing import Any

import hvac

logger = logging.getLogger(__name__)


def load_vault_secrets() -> dict[str, str]:
    """
    Load secrets from Vault using AppRole login, with fallback to empty dict.

    Returns
    -------
    dict[str, str]
        Dictionary of key-value secrets from the appropriate Vault path.
    """
    vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
    role_id = os.getenv("VAULT_ROLE_ID")
    secret_id = os.getenv("VAULT_SECRET_ID")
    poller = os.getenv("POLLER_NAME", "stock_data_poller")
    environment = os.getenv("ENVIRONMENT", "dev")

    if not role_id or not secret_id:
        logger.warning("🔐 VAULT_ROLE_ID or VAULT_SECRET_ID not set — skipping Vault load.")
        return {}

    try:
        client = hvac.Client(url=vault_addr)
        login = client.auth.approle.login(role_id=role_id, secret_id=secret_id)

        if not login or not login.get("auth"):
            logger.warning("⚠️ Vault AppRole login failed.")
            return {}

        token = login["auth"]["client_token"]
        client.token = token

        logger.info(f"🔓 Authenticated to Vault as {poller}.")

        path = f"secret/data/{poller}/{environment}"
        response = client.secrets.kv.v2.read_secret_version(path=f"{poller}/{environment}")
        return response["data"]["data"]

    except Exception as e:
        logger.warning(f"❌ Vault load failed: {e}")
        return {}
