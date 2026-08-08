"""Switch platform for buttplugio."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from buttplug import ButtplugConnectorError
from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
)
from homeassistant.const import (
    EntityCategory,
)
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .entity import ButtplugioHubEntity

if TYPE_CHECKING:
    from buttplug import ButtplugClient
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import ButtplugioConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: ButtplugioConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch platform for buttplugio."""
    client = entry.runtime_data.client
    async_add_entities([ButtplugioScanSwitch(client, entry)])


class ButtplugioScanSwitch(ButtplugioHubEntity, SwitchEntity):
    """Buttplug.io Server Scan Switch class."""

    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_entity_category = EntityCategory.CONFIG
    _attr_translation_key = "scan_devices"

    def __init__(
        self,
        client: ButtplugClient,
        entry: ButtplugioConfigEntry,
    ) -> None:
        """Initialize scan switch class."""
        super().__init__(client, entry)
        self._attr_unique_id = f"{entry.entry_id}_scan_devices"

    @property
    @override
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._client.scanning

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        try:
            await self._client.start_scanning()
        except ButtplugConnectorError as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN, translation_key="not_connected"
            ) from err

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        try:
            await self._client.stop_scanning()
        except ButtplugConnectorError as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN, translation_key="not_connected"
            ) from err
