"""Custom types for buttplugio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from buttplug import ButtplugClient
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration


type ButtplugioConfigEntry = ConfigEntry[ButtplugioData]


@dataclass
class ButtplugioData:
    """Data for the Blueprint integration."""

    client: ButtplugClient
    integration: Integration
