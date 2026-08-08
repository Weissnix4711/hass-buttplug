"""
Custom integration to integrate Buttplug.io with Home Assistant.

For more details about this integration, please refer to
https://github.com/Weissnix4711/hass-buttplug
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from buttplug import (
    ButtplugClient,
    ButtplugConnectorError,
    ButtplugDevice,
    ButtplugHandshakeError,
)
from homeassistant.const import (
    CONF_URL,
    Platform,
)
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.loader import async_get_loaded_integration

from .const import (
    LOGGER,
    SIGNAL_DEVICE_ADDED,
    SIGNAL_DEVICE_REMOVED,
    SIGNAL_SERVER_DISCONNECT,
)
from .data import ButtplugioData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import ButtplugioConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    # Platform.BINARY_SENSOR,
    Platform.SWITCH,
    # Platform.BUTTON,
    Platform.NUMBER,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ButtplugioConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    client = ButtplugClient("Home Assistant")

    entry.runtime_data = ButtplugioData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
    )

    async def on_device_added(device: ButtplugDevice) -> None:
        LOGGER.debug("Device added: %s", device)
        signal = SIGNAL_DEVICE_ADDED.format(entry.entry_id)
        async_dispatcher_send(hass, signal, device)

    async def on_device_removed(device: ButtplugDevice) -> None:
        LOGGER.debug("Device removed: %s", device)
        signal = SIGNAL_DEVICE_REMOVED.format(entry.entry_id)
        async_dispatcher_send(hass, signal, device)

    async def on_server_disconnect() -> None:
        LOGGER.error("Buttplug server disconnected. Reloading.")
        signal = SIGNAL_SERVER_DISCONNECT.format(entry.entry_id)
        async_dispatcher_send(hass, signal)

        hass.async_create_task(hass.config_entries.async_reload(entry.entry_id))

    client.on_device_added = on_device_added
    client.on_device_removed = on_device_removed
    client.on_server_disconnect = on_server_disconnect

    try:
        await client.connect(url=entry.data[CONF_URL])
    except (ButtplugConnectorError, ButtplugHandshakeError) as err:
        msg = f"Failed to connect to Buttplug server: {err}"
        raise ConfigEntryNotReady(msg) from err

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ButtplugioConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        client = entry.runtime_data.client
        if client:
            await client.disconnect()
            await asyncio.sleep(0.5)

    return unload_ok
