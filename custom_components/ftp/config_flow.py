"""Config flow for the FTP integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from aioftp.errors import AIOFTPException
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import CONF_BACKUP_PATH, DOMAIN
from .helpers import async_create_client

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): TextSelector(
            TextSelectorConfig(
                type=TextSelectorType.PASSWORD,
            )
        ),
        vol.Optional(CONF_BACKUP_PATH, default="/"): str,
    }
)


class FtpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FTP."""

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            # Check if we can connect to the FTP server
            try:
                client = await async_create_client(
                    hass=self.hass,
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
                await client.quit()
            except AIOFTPException:
                _LOGGER.exception("Connection error")
                errors["base"] = "cannot_connect"
            else:
                self._async_abort_entries_match(
                    {
                        CONF_HOST: user_input[CONF_HOST],
                        CONF_PORT: user_input[CONF_PORT],
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_BACKUP_PATH: user_input[CONF_BACKUP_PATH],
                    }
                )

                return self.async_create_entry(
                    title=(
                        f"{user_input[CONF_USERNAME]}@{user_input[CONF_HOST]}:"
                        f"{user_input[CONF_PORT]}/"
                        f"{user_input[CONF_BACKUP_PATH].strip('/')}"
                    ),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
