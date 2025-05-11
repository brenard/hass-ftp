"""Helper functions for the FTP component."""

import logging

from aioftp import Client
from aioftp.errors import AIOFTPException
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
    if await client.exists(path):
        if not await client.is_dir(path):
            _LOGGER.error("%s exists on FTP server but is not a directory", path)
            return False
        return True

    _LOGGER.debug("%s directory does not exists on FTP server, create it", path)
    parts = path.rstrip("/").split("/")
    for i in range(1, len(parts) + 1):
        sub_path = "/" if parts[:i] == [""] else "/".join(parts[:i])
        _LOGGER.debug("Check '%s' directory on FTP server", str(sub_path))
        try:
            if await client.exists(sub_path):
                if not await client.is_dir(sub_path):
                    _LOGGER.error("%s exists on FTP server but is not a directory", sub_path)
                    return False
                _LOGGER.debug("%s directory already exists on FTP server", sub_path)
            elif await client.make_directory(sub_path):
                _LOGGER.debug("%s directory created on FTP server", sub_path)
            else:
                _LOGGER.error("Failed to create %s directory on FTP server", sub_path)
                return False
        except AIOFTPException:
            _LOGGER.exception("Failed to ensure if %s directory exists on FTP server", sub_path)
            return False

    _LOGGER.info("%s directory create on FTP server", path)
    return True
