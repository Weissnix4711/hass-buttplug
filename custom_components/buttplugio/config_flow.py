"""Adds config flow for Buttplug.io integration."""

from __future__ import annotations

import voluptuous as vol
from buttplug import ButtplugClient, ButtplugConnectorError, ButtplugHandshakeError
from homeassistant import config_entries
from homeassistant.const import CONF_URL
from homeassistant.helpers import selector
from homeassistant.loader import async_get_loaded_integration

from .const import DEFAULT_URI, DOMAIN, LOGGER


class ButtplugioFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Buttplug.io Config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            url = user_input[CONF_URL]
            try:
                await self._test_connection(url)
            except (ButtplugConnectorError, ButtplugHandshakeError) as err:
                LOGGER.error("Failed to connect to Buttplug server: %s", err)
                _errors["base"] = "connection"
            except Exception as err:  # noqa: BLE001
                LOGGER.error(
                    "Unexpected error while connecting to Buttplug server: %s", err
                )
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Buttplug server at {url}",
                    data=user_input,
                )

        integration = async_get_loaded_integration(self.hass, DOMAIN)
        assert integration.documentation is not None, (  # noqa: S101
            "Integration documentation URL is not set in manifest.json"
        )

        return self.async_show_form(
            step_id="user",
            description_placeholders={
                "documentation_url": integration.documentation,
            },
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_URL,
                        default=(user_input or {}).get(CONF_URL, DEFAULT_URI),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self, url: str) -> None:
        """Test the connection to the Buttplug server."""
        client = ButtplugClient("Home Assistant Config test")
        await client.connect(url)
        await client.disconnect()
