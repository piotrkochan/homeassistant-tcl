from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TclConfigEntry
from .entity import TclDisplayEntity
from .protocol import set_adjustment, set_backlight

ADJUSTMENTS = {
    "brightness": ("Picture brightness", "mdi:brightness-6"),
    "contrast": ("Contrast", "mdi:contrast-box"),
    "hue": ("Hue", "mdi:palette-outline"),
    "sharpness": ("Sharpness", "mdi:image-filter-center-focus-strong"),
    "saturation": ("Saturation", "mdi:invert-colors"),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TclConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    del hass
    async_add_entities(
        [TclBacklightNumber(entry)]
        + [TclAdjustmentNumber(entry, key, name, icon) for key, (name, icon) in ADJUSTMENTS.items()]
    )


class TclBaseNumber(TclDisplayEntity, NumberEntity):
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_mode = NumberMode.SLIDER

    @property
    def native_value(self) -> float | None:
        value = self.coordinator.data.get(self._key)
        return float(value) if value is not None else None


class TclBacklightNumber(TclBaseNumber):
    _attr_name = "Backlight"
    _attr_icon = "mdi:brightness-percent"

    def __init__(self, entry: TclConfigEntry) -> None:
        super().__init__(entry, "backlight")
        self._key = "backlight"

    async def async_set_native_value(self, value: float) -> None:
        await self._entry.runtime_data.api.async_write(set_backlight(round(value)))
        await self.coordinator.async_request_refresh()


class TclAdjustmentNumber(TclBaseNumber):
    def __init__(self, entry: TclConfigEntry, key: str, name: str, icon: str) -> None:
        super().__init__(entry, key)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon

    async def async_set_native_value(self, value: float) -> None:
        await self._entry.runtime_data.api.async_write(set_adjustment(self._key, round(value)))
        await self.coordinator.async_request_refresh()

