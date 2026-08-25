from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TclConfigEntry
from .entity import TclDisplayEntity
from .protocol import HDR_NAMES, LOCAL_DIMMING_NAMES, MEMC_NAMES, VRR_NAMES

SENSORS = {
    "panel_hz": ("Panel frame rate", "mdi:motion-play-outline", "Hz", None),
    "signal_hdr": ("Video signal", "mdi:video-input-hdmi", None, HDR_NAMES),
    "memc_mode": ("Motion smoothing", "mdi:motion", None, MEMC_NAMES),
    "local_dimming": ("Local dimming", "mdi:theme-light-dark", None, LOCAL_DIMMING_NAMES),
    "vrr_mode": ("VRR mode", "mdi:gamepad-variant-outline", None, VRR_NAMES),
    "game_master": ("Game Master code", "mdi:gamepad-variant", None, None),
    "game_picture_mode": ("Game picture mode code", "mdi:controller-classic-outline", None, None),
    "dlg_mode": ("DLG mode code", "mdi:speedometer", None, None),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TclConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    del hass
    async_add_entities(
        TclDisplaySensor(entry, key, name, icon, unit, mapping)
        for key, (name, icon, unit, mapping) in SENSORS.items()
    )


class TclDisplaySensor(TclDisplayEntity, SensorEntity):
    def __init__(self, entry, key, name, icon, unit, mapping) -> None:
        super().__init__(entry, key)
        self._key = key
        self._mapping = mapping
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit
        if unit is not None:
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        value = self.coordinator.data.get(self._key)
        if value is None or self._mapping is None:
            return value
        return self._mapping.get(value, f"Code {value}")

