from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TclConfigEntry
from .entity import TclDisplayEntity
from .protocol import (
    COLOR_TEMPERATURE_NAMES,
    COLOR_TEMPERATURES,
    PICTURE_MODE_NAMES,
    PICTURE_MODES,
    set_color_temperature,
    set_picture_mode,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TclConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    del hass
    async_add_entities([TclPictureModeSelect(entry), TclColorTemperatureSelect(entry)])


class TclPictureModeSelect(TclDisplayEntity, SelectEntity):
    _attr_name = "Picture mode"
    _attr_icon = "mdi:image-filter-center-focus"
    _attr_options = list(PICTURE_MODES)

    def __init__(self, entry: TclConfigEntry) -> None:
        super().__init__(entry, "picture_mode")

    @property
    def current_option(self) -> str | None:
        return PICTURE_MODE_NAMES.get(self.coordinator.data.get("picture_mode"))

    async def async_select_option(self, option: str) -> None:
        await self._entry.runtime_data.api.async_write(set_picture_mode(PICTURE_MODES[option]))
        await self.coordinator.async_request_refresh()


class TclColorTemperatureSelect(TclDisplayEntity, SelectEntity):
    _attr_name = "Color temperature"
    _attr_icon = "mdi:temperature-kelvin"
    _attr_options = list(COLOR_TEMPERATURES)

    def __init__(self, entry: TclConfigEntry) -> None:
        super().__init__(entry, "color_temperature")

    @property
    def current_option(self) -> str | None:
        return COLOR_TEMPERATURE_NAMES.get(self.coordinator.data.get("color_temperature"))

    async def async_select_option(self, option: str) -> None:
        await self._entry.runtime_data.api.async_write(
            set_color_temperature(COLOR_TEMPERATURES[option])
        )
        await self.coordinator.async_request_refresh()

