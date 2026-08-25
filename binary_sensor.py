from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TclConfigEntry
from .entity import TclDisplayEntity

BINARY_SENSORS = {
    "signal_allm": ("ALLM active", "mdi:gamepad"),
    "signal_vrr": ("VRR active", "mdi:sync"),
    "motion_clarity": ("Motion clarity", "mdi:motion-play"),
    "low_latency": ("Low latency", "mdi:timer-outline"),
    "dolby_game": ("Dolby game", "mdi:dolby"),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TclConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    del hass
    async_add_entities(
        TclDisplayBinarySensor(entry, key, name, icon)
        for key, (name, icon) in BINARY_SENSORS.items()
    )


class TclDisplayBinarySensor(TclDisplayEntity, BinarySensorEntity):
    def __init__(self, entry, key, name, icon) -> None:
        super().__init__(entry, key)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get(self._key)
        return bool(value) if value is not None else None

