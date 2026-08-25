from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TclConfigEntry
from .entity import TclDisplayEntity
from .protocol import set_adaptive_brightness


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TclConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    del hass
    async_add_entities([TclAdaptiveBrightnessSwitch(entry)])


class TclAdaptiveBrightnessSwitch(TclDisplayEntity, SwitchEntity):
    _attr_name = "Adaptive brightness"
    _attr_icon = "mdi:brightness-auto"

    def __init__(self, entry: TclConfigEntry) -> None:
        super().__init__(entry, "adaptive_brightness")

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get("adaptive_brightness"))

    async def async_turn_on(self, **kwargs: object) -> None:
        await self._entry.runtime_data.api.async_write(set_adaptive_brightness(True))
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: object) -> None:
        await self._entry.runtime_data.api.async_write(set_adaptive_brightness(False))
        await self.coordinator.async_request_refresh()

