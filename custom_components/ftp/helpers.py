"""Helper functions for the FTP component."""

import logging

from aioftp import Client
from homeassistant.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)


@callback
async def async_create_client(
    *,
    hass: HomeAssistant,
    host: str,
    port: int,
    username: str,
    password: str,
) -> Client:
    """Create a FTP client."""
    client = Client()
    await client.connect(host, port)
    if username and password:
        await client.login(username, password)
    return client


async def async_ensure_path_exists(client: Client, path: str) -> bool:
    """Ensure that a path exists recursively on the FTP server."""
    parts = path.rstrip("/").split("/")
    for i in range(1, len(parts) + 1):
        sub_path = "/".join(parts[:i])
        if not await client.exists(sub_path) and not await client.make_directory(sub_path):
            return False

    return True
