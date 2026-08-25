from __future__ import annotations

from datetime import timedelta

DOMAIN = "tcl_androidtv_display"
CONF_SOURCE_ENTITY = "source_entity"
PLATFORMS = ["binary_sensor", "number", "select", "sensor", "switch"]
SCAN_INTERVAL = timedelta(seconds=30)

