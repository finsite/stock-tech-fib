"""Vault client for secure secret retrieval using AppRole authentication.

Supports KV v2 secrets engine and includes environment-aware namespace handling.
"""

import os
import time

import hvac

from app.utils.setup_logger import setup_logger

__all__ = ["VaultClient", "get_secret_or_env"]

logger = setup_logger(__name__)


class VaultClient:
    """Handles interaction with HashiCorp Vault using AppRole authentication."""

    def __init__(self) -> None:
        """Initialize the VaultClient using environment variables and authenticate."""
        self.vault_addr: str = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
        self.role_id: str | None = os.getenv("VAULT_ROLE_ID")
        self.secret_id: str | None = os.getenv("VAULT_SECRET_ID")
        self.poller: str = os.getenv("POLLER_NAME", "stock_data_poller")
        self.environment: str = os.getenv("ENVIRONMENT", "dev")
        self.client: hvac.Client = hvac.Client(url=self.vault_addr)
        self.secrets: dict[str, str] = {}

        self._authenticate()
        self._load_secrets()

    def _authenticate(self) -> None:
        """Authenticate to Vault using AppRole credentials from the environment."""
        if not self.role_id or not self.secret_id:
            logger.warning("🔐 VAULT_ROLE_ID or VAULT_SECRET_ID not set — skipping Vault load.")
            return

        for attempt in range(1, 4):
            try:
                login = self.client.auth.approle.login(
                    role_id=self.role_id,
                    secret_id=self.secret_id,
                )
                if login and login.get("auth"):
                    self.client.token = login["auth"]["client_token"]
                    logger.info(f"🔓 Authenticated to Vault as {self.poller}.")
                    return
                logger.warning("⚠️ Vault login response missing 'auth'.")
            except Exception as e:
                logger.warning(f"⚠️ Vault login attempt {attempt} failed: %s", e)
                time.sleep(2)

        logger.error("❌ Failed to authenticate to Vault after 3 attempts.")

    def _load_secrets(self) -> None:
        """Load secrets from Vault's KV v2 engine using the configured path."""
        try:
            path = f"{self.poller}/{self.environment}"
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            self.secrets = response["data"]["data"]
            logger.info(f"📦 Loaded {len(self.secrets)} secrets from Vault.")
        except Exception as e:
            logger.warning("❌ Failed to load secrets from Vault: %s", e)
            self.secrets = {}

    def get(self, key: str, default: str | None = None) -> str | None:
        """Retrieve a secret by key.

        Args:
            key (str): The secret key to retrieve.
            default (str | None): The fallback value if key is not found.

        Returns:
            str | None: The secret value or the default.

        """
        return self.secrets.get(key, default)


# Singleton Vault client
_vault_client: VaultClient | None = None


def get_secret_or_env(key: str, default: str = "") -> str:
    """Return the secret from Vault or fall back to environment variable.

    Args:
        key (str): The secret key or environment variable name.
        default (str): Fallback value if not found.

    Returns:
        str: The resolved value.

    """
    global _vault_client
    if _vault_client is None:
        _vault_client = VaultClient()

    return _vault_client.get(key, os.getenv(key, default)) or default
