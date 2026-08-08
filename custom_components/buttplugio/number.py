"""Number platform for buttplugio."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from buttplug import ButtplugDevice, DeviceFeature, DeviceOutputCommand, OutputType
from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import LOGGER, SIGNAL_DEVICE_ADDED, SIGNAL_DEVICE_REMOVED
from .entity import ButtplugioDeviceEntity

if TYPE_CHECKING:
    from buttplug import ButtplugClient
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import ButtplugioConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ButtplugioConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number platform for buttplugio."""
    client = entry.runtime_data.client
    entities: dict[int, list[ButtplugioDeviceEntity]] = {}

    @callback
    def async_add_new_device(device: ButtplugDevice) -> None:
        if device.index in entities:
            for entity in entities[device.index]:
                entity.async_set_available()
            return

        new_entities: list[ButtplugioDeviceEntity] = []

        features: list[DeviceFeature] = list(device.features.values())
        for feature in features:
            if feature.has_output(OutputType.VIBRATE):
                new_entities.append(
                    ButtplugioVibrateNumber(client, entry, device, feature)
                )
            if feature.has_output(OutputType.ROTATE):
                pass
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


class ButtplugioVibrateNumber(ButtplugioDeviceEntity, NumberEntity):
    """Buttplug.io Vibration Intensity Number class."""

    _attr_native_max_value = 100.0
    _attr_native_min_value = 0.0
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_translation_key = "vibrate"

    def __init__(
        self,
        client: ButtplugClient,
        entry: ButtplugioConfigEntry,
        device: ButtplugDevice,
        feature: DeviceFeature,
    ) -> None:
        """Initialise vibration number class."""
        super().__init__(client, entry, device)
        self._feature = feature
        self._attr_unique_id = f"{entry.entry_id}_device_{device.index}_vibrate"

        feature_name = feature.description or f"Feature {feature.index}"
        self._attr_translation_placeholders = {"feature_name": feature_name}

    @override
    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        unit_value = value / 100.0

        try:
            if unit_value > 0:
                await self._device.run_output(
                    DeviceOutputCommand(OutputType.VIBRATE, float(unit_value))
                )
            else:
                await self._device.stop()
            self.async_set_available()
            self.async_write_ha_state()
        except Exception as err:
            LOGGER.error("Cannot send command: %s", err)
            self.async_set_unavailable()
