from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import CONF_SOURCE_ENTITY, DOMAIN


class TclAndroidTvDisplayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            source = user_input[CONF_SOURCE_ENTITY]
            await self.async_set_unique_id(source)
            self._abort_if_unique_id_configured()
            state = self.hass.states.get(source)
            title = state.name if state else source
            return self.async_create_entry(title=f"{title} display", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_SOURCE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="media_player")
                )
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

