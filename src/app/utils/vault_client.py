"""Vault client for secure secret retrieval using AppRole authentication.

Supports KV v2 secrets engine and includes environment-aware namespace handling.
"""

import os
from functools import lru_cache
from typing import Any, Optional

import hvac
from tenacity import retry, stop_after_attempt, wait_fixed

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

VAULT_ADDR: str = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_ROLE_ID: str | None = os.getenv("VAULT_ROLE_ID")
VAULT_SECRET_ID: str | None = os.getenv("VAULT_SECRET_ID")
POLLER_NAME: str | None = os.getenv("POLLER_NAME")
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")


class VaultClient:
    """VaultClient handles authentication and secret retrieval from HashiCorp Vault using AppRole."""

    def __init__(self) -> None:
        """Initialize the Vault client and authenticate using AppRole.

        Raises:
            RuntimeError: If authentication fails or no token is returned.

        """
        self.client: hvac.Client = hvac.Client(url=VAULT_ADDR)
        self._authenticate()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _authenticate(self) -> None:
        """Authenticate to Vault using AppRole credentials.

        Raises:
            RuntimeError: If authentication response is missing a token.

        """
        if VAULT_ROLE_ID and VAULT_SECRET_ID:
            try:
                response: dict[str, Any] = self.client.auth_approle(VAULT_ROLE_ID, VAULT_SECRET_ID)
                if not response["auth"].get("client_token"):
                    raise RuntimeError("❌ Failed to retrieve Vault token from response.")
                logger.info("🔐 Vault AppRole authentication successful.")
            except Exception as e:
                logger.warning("⚠️ Vault authentication failed: %s", str(e))
                raise
        else:
            logger.warning("⚠️ VAULT_ROLE_ID or VAULT_SECRET_ID not provided. Vault auth skipped.")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get(self, key: str, fallback: str | None = None) -> str | None:
        """Retrieve a value from Vault for the given key.

        Args:
            key (str): The key to retrieve from Vault.
            fallback (Optional[str]): Value to return if Vault lookup fails.

        Returns:
            Optional[str]: The retrieved value or fallback if not found.

        """
        if not POLLER_NAME:
            logger.warning("⚠️ POLLER_NAME not set. Skipping Vault lookup for key: %s", key)
            return fallback

        secret_path: str = f"secret/data/{POLLER_NAME}/{ENVIRONMENT}"

        try:
            secret: dict[str, Any] = self.client.secrets.kv.v2.read_secret_version(
                path=f"{POLLER_NAME}/{ENVIRONMENT}"
            )
            value: Any | None = secret["data"]["data"].get(key)
            if value is not None:
                logger.debug("🔑 Vault value retrieved for key: %s", key)
                return str(value)
            logger.warning("⚠️ Key '%s' not found in Vault path '%s'.", key, secret_path)
        except Exception as e:
            logger.warning("⚠️ Failed to retrieve key '%s' from Vault: %s", key, str(e))

        return fallback


@lru_cache
def get_secret_or_env(key: str, default: str | None = None) -> str | None:
    """Retrieve a secret value from Vault or fallback to environment variable or default.

    Args:
        key (str): The secret key to retrieve.
        default (Optional[str]): Default value to return if key not found in Vault or env.

    Returns:
        Optional[str]: Retrieved value or fallback.

    """
    vault_client: VaultClient = VaultClient()
    return vault_client.get(key, fallback=os.getenv(key, default))
