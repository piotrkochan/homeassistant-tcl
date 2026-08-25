from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TclAndroidTvApi
from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class TclDisplayCoordinator(DataUpdateCoordinator[dict[str, int]]):
    def __init__(self, hass: HomeAssistant, api: TclAndroidTvApi) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, int]:
        try:
            return await self.api.async_read()
        except Exception as err:
            raise UpdateFailed(str(err)) from err
