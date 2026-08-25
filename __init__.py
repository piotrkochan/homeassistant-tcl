from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import TclAndroidTvApi
from .const import CONF_SOURCE_ENTITY, PLATFORMS
from .coordinator import TclDisplayCoordinator


@dataclass
class TclRuntimeData:
    api: TclAndroidTvApi
    coordinator: TclDisplayCoordinator


TclConfigEntry = ConfigEntry[TclRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: TclConfigEntry) -> bool:
    api = TclAndroidTvApi(hass, entry.data[CONF_SOURCE_ENTITY])
    coordinator = TclDisplayCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = TclRuntimeData(api, coordinator)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: TclConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

