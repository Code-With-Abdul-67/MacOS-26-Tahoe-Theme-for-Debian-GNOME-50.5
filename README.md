# macOS 26 Tahoe Theme for Debian GNOME 50.5

> Make GNOME look and behave as close as possible to **macOS 26 Tahoe** — complete with liquid glass effects, a macOS dock, a menu bar, the genie minimize animation, SF Pro fonts, and matching themes, icons, and cursors.

---

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [File Structure](#file-structure)
4. [Quick Start](#quick-start)
5. [What the Installer Does](#what-the-installer-does)
6. [Extensions Installed](#extensions-installed)
7. [Assets Required](#assets-required)
8. [GNOME System Settings Applied](#gnome-system-settings-applied)
9. [Configuration Files](#configuration-files)
10. [Reverting Everything](#reverting-everything)
11. [Known Issues & Tips](#known-issues--tips)

---

## Overview

This project provides a **fully automated setup** that transforms a standard Debian GNOME desktop into a near-perfect recreation of macOS 26 Tahoe. It was built by:

1. Analyzing a fully configured live Debian GNOME 50.5 system
2. Capturing every extension setting directly from `dconf` and extension schema files
3. Generating complete documentation, default + custom config files, and a Python installer script

The installer handles dependency checks, extension downloads, all `dconf`/`gsettings` writes, and offers to log you out when done.

---

## System Requirements

| Requirement | Details |
|-------------|---------|
| OS | Debian Testing (or any Debian-based distro) |
| Desktop | GNOME 50.5 or newer |
| Python | 3.8 or newer |
| Packages | `gnome-shell-extensions`, `dconf-cli`, `curl`, `unzip` *(installer installs these)* |
| Disk space | ~50 MB for extensions |

---

## File Structure

```
Mac OS Theme for Debian with Gnome 50.5/
├── README.md               ← You are here
├── plan.md                 ← Original project requirements
├── documentation.md        ← Full technical docs for every extension & setting
├── settings_default.json   ← Factory-default settings for all extensions
├── settings_custom.json    ← Your personal custom settings (captured live)
└── install.py              ← Interactive Python installer & manager
```

---

## Quick Start

```bash
# Navigate to the project folder
cd ~/Desktop/"Mac OS Theme for Debian with Gnome 50.5"

# Run the installer
python3 install.py
```

You will see an interactive menu:

```
  ┌─────────────────────────────────────────────────┐
  │  What would you like to do?                     │
  │                                                 │
  │  1. Install extensions with DEFAULT settings    │
  │  2. Install extensions with CUSTOM settings     │
  │  3. Revert everything (uninstall & restore)     │
  │  4. Check system & dependencies only            │
  │  0. Exit                                        │
  └─────────────────────────────────────────────────┘
```

- Choose **1** for a clean default install
- Choose **2** to apply the exact personal settings from this system
- Choose **3** to undo everything and restore GNOME defaults
- Choose **4** to just check what's installed without making changes

After installation the script will ask:
> *"Installation complete. You need to log out of GNOME Shell for the changes to take full effect. Do you want to log out now? (yes/no)"*

Answering **yes** triggers `gnome-session-quit --logout --no-prompt` automatically.

---

## What the Installer Does

### Step 1 — Dependency Check
Verifies `dconf-cli`, `curl`, `unzip`, `gnome-shell-extensions`, and `python3-gi` are installed. If any are missing, it offers to run `sudo apt-get install` for you.

### Step 2 — Extension Installation
Downloads each extension as a `.zip` from its GitHub release URL, extracts it to `~/.local/share/gnome-shell/extensions/<uuid>/`, and compiles the GSettings schemas.

### Step 3 — Settings Application
Writes all settings to `dconf` and `gsettings` with correct GVariant types:
- String keys → `'value'`
- Boolean keys → `true` / `false`
- Integer/float keys → raw number
- List keys → `['a', 'b']`
- Tuples (e.g. Lintel weather location) → `('City', lat, lon, 'Timezone')`
- Nested dict subpaths (Blur My Shell) → written to their own dconf sub-paths

### Step 4 — Enable / Disable Extensions
Sets `org.gnome.shell enabled-extensions` to the full custom list, and adds conflicting extensions (`dash-to-panel`, `dash2dock-lite`, etc.) to `disabled-extensions`.

### Step 5 — Log-out Prompt
Asks if you want to log out immediately. If yes, sends a graceful logout signal to the GNOME session.

---

## Extensions Installed

| # | Extension | UUID | Version | Purpose |
|---|-----------|------|---------|---------|
| 1 | **AppMenu** | `appmenu@ChathurangaBW.github.io` | 15 | macOS-style menu bar with Apple logo |
| 2 | **Blur my Shell** | `blur-my-shell@aunetx` | 75 | Frosted-glass blur on panel, overview, popups |
| 3 | **Compiz Magic Lamp** | `compiz-alike-magic-lamp-effect@hermes83.github.com` | 25 | Genie/magic-lamp minimize animation |
| 4 | **Coverflow Alt-Tab** | `CoverflowAltTab@palatis.blogspot.com` | 88 | 3D Coverflow window switcher |
| 5 | **Dash2Dock Motion** | `dash2dock-motion@unmade.space` | — | macOS dock with magnification |
| 6 | **Just Perfection** | `just-perfection-desktop@just-perfection` | 37 | Hide Activities button, tune panel, tweak UI |
| 7 | **Lintel** | `lintel@topbar` | — | macOS menu bar + Notification Center + Control Center |
| 8 | **Liquid Glass** | `liquid-glass@thinkingcoding1231.gmail.com` | — | macOS Tahoe liquid glass effect on all surfaces |
| 9 | **Astra Monitor** | `monitor@astraext.github.io` | 62 | Minimal network I/O graph in panel |
| 10 | **System Monitor** | `sysmonitor@talhasiddique7` | 10 | CPU / RAM / swap readout in panel |
| 11 | **User Themes** | `user-theme@gnome-shell-extensions.gcampax.github.com` | 79 | Load custom shell theme from `~/.themes` |

### Key Extension Settings (Custom Profile)

#### AppMenu
- Apple logo in the top-left corner (`menu-icon: apple-logo`)
- Locks to focused app, no workspace indicator, no user switcher

#### Blur my Shell
- Panel: blur on, static-blur off, override-background on
- Overview: style-components 3 (full blur)
- Applications: corner-when-maximized enabled, opacity 255

#### Compiz Magic Lamp
- Duration: **500ms** (slower/smoother than default 400ms)
- Tiles: 15×20 (more fluid than default 10×10)

#### Dash2Dock Motion
- Position: bottom, icon size 48, magnify scale 1.42×
- Transparent background (opacity 0), glass outline enabled
- Running indicator: single dot (macOS style)
- Show-apps button hidden

#### Just Perfection
- Activities button: **hidden**
- Panel size: **30px** (taller, more macOS-like)
- Clock position: center
- Notification banners: top-right
- Quick settings toggle: hidden from panel
- Window preview captions & close buttons: hidden

#### Lintel
- Appearance: follows GNOME theme
- Notification Center widgets: battery, clock, calendar, system, weather
- Control Center: 16 macOS-style toggles (wifi, bluetooth, airdrop, dark mode, etc.)
- Weather: manually set to Karachi

#### Liquid Glass
- Enabled on: menus, quick settings, notifications, app windows, desktop menu
- All corner radii: **25px**
- All tint: neutral grey `#9a9996`, strength 0 (pure glass)
- Backdrop highlights on, displacement scale 0 (flat glass)
- Application content opacity: **0.80**

#### Astra Monitor
- Only network header visible (CPU/RAM/storage/GPU panels hidden)
- All colors: near-white `rgb(246,245,244)` to match panel text
- Network graph width: 45px, update rate: ~1 second

#### System Monitor
- Monochrome mode on, 1-second refresh
- Shows CPU + RAM + swap only

---

## Assets Required

These must be installed manually before running the installer (they are already present on this system):

### GTK + Shell Themes → `~/.themes/`
| Theme | Use |
|-------|-----|
| `MacTahoe-Dark` | Active GTK theme |
| `MacTahoe-Dark-blue` | Active GNOME Shell theme |
| `MacTahoe-Light` and variants | Alternative light mode |
| `WhiteSur-Dark` / `WhiteSur-Light` | Alternative macOS-style themes |

**Install source:** [WhiteSur-gtk-theme](https://github.com/vinceliuice/WhiteSur-gtk-theme) or [MacTahoe theme pack](https://www.pling.com/p/2215875/)

### Icon Themes → `~/.local/share/icons/`
| Icon Set | Use |
|----------|-----|
| `MacTahoe-dark` | Active icon theme |
| `MacTahoe`, `MacTahoe-light` | Variants |
| `Mkos-Big-Sur`, `Mkos-Big-Sur-Night` | Alternative icon sets |
| `WhiteSur-dark`, `WhiteSur-light` | Alternative macOS icons |

**Install source:** [WhiteSur-icon-theme](https://github.com/vinceliuice/WhiteSur-icon-theme)

### Cursor Themes → `~/.icons/`
| Cursor | Use |
|--------|-----|
| `WhPbqU-MacTahoe` | Active cursor (set as `MacTahoe`) |
| `Apple-cursors` | Alternative Apple cursor |
| `WhiteSur-cursors` | Alternative macOS cursor |

### Fonts → `~/.fonts/`
| Font File | Family |
|-----------|--------|
| `SF-Pro-Rounded-Regular.otf` | SF Pro Rounded (system UI) |
| `SF-Pro-Text-Bold.otf` | SF Pro Text Bold |
| `SF-Pro-Text-Medium.otf` | SF Pro Text Medium |
| `SF-Pro-Text-Regular.otf` | SF Pro Text Regular |

> **Note:** SF Pro fonts are Apple proprietary and cannot be redistributed. Extract them from macOS or a macOS installer image.

---

## GNOME System Settings Applied

| Category | Setting | Value |
|----------|---------|-------|
| Interface | GTK Theme | `MacTahoe-Dark` |
| Interface | Shell Theme | `MacTahoe-Dark-blue` |
| Interface | Icon Theme | `MacTahoe-dark` |
| Interface | Cursor Theme | `MacTahoe` |
| Interface | System Font | `SF Pro Rounded Bold 10` |
| Interface | Color Scheme | `prefer-dark` |
| Interface | Accent Color | `slate` |
| Interface | Font Antialiasing | `grayscale` |
| Interface | Hot Corners | `false` (disabled) |
| Interface | Battery Percentage | `true` (shown) |
| Interface | Clock Weekday | `true` (shown) |
| Window Manager | Button Layout | `close,minimize,maximize:` ← left side |
| Window Manager | Close Shortcut | `Ctrl+Q` |
| Mutter | Workspaces on Primary Only | `true` |

---

## Configuration Files

### `settings_default.json`
Contains the **factory default** values for every extension and GNOME system key. Use this to understand what changed, or to install a clean base without any personal tweaks.

### `settings_custom.json`
Contains **your exact personal settings** — captured live from dconf on 2026-10-17. Applying this file reproduces the setup exactly as it was on the day it was recorded.

Both files use the same JSON structure:
```json
{
  "gnome_system": { ... },
  "extensions": {
    "uuid@example": { "key": "value", ... },
    ...
  }
}
```

---

## Reverting Everything

Run the installer and choose option **3**:

```bash
python3 install.py
# → Choose 3
```

This will:
1. Reset all `org.gnome.desktop.interface` keys to defaults
2. Reset WM button layout, mutter, and keybinding settings
3. Disable all custom extensions (`enabled-extensions = []`)
4. Clear the shell theme (`user-theme name = ""`)
5. Optionally **delete** the extension directories from `~/.local/share/gnome-shell/extensions/`

---

## Known Issues & Tips

| Issue | Solution |
|-------|----------|
| Liquid Glass is slow/laggy | Reduce `glass-blur-downscale` from 4 → 2 in `settings_custom.json` before installing |
| AppMenu shows empty menus in Electron apps | Known limitation — Discord, Slack, VS Code expose limited menus via D-Bus |
| Dash2Dock Motion conflicts with another dock | Make sure `dash-to-panel` and `dash2dock-lite` stay in `disabled-extensions` |
| Shell theme not applying | Ensure `user-theme` extension is enabled and `~/.themes/MacTahoe-Dark-blue` exists |
| Settings don't take effect | Log out and log back in — GNOME Shell must restart to load new extension configs |
| GNOME version mismatch | Extensions are versioned for GNOME 50.5. Newer GNOME versions may need updated extension zips |
| SF Pro font missing | Install fonts manually to `~/.fonts/` and run `fc-cache -fv` |
| dconf: "No such schema" error | Run `glib-compile-schemas ~/.local/share/gnome-shell/extensions/<uuid>/schemas/` |

---

## How This Project Was Built

1. **Live system analysis** — All extension directories in `~/.local/share/gnome-shell/extensions/` were inspected, `metadata.json` was read for each, and `dconf dump /org/gnome/shell/extensions/` captured every live setting.
2. **Schema extraction** — Each extension's `.gschema.xml` was parsed to extract factory defaults, so the default config file reflects true upstream values.
3. **GNOME system settings** — `gsettings get` and `dconf dump` on `/org/gnome/desktop/interface/`, `/org/gnome/desktop/wm/`, and `/org/gnome/mutter/` captured the full system config.
4. **Documentation** — All findings were written into `documentation.md` with per-extension role descriptions and setting explanations.
5. **Config files** — `settings_default.json` and `settings_custom.json` were generated from schema data and live dconf data respectively.
6. **Installer script** — `install.py` was written to automate the entire setup: deps, extension download/install, dconf writes with correct GVariant types, enable/disable lists, and graceful logout.
7. **Banner fix** — The installer's ASCII art header was updated to use Unicode box-drawing block characters after the initial font rendering produced garbled output in the terminal.

---

*Generated: 2026-10-17 | System: Debian Testing, GNOME 50.5 | Profile: macOS 26 Tahoe Dark Blue*
