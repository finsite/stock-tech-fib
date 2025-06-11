"""Vault client for secure secret retrieval using AppRole authentication.

Supports KV v2 secrets engine and includes environment-aware namespace
handling.
"""

import os
import time

import hvac

from app.utils.setup_logger import setup_logger

__all__ = ["VaultClient", "get_secret_or_env"]

logger = setup_logger(__name__)


class VaultClient:
    """Handles interaction with HashiCorp Vault using AppRole
    authentication.
    """

    def __init__(self) -> None:
        """Initialize the VaultClient with environment variables and
        authenticate.
        """
        self.vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
        self.role_id = os.getenv("VAULT_ROLE_ID")
        self.secret_id = os.getenv("VAULT_SECRET_ID")
        self.poller = os.getenv("POLLER_NAME", "stock_data_poller")
        self.environment = os.getenv("ENVIRONMENT", "dev")
        self.client = hvac.Client(url=self.vault_addr)
        self.secrets: dict[str, str] = {}

        self._authenticate()
        self._load_secrets()

    def _authenticate(self) -> None:
        """Authenticate to Vault using AppRole credentials from the
        environment.
        """
        if not self.role_id or not self.secret_id:
            logger.warning("🔐 VAULT_ROLE_ID or VAULT_SECRET_ID not set — skipping Vault load.")
            return

        for attempt in range(3):
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
                logger.warning(f"⚠️ Vault login attempt {attempt + 1} failed: %s", e)
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
            key: The secret key to retrieve.
            default: Value to return if key is missing.

        Returns:
            The secret value or the default.

        """
        return self.secrets.get(key, default)


_vault_client: VaultClient | None = None


def get_secret_or_env(key: str, default: str = "") -> str:
    """Return the secret from Vault or fall back to environment variable.

    Args:
        key: The secret key to retrieve.
        default: Fallback value if not found.

    Returns:
        The secret value or the fallback/default.

    """
    global _vault_client
    if _vault_client is None:
        _vault_client = VaultClient()

    return _vault_client.get(key, os.getenv(key, default)) or default
