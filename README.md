# TCL Android TV Display

Home Assistant controls and sensors for TCL-specific display settings. The
integration reuses an existing Android TV integration with working ADB
commands. It does not establish a second ADB connection.

Tested with a TCL 65C8K. TCL Binder transactions can vary between models and
firmware versions.

## Entities

Writable entities:

- panel backlight
- picture brightness
- contrast
- hue
- sharpness
- saturation
- picture mode
- color temperature
- adaptive brightness

Read-only entities include panel frame rate, HDR signal, motion smoothing,
local dimming, VRR, ALLM and selected Game Master states. Unconfirmed gaming
mode mappings are deliberately exposed as numeric codes.

## Installation with HACS

1. Open HACS.
2. Add `https://github.com/piotrkochan/homeassistant-tcl` as a custom
   integration repository.
3. Install `TCL Android TV Display`.
4. Restart Home Assistant.
5. Open Settings, Devices & services, Add integration.
6. Select `TCL Android TV Display` and choose an existing Android TV ADB
   media-player entity.

Add the integration again with another Android TV entity to configure multiple
TCL televisions.

## Safety

Only setters verified by the source research are exposed as writable entities.
Other discovered transactions remain read-only. Commands are sent locally
through Home Assistant's `androidtv.adb_command` action.
