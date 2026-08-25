from __future__ import annotations

import re

MARKER_PREFIX = "__TCL_ANDROIDTV_DISPLAY_"
PARCEL_RE = re.compile(r"00000000\s+([0-9a-fA-F]{8})")

READS: dict[str, tuple[int, tuple[int, ...]]] = {
    "backlight": (101, ()),
    "picture_mode": (27, ()),
    "adaptive_brightness": (107, ()),
    "brightness": (30, (0,)),
    "contrast": (32, (0,)),
    "hue": (34, (0,)),
    "sharpness": (36, (0,)),
    "saturation": (38, (0,)),
    "color_temperature": (54, (0,)),
    "panel_hz": (140, ()),
    "signal_allm": (21, (0,)),
    "signal_vrr": (21, (1,)),
    "signal_hdr": (21, (2,)),
    "motion_clarity": (77, (0,)),
    "memc_mode": (79, (0,)),
    "local_dimming": (97, ()),
    "vrr_mode": (125, (0,)),
    "dlg_mode": (129, (0,)),
    "low_latency": (142, (0,)),
    "game_picture_mode": (158, (0,)),
    "game_master": (160, (0,)),
    "dolby_game": (161, (0,)),
}

PICTURE_MODES = {
    "Standard": 0,
    "Vivid": 1,
    "Movie": 3,
    "Sports": 4,
    "Intelligent": 10,
    "Art": 12,
    "Filmmaker": 60,
}
PICTURE_MODE_NAMES = {value: name for name, value in PICTURE_MODES.items()}

COLOR_TEMPERATURES = {"Cool": 0, "Standard": 1, "Warm": 2}
COLOR_TEMPERATURE_NAMES = {
    0: "Cool",
    1: "Standard",
    2: "Warm",
    3: "Personal",
    4: "Custom",
}

HDR_NAMES = {
    0: "SDR",
    1: "HDR10",
    2: "HDR10+",
    3: "HLG",
    4: "HLG18",
    5: "Dolby Vision",
    6: "Premium HDR",
}
MEMC_NAMES = {
    0: "Off",
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Custom",
    5: "24p Film",
}
LOCAL_DIMMING_NAMES = {0: "Off", 1: "Low", 2: "Medium", 3: "High"}
VRR_NAMES = {
    0: "Off",
    1: "Basic",
    2: "FreeSync",
    3: "FreeSync Premium",
    4: "FreeSync Premium Pro",
    5: "G-Sync",
}

ADJUSTMENT_SETTERS = {
    "brightness": 29,
    "contrast": 31,
    "hue": 33,
    "sharpness": 35,
    "saturation": 37,
}


def service_call(transaction: int, *arguments: int) -> str:
    args = " ".join(f"i32 {value}" for value in arguments)
    return f"service call tcl_tv_display {transaction}{' ' if args else ''}{args}"


def batch_command() -> str:
    commands: list[str] = []
    for key, (transaction, arguments) in READS.items():
        commands.append(f"printf '\\n{MARKER_PREFIX}{key}__\\n'")
        commands.append(service_call(transaction, *arguments))
    # Keep backlight last for compatibility with older template-number parsers.
    commands.append(f"printf '\\n{MARKER_PREFIX}backlight_final__\\n'")
    commands.append(service_call(101))
    return "; ".join(commands)


def parse_batch(response: str) -> dict[str, int]:
    values: dict[str, int] = {}
    for section in response.split(MARKER_PREFIX)[1:]:
        key, separator, body = section.partition("__")
        if not separator:
            continue
        match = PARCEL_RE.search(body)
        if match:
            values[key] = int(match.group(1), 16)
    return values


def set_backlight(value: int) -> str:
    return service_call(100, 0, value, 2)


def set_adjustment(key: str, value: int) -> str:
    return service_call(ADJUSTMENT_SETTERS[key], 0, 0, value, 2)


def set_picture_mode(value: int) -> str:
    return service_call(26, 0, value, 2, 2)


def set_color_temperature(value: int) -> str:
    return service_call(53, 0, 0, value, 2)


def set_adaptive_brightness(enabled: bool) -> str:
    return service_call(106, int(enabled), 2)

