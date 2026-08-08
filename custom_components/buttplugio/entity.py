"""Entity base classes for buttplugio."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

if TYPE_CHECKING:
    from buttplug import ButtplugClient, ButtplugDevice

    from .data import ButtplugioConfigEntry


class ButtplugioHubEntity(Entity):
    """Buttplug.io Hub (Server) Entity class."""

    _attr_has_entity_name = True

    def __init__(self, client: ButtplugClient, entry: ButtplugioConfigEntry) -> None:
        """Initialise a server entity."""
        super().__init__()
        self._client = client
        self._entry = entry

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=client.server_name,
            manufacturer="Buttplug.io",
            model="Buttplug Server",
            entry_type=DeviceEntryType.SERVICE,
        )


class ButtplugioDeviceEntity(Entity):
    """Buttplug.io Device Entity class."""

    _attr_has_entity_name = True

    def __init__(
        self,
        client: ButtplugClient,
        entry: ButtplugioConfigEntry,
        device: ButtplugDevice,
    ) -> None:
        """Initialise a device entity."""
        super().__init__()
        self._client = client
        self._entry = entry
        self._device = device

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry.entry_id}_device_{device.index}")},
            name=device.display_name or device.name,
            manufacturer="Buttplug.io",
            model=device.name,
            via_device=(DOMAIN, entry.entry_id),
        )

    @callback
    def async_set_available(self, available: bool = True) -> None:  # noqa: FBT001, FBT002
        """Update entity availability state."""
        if self._attr_available != available:
            self._attr_available = available
            self.async_write_ha_state()

    @callback
    def async_set_unavailable(self) -> None:
        """Update entity availability state."""
        self.async_set_available(available=False)
