"""Vault client for secure secret retrieval using AppRole authentication.

This module provides a client interface for reading secrets from HashiCorp Vault,
typically using AppRole-based authentication. Supports KV v2 secrets engine
and includes environment-aware namespace handling.
"""

import logging
import os
import time

import hvac

logger = logging.getLogger(__name__)


class VaultClient:
    """Handles interaction with HashiCorp Vault using AppRole
    authentication.

    Parameters
    ----------

    Returns
    -------


    """

    def __init__(self) -> None:
        """Initialize the VaultClient with environment variables and authenticate."""
        # Set Vault address, defaulting to local Vault server
        self.vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")

        # Retrieve AppRole credentials from environment variables
        self.role_id = os.getenv("VAULT_ROLE_ID")
        self.secret_id = os.getenv("VAULT_SECRET_ID")

        # Set poller and environment, with default values
        self.poller = os.getenv("POLLER_NAME", "stock_data_poller")
        self.environment = os.getenv("ENVIRONMENT", "dev")

        # Initialize the HVAC client with the Vault address
        self.client = hvac.Client(url=self.vault_addr)

        # Dictionary to store loaded secrets
        self.secrets: dict[str, str] = {}

        # Authenticate to Vault and load secrets
        self._authenticate()
        self._load_secrets()

    def _authenticate(self) -> None:
        """Authenticate to Vault using AppRole.

        This function attempts to authenticate to Vault using the AppRole
        authentication backend. It takes the role ID and secret ID from the
        environment and attempts to authenticate up to 3 times in case of
        failure.

        If the authentication is successful, it sets the client's token and
        logs a success message. If it fails, it logs an error message.

        Parameters
        ----------

        Returns
        -------


        """
        if not self.role_id or not self.secret_id:
            logger.warning("🔐 VAULT_ROLE_ID or VAULT_SECRET_ID not set — skipping Vault load.")
            return

        for attempt in range(3):
            try:
                login = self.client.auth.approle.login(
                    role_id=self.role_id, secret_id=self.secret_id
                )
                if login and login.get("auth"):
                    self.client.token = login["auth"]["client_token"]
                    logger.info(f"🔓 Authenticated to Vault as {self.poller}.")
                    return
                else:
                    logger.warning("⚠️ Vault login response missing 'auth'.")
            except Exception as e:
                logger.warning(f"⚠️ Vault login attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        logger.error("❌ Failed to authenticate to Vault after 3 attempts.")

    def _load_secrets(self) -> None:
        """Load secrets from Vault's KV v2 backend.

        This method constructs the path to the secrets based on the poller and environment
        attributes, attempts to read the secrets from Vault, and updates the internal secrets
        dictionary. If an error occurs during the process, it logs a warning and resets the
        secrets dictionary to empty.

        Parameters
        ----------

        Returns
        -------


        """
        try:
            # Construct the path for the secrets in Vault
            path = f"{self.poller}/{self.environment}"

            # Attempt to read the secret version from the specified path
            response = self.client.secrets.kv.v2.read_secret_version(path=path)

            # Update the internal secrets dictionary with the retrieved data
            self.secrets = response["data"]["data"]

            # Log the number of secrets successfully loaded
            logger.info(f"📦 Loaded {len(self.secrets)} secrets from Vault.")

        except Exception as e:
            # Log a warning if an error occurs and reset the secrets dictionary
            logger.warning(f"❌ Failed to load secrets from Vault: {e}")
            self.secrets = {}

    def get(self, key: str, default: str | None = None) -> str | None:
        """Retrieve a secret by key.

        This method accesses the internal secrets dictionary to fetch the value
        associated with the given key. If the key does not exist in the dictionary,
        it returns the provided default value.

        Args:
        ----
            key (str): The secret key to retrieve.
            default (Optional[str]): Default value to return if key not found.

        Parameters
        ----------
        key :
            str:
        default :
            str | None:  (Default value = None)
        key :
            str:
        default :
            str | None:  (Default value = None)
        key :
            str:
        default :
            str | None:  (Default value = None)
        key : str :

        default : str | None :
            (Default value = None)
        key: str :

        default: str | None :
             (Default value = None)

        Returns
        -------


        """
        # Retrieve the secret value from the dictionary, defaulting if not found
        return self.secrets.get(key, default)
