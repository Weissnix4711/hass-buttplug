"""Constants for buttplugio."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "buttplugio"
DEFAULT_URI = "ws://localhost:12345"
SIGNAL_DEVICE_ADDED = f"{DOMAIN}_device_added_{{}}"
SIGNAL_DEVICE_REMOVED = f"{DOMAIN}_device_removed_{{}}"
