from __future__ import annotations

from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .protocol import batch_command, parse_batch


class TclAndroidTvApi:
    def __init__(self, hass: HomeAssistant, source_entity: str) -> None:
        self.hass = hass
        self.source_entity = source_entity

    async def async_read(self) -> dict[str, int]:
        source = self.hass.states.get(self.source_entity)
        if source is None or source.state in {STATE_UNAVAILABLE, STATE_UNKNOWN}:
            raise HomeAssistantError("Android TV ADB entity is not available")
        return await self.async_command(batch_command())

    async def async_write(self, command: str) -> None:
        await self.hass.services.async_call(
            "androidtv",
            "adb_command",
            {"entity_id": self.source_entity, "command": command},
            blocking=True,
        )

    async def async_command(self, command: str) -> dict[str, int]:
        await self.async_write(command)
        source = self.hass.states.get(self.source_entity)
        response = source.attributes.get("adb_response", "") if source else ""
        values = parse_batch(response)
        if "backlight" not in values:
            raise HomeAssistantError("TCL Binder response was not received")
        return values
