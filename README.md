# Buttplug.io Integration

Custom integration for [buttplug.io][buttplug]

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

<!--[![hacs][hacsbadge]][hacs]-->

![Project Maintenance][maintenance-shield]

[![Ko-fi][kofibadge]][kofi]

## ✨ Features

- Vibrators

**This integration will set up the following platforms.**

| Platform | Description                                       |
| -------- | ------------------------------------------------- |
| `number` | Vibration intensity for vibrator device features. |
| `sensor` | Diagnostics (battery level, signal strength)      |
| `switch` | Scan for devices                                  |

## 🚀 Quick Start

### Step 1: Install the Integration

**Prerequisites:** This integration requires [HACS](https://hacs.xyz/) (Home Assistant Community Store) to be installed.

Click the button below to open the integration directly in HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Weissnix4711&repository=hass-buttplug&category=integration)

Then:

1. Click "Download" to install the integration
2. **Restart Home Assistant** (required after installation)

<details>
<summary><strong>Manual Installation (Advanced)</strong></summary>

If you prefer not to use HACS:

1. Download the `custom_components/buttplugio/` folder from this repository
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

</details>

### Step 2: Add and Configure the Integration

**Important:** You must have installed the integration first (see Step 1) and restarted Home Assistant!

#### Option 1: One-Click Setup (Quick)

Click the button below to open the configuration dialog:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=buttplugio)

1. Enter your Intiface or Buttplug server WebSocket URL (eg. `ws://localhost:12345`)

That's it!

#### Option 2: Manual Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for "Buttplug.io"
4. Follow the same setup steps as Option 1

### Step 3: Start Using!

Find all entities in **Settings** → **Devices & Services** → **Buttplug.io** → click on the device.

## Available Entities

### Sensors

- **Battery Level** (Diagnostic): Shows battery level as percentage
- **Signal Strength** (Diagnostic): Shows RSSI

### Switches

- **Scan for Devices**: Toggles scanning

### Number

- **Vibration Intensity**: Percentage

## Custom Services

The integration provides no services yet.

## Troubleshooting

### Enable Debug Logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
    default: info
    logs:
        custom_components.buttplugio: debug
```

### Common Issues

None yet.

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or improvements.

---

[buttplug]: https://buttplug.io/
[commits-shield]: https://img.shields.io/github/commit-activity/y/Weissnix4711/hass-buttplug.svg?style=for-the-badge
[commits]: https://github.com/Weissnix4711/hass-buttplug/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/Weissnix4711/hass-buttplug.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40Weissnix4711-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Weissnix4711/hass-buttplug.svg?style=for-the-badge
[releases]: https://github.com/Weissnix4711/hass-buttplug/releases
[user_profile]: https://github.com/Weissnix4711
[kofi]: https://ko-fi.com/thomasaldrian
[kofibadge]: https://img.shields.io/badge/ko--fi-donate-yellow.svg?style=for-the-badge
