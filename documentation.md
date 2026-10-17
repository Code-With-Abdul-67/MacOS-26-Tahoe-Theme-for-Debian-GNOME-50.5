# macOS Tahoe Recreation on GNOME 50.5 — Complete Documentation

## System Information

| Item | Value |
|------|-------|
| OS | Debian Testing |
| Desktop Environment | GNOME 50.5 |
| GTK Theme | MacTahoe-Dark / MacTahoe-Dark-blue |
| Shell Theme | MacTahoe-Dark-blue |
| Icon Theme | MacTahoe-dark |
| Cursor Theme | MacTahoe (in `~/.icons/WhPbqU-MacTahoe`) |
| System Font | SF Pro Rounded Bold 10 |
| Document Font | SF Pro Rounded Bold 10 |
| Monospace Font | SF Pro Rounded Bold 10 |
| Color Scheme | Dark (prefer-dark) |
| Accent Color | Slate |
| Button Layout | `close,minimize,maximize:` (left side, macOS style) |

---

## Installed GNOME Shell Extensions

### 1. AppMenu (`appmenu@ChathurangaBW.github.io`)
- **Version:** 15
- **Source:** https://github.com/ChathurangaBW/AppMenu
- **Role in Setup:** Replaces the standard GNOME activities/app menu with a macOS-style menu bar that shows the focused application's name and menus in the top panel.
- **Key Custom Settings:**
  - `menu-icon`: `apple-logo` — shows the Apple logo in the top-left corner
  - `icon-size`: 15 — compact icon size
  - `lock-to-focused-app`: true — menu tracks the active app
  - `show-os-icon`: true — displays the OS icon
  - `show-user-switcher`: false — hidden for cleaner look
  - `show-workspace-indicator`: false — hidden
  - `use-real-menus`: true — uses actual app menus

---

### 2. Blur My Shell (`blur-my-shell@aunetx`)
- **Version:** 75
- **Source:** https://github.com/aunetx/blur-my-shell
- **Role in Setup:** Applies blur effects to the top panel, overview, application windows, and other shell elements to mimic macOS's frosted-glass aesthetic.
- **Key Custom Settings:**
  - Panel: blur enabled, static-blur off, `override-background` on, `corner-radius` 0
  - Applications: blur enabled, `corner-when-maximized` true, opacity 255, enable-all false
  - Overview: blur enabled, `style-components` 3
  - Dash-to-dock: `override-background` on, `style-dash-to-dock` 2, rounded pipeline
  - Popup: override-background on

---

### 3. Compiz Alike Magic Lamp Effect (`compiz-alike-magic-lamp-effect@hermes83.github.com`)
- **Version:** 25
- **Source:** https://github.com/hermes83/compiz-alike-magic-lamp-effect
- **Role in Setup:** Adds the iconic macOS "genie effect" (magic lamp) animation when minimizing/unminimizing windows.
- **Key Custom Settings:**
  - `effect`: `default`
  - `duration`: 500ms (slightly slower, more dramatic than default 400ms)
  - `x-tiles`: 15 (default 10)
  - `y-tiles`: 20 (default 10)

---

### 4. Coverflow Alt-Tab (`CoverflowAltTab@palatis.blogspot.com`)
- **Version:** 88
- **Source:** https://github.com/dsheeler/CoverflowAltTab
- **Role in Setup:** Replaces the default Alt+Tab switcher with a 3D Coverflow-style window switcher similar to macOS Exposé/Mission Control.
- **Key Custom Settings:**
  - `switcher-background-color`: `(0.44, 0.51, 0.59)` — blue-grey tint

---

### 5. Dash2Dock Motion (`dash2dock-motion@unmade.space`)
- **Source:** https://github.com/Unmade760/dash2dock-motion
- **Role in Setup:** Provides a macOS-style dock at the bottom of the screen with magnification effect, smooth animations, and glass-like appearance.
- **Key Custom Settings:**
  - `dock-position`: BOTTOM
  - `dash-max-icon-size`: 48
  - `magnify-max-scale`: 1.42 (magnification on hover)
  - `magnify-effect-width`: 413
  - `dock-fixed`: false (auto-hide capable)
  - `background-opacity`: 0.0 (transparent background)
  - `glass-outline`: true — glass border outline
  - `custom-theme-shrink`: true
  - `running-indicator-style`: DOT
  - `show-show-apps-button`: false
  - `edge-distance`: -4
  - `show-trash`: true

---

### 6. Just Perfection (`just-perfection-desktop@just-perfection`)
- **Version:** 37
- **Source:** https://gitlab.gnome.org/jrahmatzadeh/just-perfection
- **Role in Setup:** Fine-tunes many GNOME Shell UI elements — hides Activities button, tweaks panel size, disables various indicators that would look un-macOS-like.
- **Key Custom Settings:**
  - `activities-button`: false — Activities button hidden
  - `panel-size`: 30 — slightly taller panel
  - `clock-menu-position`: 1 (center)
  - `notification-banner-position`: 1 (top-right, like macOS)
  - `quick-settings`: false — quick settings hidden from panel
  - `workspace-popup`: false — workspace popup disabled
  - `dash-separator`: false
  - `window-preview-caption`: false
  - `window-preview-close-button`: false
  - `workspace-background-corner-size`: 0
  - `controls-manager-spacing-size`: 0
  - `panel-in-overview`: true
  - `startup-status`: 1

---

### 7. Lintel (`lintel@topbar`)
- **Source:** https://github.com/eliotBenitez/lintel
- **Role in Setup:** Transforms the top panel into a macOS-style menu bar with a Notification Center widget panel, weather, battery, calendar, and Control Center with macOS-like quick toggles.
- **Key Custom Settings:**
  - `appearance`: `follow-gnome`
  - `overview-mode`: `transparent`
  - `panel-height`: 5
  - `show-active-app`: false
  - `show-system-menu`: false
  - `text-mode`: `auto`
  - `control-center-mode`: `custom`
  - Control center controls: wifi, network, media, bluetooth, airdrop, stage-manager, screen-mirroring, dark-mode, focus, display, sound, night-light, screenshot, airplane, microphone, power-mode
  - Notification center widgets: battery, clock, calendar, system, weather
  - `weather-location`: Karachi (manually set)
  - `weather-location-mode`: manual
  - `h-padding`: -1
  - `clock-show-seconds`: false

---

### 8. Liquid Glass (`liquid-glass@thinkingcoding1231.gmail.com`)
- **Source:** https://github.com/ryohsuke1231/liquid-glass
- **Role in Setup:** Applies Apple's macOS 26 Tahoe "liquid glass" visual effect to menus, notifications, quick settings, and application windows — the most visually distinctive macOS Tahoe feature.
- **Key Custom Settings:**
  - `enable-menu-glass`: true — glass effect on menus
  - `enable-quick-settings-glass`: true — glass on quick settings
  - `enable-notification-glass`: true — glass notifications
  - `enable-application-glass`: true — glass on app windows
  - `enable-desktop-menu-glass`: true — desktop right-click glass
  - `application-glass-all-windows`: true
  - `application-corner-radius`: 25.0
  - `menu-corner-radius`: 25.0
  - `quick-settings-corner-radius`: 25.0
  - `notification-corner-radius`: 25.0
  - `application-content-opacity`: 0.80
  - `application-contrast`: 1.5
  - `blur-method`: 0
  - `glass-backdrop-highlights`: true
  - All tint colors: `#9a9996` (neutral warm grey)
  - All tint-strength: 0.0 (fully transparent glass)
  - `preferences-advanced`: true

---

### 9. Astra Monitor (`monitor@astraext.github.io`)
- **Version:** 62
- **Source:** https://github.com/AstraExt/astra-monitor
- **Role in Setup:** Provides a minimal, elegant system monitor in the top panel showing network I/O and CPU percentage in a macOS-like style.
- **Key Custom Settings:**
  - `theme-style`: dark
  - All monitor colors: `rgb(246,245,244)` (near-white, matches light panel text)
  - `network-header-graph`: true, `network-header-graph-width`: 45
  - `network-header-io`: true (speed display)
  - `network-update`: ~1.0 second
  - Processor, memory, storage, GPU headers: all hidden (`show=false`), only network visible
  - `compact-mode`: false

---

### 10. System Monitor (`sysmonitor@talhasiddique7`)
- **Version:** 10
- **Source:** https://extensions.gnome.org/extension/9838/system-monitor/
- **Role in Setup:** Additional lightweight system monitor showing CPU, RAM, and swap in the panel.
- **Key Custom Settings:**
  - `monochrome-mode`: true — white monochrome display
  - `refresh-interval`: 1 second
  - `show-cpu`: true
  - `show-ram`: true
  - `show-swap`: true
  - `show-gpu`: false
  - `show-network`: false

---

### 11. User Themes (`user-theme@gnome-shell-extensions.gcampax.github.com`)
- **Version:** 79
- **Source:** https://gitlab.gnome.org/GNOME/gnome-shell-extensions
- **Role in Setup:** Allows loading a custom GNOME Shell theme from `~/.themes`. Required to apply the MacTahoe-Dark-blue shell theme.
- **Key Custom Setting:**
  - `name`: `MacTahoe-Dark-blue`

---

## GNOME System Settings

### Desktop Interface

| Setting | Value |
|---------|-------|
| GTK Theme | `MacTahoe-Dark` |
| Shell Theme | `MacTahoe-Dark-blue` |
| Icon Theme | `MacTahoe-dark` |
| Cursor Theme | `MacTahoe` |
| Font | `SF Pro Rounded Bold 10` |
| Document Font | `SF Pro Rounded Bold 10` |
| Monospace Font | `SF Pro Rounded Bold 10` |
| Color Scheme | `prefer-dark` |
| Accent Color | `slate` |
| Font Antialiasing | `grayscale` |
| Show Battery % | `true` |
| Enable Animations | `true` |
| Hot Corners | `false` |
| Clock Show Weekday | `true` |
| Clock Show Date | `true` |

### Window Manager

| Setting | Value |
|---------|-------|
| Button Layout | `close,minimize,maximize:` |
| Close Shortcut | `<Control>q` |

### Mutter (Compositor)

| Setting | Value |
|---------|-------|
| Workspaces Only on Primary | `true` |

---

## Installed Assets

### Themes (`~/.themes/`)
Full MacTahoe theme collection — includes Dark, Dark-blue, Light, Light-blue, and many other variants. Also includes WhiteSur-Dark/Light themes. Active theme: **MacTahoe-Dark** (GTK) + **MacTahoe-Dark-blue** (Shell).

### Icons (`~/.local/share/icons/`)
- `MacTahoe` — main icon set
- `MacTahoe-dark` — dark variant (active)
- `MacTahoe-light`
- `Mkos-Big-Sur`, `Mkos-Big-Sur-Night`, `Mkos-Big-Sur-Panel-white`
- `WhiteSur`, `WhiteSur-dark`, `WhiteSur-light`

### Cursors (`~/.icons/`)
- `Apple-cursors`
- `WhiteSur-cursors`
- `WhPbqU-MacTahoe` (active via cursor-theme setting `MacTahoe`)

### Fonts (`~/.fonts/`)
- `SF Pro Rounded Regular` — system UI font
- `SF Pro Text Bold`, `SF Pro Text Medium`, `SF Pro Text Medium Italic`, `SF Pro Text Regular`

---

## Known Notes

1. **Liquid Glass** is the most resource-intensive extension. On lower-end hardware, reduce `glass-blur-downscale` from 4 to 2 for better performance.
2. **Lintel** replaces the default system menu. If Lintel is disabled, you lose the macOS-style notification center and control center.
3. **Dash2Dock Motion** can conflict with the default GNOME dash. Ensure `dash2dock-lite` and `dash-to-panel` remain in the disabled extensions list.
4. **AppMenu** requires applications to expose their menus via the app-menu protocol. Some Electron apps (Discord, Slack, VS Code) may show limited menus.
5. The **SF Pro** fonts are Apple proprietary — they are not redistributed by this script. You must have them installed at `~/.fonts/` manually (or they're already present as detected).
6. The **MacTahoe** theme pack must be installed at `~/.themes/` before applying settings.
7. After applying settings, a **GNOME Shell restart** (log out → log back in) is required. `Alt+F2 → r → Enter` also works if running X11.
8. Extensions not present in `~/.local/share/gnome-shell/extensions/` must be installed from [extensions.gnome.org](https://extensions.gnome.org) or their GitHub repos.
