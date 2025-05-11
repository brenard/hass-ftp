"""The FTP integration."""

from __future__ import annotations

import logging

from aioftp import Client
from aioftp.errors import AIOFTPException
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_BACKUP_PATH, DATA_BACKUP_AGENT_LISTENERS, DOMAIN
from .helpers import async_create_client, async_ensure_path_exists

type FtpConfigEntry = ConfigEntry[Client]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: FtpConfigEntry) -> bool:
    """Set up FTP from a config entry."""
    try:
        client = await async_create_client(
            hass=hass,
            host=entry.data[CONF_HOST],
            port=entry.data[CONF_PORT],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
        )
    except AIOFTPException as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_connect",
        ) from err

    path = entry.data.get(CONF_BACKUP_PATH, "/")

    # Ensure the backup directory exists
    if not await async_ensure_path_exists(client, path):
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_access_or_create_backup_path",
        )

    entry.runtime_data = client

    def async_notify_backup_listeners() -> None:
        for listener in hass.data.get(DATA_BACKUP_AGENT_LISTENERS, []):
            listener()

    entry.async_on_unload(entry.async_on_state_change(async_notify_backup_listeners))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: FtpConfigEntry) -> bool:
    """Unload a FTP config entry."""
    return True
