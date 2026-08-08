"""Sensor platform for buttplugio."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from buttplug import ButtplugDeviceError
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
)
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import SIGNAL_DEVICE_ADDED, SIGNAL_DEVICE_REMOVED
from .entity import ButtplugioDeviceEntity

if TYPE_CHECKING:
    from buttplug import ButtplugClient, ButtplugDevice
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import ButtplugioConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ButtplugioConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform for buttplugio."""
    client = entry.runtime_data.client
    entities: dict[int, list[ButtplugioDeviceEntity]] = {}

    @callback
    def async_add_new_device(device: ButtplugDevice) -> None:
        if device.index in entities:
            for entity in entities[device.index]:
                entity.async_set_available()
            return

        new_entities: list[ButtplugioDeviceEntity] = []
        if device.has_battery:
            new_entities.append(ButtplugioBatterySensor(client, entry, device))
        if device.has_rssi:
            new_entities.append(ButtplugioRssiSensor(client, entry, device))
        if new_entities:
            entities[device.index] = new_entities
            async_add_entities(new_entities)

    @callback
    def async_remove_device(device: ButtplugDevice) -> None:
        if device_entities := entities.get(device.index):
            for entity in device_entities:
                entity.async_set_unavailable()

    # Add existing devices
    for device in client.devices.values():
        async_add_new_device(device)

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, SIGNAL_DEVICE_ADDED.format(entry.entry_id), async_add_new_device
        )
    )
    entry.async_on_unload(
        async_dispatcher_connect(
            hass, SIGNAL_DEVICE_REMOVED.format(entry.entry_id), async_remove_device
        )
    )


class ButtplugioBatterySensor(ButtplugioDeviceEntity, SensorEntity):
    """Buttplug.io Battery Sensor class."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "battery"

    def __init__(
        self,
        client: ButtplugClient,
        entry: ButtplugioConfigEntry,
        device: ButtplugDevice,
    ) -> None:
        """Initialise battery sensor class."""
        super().__init__(client, entry, device)
        self._attr_unique_id = f"{entry.entry_id}_device_{device.index}_battery"

    @override
    async def async_update(self) -> None:
        try:
            val = await self._device.battery()
            self._attr_native_value = round(val * 100)
            self.async_set_available()
        except ButtplugDeviceError:
            self.async_set_unavailable()


class ButtplugioRssiSensor(ButtplugioDeviceEntity, SensorEntity):
    """Buttplug.io Signal Strength Sensor class."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "rssi"

    def __init__(
        self,
        client: ButtplugClient,
        entry: ButtplugioConfigEntry,
        device: ButtplugDevice,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(client, entry, device)
        self._attr_unique_id = f"{entry.entry_id}_device_{device.index}_rssi"

    @override
    async def async_update(self) -> None:
        try:
            val = await self._device.rssi()
            self._attr_native_value = val
            self.async_set_available()
        except ButtplugDeviceError:
            self.async_set_unavailable()
