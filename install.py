#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║          macOS Tahoe GNOME Theme — Installer & Manager                 ║
║          For Debian with GNOME 50.5 or newer                           ║
╚══════════════════════════════════════════════════════════════════════════╝

This script installs, configures, and reverts all GNOME Shell extensions
and system settings needed to make GNOME look like macOS 26 Tahoe.

Usage:
    python3 install.py

Requires: Python 3.8+, running GNOME session (for dconf/gsettings)
"""

import os
import sys
import json
import shutil
import subprocess
import time
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — edit these paths if you move the settings files
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()
SETTINGS_DEFAULT = SCRIPT_DIR / "settings_default.json"
SETTINGS_CUSTOM  = SCRIPT_DIR / "settings_custom.json"

# Extension install location (user-level, no root required)
EXT_DIR = Path.home() / ".local" / "share" / "gnome-shell" / "extensions"

# Extension UUIDs and their download URLs (GitHub releases / direct zip)
# Format: { uuid: (display_name, zip_url) }
# zip_url may be None if the extension is typically installed via the browser
EXTENSIONS = {
    "appmenu@ChathurangaBW.github.io": (
        "AppMenu",
        "https://github.com/ChathurangaBW/AppMenu/releases/download/v15/appmenu@ChathurangaBW.github.io.zip"
    ),
    "blur-my-shell@aunetx": (
        "Blur my Shell",
        "https://github.com/aunetx/blur-my-shell/releases/download/v75/blur-my-shell@aunetx.zip"
    ),
    "compiz-alike-magic-lamp-effect@hermes83.github.com": (
        "Compiz Alike Magic Lamp Effect",
        "https://github.com/hermes83/compiz-alike-magic-lamp-effect/archive/refs/heads/main.zip"
    ),
    "CoverflowAltTab@palatis.blogspot.com": (
        "Coverflow Alt-Tab",
        "https://github.com/dsheeler/CoverflowAltTab/releases/download/v88/CoverflowAltTab@palatis.blogspot.com.zip"
    ),
    "dash2dock-motion@unmade.space": (
        "Dash2Dock Motion",
        "https://github.com/Unmade760/dash2dock-motion/archive/refs/heads/main.zip"
    ),
    "just-perfection-desktop@just-perfection": (
        "Just Perfection",
        "https://gitlab.gnome.org/jrahmatzadeh/just-perfection/-/archive/37/just-perfection-37.zip"
    ),
    "lintel@topbar": (
        "Lintel",
        "https://github.com/eliotBenitez/lintel/archive/refs/heads/main.zip"
    ),
    "liquid-glass@thinkingcoding1231.gmail.com": (
        "Liquid Glass",
        "https://github.com/ryohsuke1231/liquid-glass/archive/refs/heads/main.zip"
    ),
    "monitor@astraext.github.io": (
        "Astra Monitor",
        "https://github.com/AstraExt/astra-monitor/releases/download/v62/monitor@astraext.github.io.zip"
    ),
    "sysmonitor@talhasiddique7": (
        "System Monitor",
        None  # Install from extensions.gnome.org manually
    ),
    "user-theme@gnome-shell-extensions.gcampax.github.com": (
        "User Themes",
        None  # Usually bundled with gnome-shell-extensions package
    ),
}

# Extensions that must be kept disabled (they conflict)
DISABLED_EXTENSIONS = [
    "dash2dock-lite@icedman.github.com",
    "dash-to-panel@jderose9.github.com",
    "monochrome-dock@custom",
    "vitals-linux@custom",
]

# GNOME system packages that should be present
REQUIRED_PACKAGES = [
    "gnome-shell-extensions",    # provides user-theme extension
    "dconf-cli",                 # dconf command
    "python3-gi",                # GObject introspection (optional, for future use)
    "curl",                      # downloading extensions
    "unzip",                     # extracting zips
]


# ─────────────────────────────────────────────────────────────────────────────
# COLOUR HELPERS
# ─────────────────────────────────────────────────────────────────────────────

class C:
    """ANSI colour codes."""
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"


def cprint(text: str, colour: str = C.WHITE, end: str = "\n") -> None:
    print(f"{colour}{text}{C.RESET}", end=end)


def header(text: str) -> None:
    width = 70
    cprint("\n" + "═" * width, C.CYAN)
    cprint(f"  {text}", C.BOLD + C.CYAN)
    cprint("═" * width, C.CYAN)


def step(text: str) -> None:
    cprint(f"  → {text}", C.BLUE)


def ok(text: str) -> None:
    cprint(f"  ✔  {text}", C.GREEN)


def warn(text: str) -> None:
    cprint(f"  ⚠  {text}", C.YELLOW)


def err(text: str) -> None:
    cprint(f"  ✗  {text}", C.RED)


def ask(prompt: str) -> str:
    return input(f"{C.CYAN}  ? {prompt}{C.RESET} ").strip().lower()


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def run(cmd: list, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command, optionally capturing output."""
    env = os.environ.copy()
    # Make sure dbus session is available for gsettings / dconf
    if "DBUS_SESSION_BUS_ADDRESS" not in env:
        uid = os.getuid()
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{uid}/bus"
    try:
        result = subprocess.run(
            cmd,
            env=env,
            check=check,
            capture_output=capture,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as exc:
        if check:
            err(f"Command failed: {' '.join(cmd)}")
            err(exc.stderr or "(no stderr)")
            raise
        return exc


def run_shell(cmd: str, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command string."""
    env = os.environ.copy()
    uid = os.getuid()
    if "DBUS_SESSION_BUS_ADDRESS" not in env:
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{uid}/bus"
    return subprocess.run(
        cmd, shell=True, env=env, check=check,
        capture_output=capture, text=True
    )


def check_root() -> bool:
    return os.geteuid() == 0


def check_gnome_running() -> bool:
    """Check if we're inside a GNOME session."""
    return os.environ.get("XDG_CURRENT_DESKTOP", "").upper() in ("GNOME", "UBUNTU:GNOME")


def dconf_write(path: str, value: str) -> None:
    """Write a single dconf key."""
    run(["dconf", "write", path, value])


def dconf_read(path: str) -> str:
    """Read a single dconf key value (returns empty string if not set)."""
    result = run(["dconf", "read", path], check=False, capture=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def gsettings_set(schema: str, key: str, value: str) -> None:
    """Set a gsettings key."""
    run(["gsettings", "set", schema, key, value])


def gsettings_reset(schema: str, key: str) -> None:
    """Reset a gsettings key to its default."""
    run(["gsettings", "reset", schema, key], check=False)


# ─────────────────────────────────────────────────────────────────────────────
# DEPENDENCY CHECKS
# ─────────────────────────────────────────────────────────────────────────────

def check_dependencies() -> bool:
    """
    Verify required system packages are installed.
    Offers to install them if missing (requires sudo).
    Returns True if all dependencies are satisfied.
    """
    header("Checking Dependencies")

    missing = []
    for pkg in REQUIRED_PACKAGES:
        result = run(["dpkg", "-s", pkg], check=False, capture=True)
        if result.returncode != 0:
            missing.append(pkg)
        else:
            ok(f"{pkg} — installed")

    if not missing:
        ok("All dependencies satisfied.")
        return True

    warn(f"Missing packages: {', '.join(missing)}")
    answer = ask("Install missing packages now? (requires sudo) [yes/no]:")
    if answer in ("yes", "y"):
        step("Running apt-get install...")
        try:
            run(["sudo", "apt-get", "install", "-y"] + missing)
            ok("Packages installed successfully.")
            return True
        except subprocess.CalledProcessError:
            err("Failed to install packages. Please install them manually and retry.")
            return False
    else:
        warn("Skipping package installation. Some steps may fail.")
        return False


def check_gnome_version() -> None:
    """Print the detected GNOME Shell version."""
    result = run(["dpkg", "-l", "gnome-shell"], check=False, capture=True)
    for line in result.stdout.splitlines():
        if line.startswith("ii"):
            parts = line.split()
            if len(parts) >= 3:
                ok(f"GNOME Shell version: {parts[2]}")
                return
    warn("Could not determine GNOME Shell version.")


# ─────────────────────────────────────────────────────────────────────────────
# EXTENSION MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

def is_extension_installed(uuid: str) -> bool:
    """Return True if the extension directory exists."""
    return (EXT_DIR / uuid).is_dir()


def download_extension(uuid: str, url: str) -> bool:
    """
    Download and extract a GNOME extension zip into EXT_DIR.
    Returns True on success.
    """
    import tempfile
    step(f"Downloading {uuid}...")
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "ext.zip")
        # Download
        result = run(["curl", "-fsSL", "-o", zip_path, url], check=False)
        if result.returncode != 0:
            warn(f"Download failed for {uuid}. You may need to install it manually.")
            warn(f"  URL: {url}")
            return False

        # Try to extract and find the correct subdirectory
        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        run(["unzip", "-q", "-o", zip_path, "-d", extract_dir])

        # Look for metadata.json to find the actual extension root
        meta_files = list(Path(extract_dir).rglob("metadata.json"))
        if not meta_files:
            warn(f"Could not find metadata.json in downloaded archive for {uuid}.")
            return False

        ext_root = meta_files[0].parent
        dest = EXT_DIR / uuid
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(str(ext_root), str(dest))

        # Compile GSettings schemas if present
        schema_dir = dest / "schemas"
        if schema_dir.is_dir():
            run(["glib-compile-schemas", str(schema_dir)], check=False)

        ok(f"Installed {uuid}")
        return True


def install_extensions(skip_download: bool = False) -> None:
    """
    Ensure all required extensions are installed.
    If skip_download is True, only reports missing ones.
    """
    header("Installing Extensions")
    EXT_DIR.mkdir(parents=True, exist_ok=True)

    not_found = []
    for uuid, (name, url) in EXTENSIONS.items():
        if is_extension_installed(uuid):
            ok(f"{name} ({uuid}) — already installed")
            continue

        if skip_download or url is None:
            warn(f"{name} ({uuid}) — NOT installed")
            if url is None:
                warn(f"  Install from: https://extensions.gnome.org or its GitHub page")
            not_found.append(uuid)
        else:
            success = download_extension(uuid, url)
            if not success:
                not_found.append(uuid)

    if not_found:
        warn("\nSome extensions could not be installed automatically.")
        warn("Please install them manually from https://extensions.gnome.org:")
        for uuid in not_found:
            name = EXTENSIONS[uuid][0]
            cprint(f"    • {name}  [{uuid}]", C.YELLOW)


def enable_extensions(uuids: list) -> None:
    """Enable a list of extensions via gsettings."""
    step("Enabling extensions...")
    # Build the GVariant array string
    quoted = ", ".join(f"'{u}'" for u in uuids)
    value = f"[{quoted}]"
    gsettings_set("org.gnome.shell", "enabled-extensions", value)
    ok("Extensions enabled.")


def disable_extensions_list(uuids: list) -> None:
    """Add extensions to the disabled list."""
    if not uuids:
        return
    step("Disabling conflicting extensions...")
    quoted = ", ".join(f"'{u}'" for u in uuids)
    value = f"[{quoted}]"
    gsettings_set("org.gnome.shell", "disabled-extensions", value)
    ok("Conflicting extensions disabled.")


# ─────────────────────────────────────────────────────────────────────────────
# SETTINGS APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def apply_gnome_system_settings(sys_cfg: dict) -> None:
    """Apply org.gnome.desktop.interface and WM settings."""
    header("Applying GNOME System Settings")

    iface = sys_cfg.get("interface", {})
    schema = "org.gnome.desktop.interface"

    str_keys = [
        "gtk-theme", "icon-theme", "cursor-theme", "font-name",
        "document-font-name", "monospace-font-name", "color-scheme",
        "accent-color", "font-antialiasing",
    ]
    bool_keys = [
        "show-battery-percentage", "enable-animations", "enable-hot-corners",
        "clock-show-weekday", "clock-show-date", "clock-show-seconds",
        "toolkit-accessibility",
    ]
    int_keys = ["cursor-size", "scaling-factor"]

    for key in str_keys:
        if key in iface:
            val = iface[key]
            gsettings_set(schema, key, f"'{val}'")
            ok(f"  {key} = '{val}'")

    for key in bool_keys:
        if key in iface:
            val = "true" if iface[key] else "false"
            gsettings_set(schema, key, val)
            ok(f"  {key} = {val}")

    for key in int_keys:
        if key in iface:
            val = str(iface[key])
            # scaling-factor needs uint32 cast
            if key == "scaling-factor":
                gsettings_set(schema, key, f"uint32 {val}")
            else:
                gsettings_set(schema, key, val)
            ok(f"  {key} = {val}")

    # WM preferences
    wm_prefs = sys_cfg.get("wm_preferences", {})
    for key, val in wm_prefs.items():
        gsettings_set("org.gnome.desktop.wm.preferences", key, f"'{val}'")
        ok(f"  wm.{key} = '{val}'")

    # WM keybindings
    wm_keys = sys_cfg.get("wm_keybindings", {})
    for key, val in wm_keys.items():
        # val is a list of strings
        quoted = ", ".join(f"'{v}'" for v in val)
        gsettings_set("org.gnome.desktop.wm.keybindings", key, f"[{quoted}]")
        ok(f"  keybinding.{key} = {val}")

    # Mutter
    mutter_cfg = sys_cfg.get("mutter", {})
    for key, val in mutter_cfg.items():
        v = "true" if val else "false"
        gsettings_set("org.gnome.mutter", key, v)
        ok(f"  mutter.{key} = {v}")


def _to_dconf_value(val) -> str:
    """
    Convert a Python value to a dconf-compatible GVariant string.
    Handles: str, bool, int, float, list, dict.
    """
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float):
        return str(val)
    if isinstance(val, str):
        # Already a quoted string like 'rgb(...)' or a plain string?
        if val.startswith("'") and val.endswith("'"):
            return val
        return f"'{val}'"
    if isinstance(val, list):
        items = ", ".join(_to_dconf_value(i) for i in val)
        return f"[{items}]"
    if isinstance(val, dict):
        # Serialize as a JSON string stored as a GVariant string
        return f"'{json.dumps(val)}'"
    return f"'{val}'"


# Map extension UUIDs to their dconf path prefixes
EXTENSION_DCONF_PATHS = {
    "appmenu@ChathurangaBW.github.io":
        "/org/gnome/shell/extensions/appmenu/",
    "blur-my-shell@aunetx":
        "/org/gnome/shell/extensions/blur-my-shell/",
    "compiz-alike-magic-lamp-effect@hermes83.github.com":
        "/org/gnome/shell/extensions/com/github/hermes83/compiz-alike-magic-lamp-effect/",
    "CoverflowAltTab@palatis.blogspot.com":
        "/org/gnome/shell/extensions/coverflowalttab/",
    "dash2dock-motion@unmade.space":
        "/org/gnome/shell/extensions/dash2dock-motion/",
    "just-perfection-desktop@just-perfection":
        "/org/gnome/shell/extensions/just-perfection/",
    "lintel@topbar":
        "/org/gnome/shell/extensions/lintel/",
    "liquid-glass@thinkingcoding1231.gmail.com":
        "/org/gnome/shell/extensions/liquid-glass/",
    "monitor@astraext.github.io":
        "/org/gnome/shell/extensions/astra-monitor/",
    "sysmonitor@talhasiddique7":
        "/org/gnome/shell/extensions/sysmon/",
    "user-theme@gnome-shell-extensions.gcampax.github.com":
        "/org/gnome/shell/extensions/user-theme/",
}

# Keys that need special treatment (nested dicts → sub-paths)
BLUR_SUBPATHS = {
    "appfolder":        "/org/gnome/shell/extensions/blur-my-shell/appfolder/",
    "applications":     "/org/gnome/shell/extensions/blur-my-shell/applications/",
    "coverflow-alt-tab":"/org/gnome/shell/extensions/blur-my-shell/coverflow-alt-tab/",
    "dash-to-dock":     "/org/gnome/shell/extensions/blur-my-shell/dash-to-dock/",
    "lockscreen":       "/org/gnome/shell/extensions/blur-my-shell/lockscreen/",
    "overview":         "/org/gnome/shell/extensions/blur-my-shell/overview/",
    "panel":            "/org/gnome/shell/extensions/blur-my-shell/panel/",
    "popup":            "/org/gnome/shell/extensions/blur-my-shell/popup/",
    "screenshot":       "/org/gnome/shell/extensions/blur-my-shell/screenshot/",
    "window-list":      "/org/gnome/shell/extensions/blur-my-shell/window-list/",
}


def apply_extension_settings(ext_cfg: dict) -> None:
    """Write all extension settings to dconf."""
    header("Applying Extension Settings")

    for uuid, settings in ext_cfg.items():
        name = settings.get("_name", uuid)
        step(f"Configuring {name}...")
        base_path = EXTENSION_DCONF_PATHS.get(uuid)
        if not base_path:
            warn(f"  No dconf path known for {uuid}, skipping.")
            continue

        for key, val in settings.items():
            # Skip metadata keys
            if key.startswith("_"):
                continue

            # Blur My Shell has nested sub-path objects
            if uuid == "blur-my-shell@aunetx" and key in BLUR_SUBPATHS:
                sub_path = BLUR_SUBPATHS[key]
                if isinstance(val, dict):
                    for sub_key, sub_val in val.items():
                        dconf_write(sub_path + sub_key, _to_dconf_value(sub_val))
                continue

            # Astra Monitor stores some values as JSON-string in dconf
            if uuid == "monitor@astraext.github.io" and isinstance(val, (list, dict)):
                dconf_write(base_path + key, f"'{json.dumps(val)}'")
                continue

            # Lintel weather-location is a tuple
            if uuid == "lintel@topbar" and key == "weather-location" and isinstance(val, list):
                if len(val) == 4:
                    dconf_write(
                        base_path + key,
                        f"('{val[0]}', {val[1]}, {val[2]}, '{val[3]}')"
                    )
                    continue

            # Lintel notification-center-widget-sizes is a dict → GVariant dict
            if uuid == "lintel@topbar" and key in (
                "notification-center-widget-sizes",
                "control-center-control-sizes",
            ) and isinstance(val, dict):
                inner = ", ".join(f"'{k}': '{v}'" for k, v in val.items())
                dconf_write(base_path + key, "{" + inner + "}")
                continue

            dconf_write(base_path + key, _to_dconf_value(val))

        ok(f"  {name} configured.")


def apply_settings_from_file(settings_file: Path) -> None:
    """Load settings JSON and apply everything."""
    if not settings_file.exists():
        err(f"Settings file not found: {settings_file}")
        sys.exit(1)

    with open(settings_file, "r") as f:
        cfg = json.load(f)

    sys_cfg = cfg.get("gnome_system", {})
    apply_gnome_system_settings(sys_cfg)

    shell_cfg = sys_cfg.get("shell", {})
    enabled = shell_cfg.get("enabled-extensions", list(EXTENSIONS.keys()))
    disabled = shell_cfg.get("disabled-extensions", DISABLED_EXTENSIONS)

    enable_extensions(enabled)
    disable_extensions_list(disabled)

    ext_cfg = cfg.get("extensions", {})
    apply_extension_settings(ext_cfg)


# ─────────────────────────────────────────────────────────────────────────────
# REVERT / UNINSTALL
# ─────────────────────────────────────────────────────────────────────────────

def revert_all() -> None:
    """
    Revert all customizations:
    - Reset GNOME interface settings to defaults
    - Disable all custom extensions
    - Optionally remove extension directories
    """
    header("Reverting All Customizations")

    # Reset GNOME interface
    step("Resetting GNOME interface settings...")
    reset_keys = [
        ("org.gnome.desktop.interface", "gtk-theme"),
        ("org.gnome.desktop.interface", "icon-theme"),
        ("org.gnome.desktop.interface", "cursor-theme"),
        ("org.gnome.desktop.interface", "font-name"),
        ("org.gnome.desktop.interface", "document-font-name"),
        ("org.gnome.desktop.interface", "monospace-font-name"),
        ("org.gnome.desktop.interface", "color-scheme"),
        ("org.gnome.desktop.interface", "accent-color"),
        ("org.gnome.desktop.interface", "font-antialiasing"),
        ("org.gnome.desktop.interface", "show-battery-percentage"),
        ("org.gnome.desktop.interface", "enable-hot-corners"),
        ("org.gnome.desktop.interface", "clock-show-weekday"),
        ("org.gnome.desktop.interface", "clock-show-seconds"),
        ("org.gnome.desktop.wm.preferences", "button-layout"),
        ("org.gnome.mutter", "workspaces-only-on-primary"),
    ]
    for schema, key in reset_keys:
        gsettings_reset(schema, key)
    ok("GNOME interface settings reset to defaults.")

    # Disable all custom extensions
    step("Disabling all custom extensions...")
    gsettings_set("org.gnome.shell", "enabled-extensions", "[]")
    gsettings_set("org.gnome.shell", "disabled-extensions", "[]")
    ok("All extensions disabled.")

    # Reset user-theme shell theme
    dconf_write("/org/gnome/shell/extensions/user-theme/name", "''")
    ok("Shell theme cleared.")

    # Ask about removing extension files
    answer = ask(
        "Do you also want to DELETE the extension files from disk?\n"
        "  (This cannot be undone easily.) [yes/no]:"
    )
    if answer in ("yes", "y"):
        removed = 0
        for uuid in EXTENSIONS:
            ext_path = EXT_DIR / uuid
            if ext_path.exists():
                shutil.rmtree(ext_path)
                ok(f"  Removed: {uuid}")
                removed += 1
        if removed == 0:
            warn("No extension directories found to remove.")
        else:
            ok(f"Removed {removed} extension(s).")
    else:
        warn("Extension files kept on disk.")

    ok("\nRevert complete. Please log out to apply changes.")


# ─────────────────────────────────────────────────────────────────────────────
# POST-INSTALL: LOG-OUT PROMPT
# ─────────────────────────────────────────────────────────────────────────────

def prompt_logout() -> None:
    """Ask if the user wants to log out of the GNOME session now."""
    print()
    cprint("  ╔══════════════════════════════════════════════════════╗", C.GREEN)
    cprint("  ║          Installation complete!                      ║", C.GREEN)
    cprint("  ║                                                      ║", C.GREEN)
    cprint("  ║  You need to log out of GNOME Shell for the changes  ║", C.GREEN)
    cprint("  ║  to take full effect.                                ║", C.GREEN)
    cprint("  ╚══════════════════════════════════════════════════════╝", C.GREEN)
    print()

    answer = ask("Do you want to log out now? [yes/no]:")
    if answer in ("yes", "y"):
        step("Logging out of GNOME session in 3 seconds...")
        time.sleep(3)
        # Try multiple logout methods in order of preference
        methods = [
            ["gnome-session-quit", "--logout", "--no-prompt"],
            ["loginctl", "terminate-session", os.environ.get("XDG_SESSION_ID", "auto")],
            ["pkill", "-SIGTERM", "-u", str(os.getuid()), "gnome-session"],
        ]
        for cmd in methods:
            result = run(cmd, check=False)
            if result.returncode == 0:
                ok("Logout command sent.")
                return
        warn("Could not log out automatically. Please log out manually.")
    else:
        ok("You can log out manually when ready.")


# ─────────────────────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────────────────────

def print_banner() -> None:
    lines = [
        "",
        "  ╔══════════════════════════════════════════════════════════════════╗",
        "  ║                                                                  ║",
        "  ║    ███╗   ███╗ █████╗  ██████╗ ██████╗ ███████╗                  ║",
        "  ║    ████╗ ████║██╔══██╗██╔════╝██╔═══██╗██╔════╝                  ║",
        "  ║    ██╔████╔██║███████║██║     ██║   ██║███████╗                  ║",
        "  ║    ██║╚██╔╝██║██╔══██║██║     ██║   ██║╚════██║                  ║",
        "  ║    ██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╔╝███████║                  ║",
        "  ║    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝                  ║",
        "  ║                                                                  ║",
        "  ║    ████████╗ █████╗ ██╗  ██╗ ██████╗ ███████╗                    ║",
        "  ║       ██╔══╝██╔══██╗██║  ██║██╔═══██╗██╔════╝                    ║",
        "  ║       ██║   ███████║███████║██║   ██║█████╗                      ║",
        "  ║       ██║   ██╔══██║██╔══██║██║   ██║██╔══╝                      ║",
        "  ║       ██║   ██║  ██║██║  ██║╚██████╔╝███████╗                    ║",
        "  ║       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝                    ║",
        "  ║                                                                  ║",
        "  ║         macOS 26 Tahoe Recreation — GNOME 50.5 Installer         ║",
        "  ║                                                                  ║",
        "  ╚══════════════════════════════════════════════════════════════════╝",
        "",
    ]
    for line in lines:
        cprint(line, C.CYAN)


def show_menu() -> str:
    print()
    cprint("  ┌─────────────────────────────────────────────────┐", C.CYAN)
    cprint("  │  What would you like to do?                     │", C.CYAN)
    cprint("  │                                                 │", C.CYAN)
    cprint("  │  1. Install extensions with DEFAULT settings    │", C.CYAN)
    cprint("  │  2. Install extensions with CUSTOM settings     │", C.CYAN)
    cprint("  │  3. Revert everything (uninstall & restore)     │", C.CYAN)
    cprint("  │  4. Check system & dependencies only            │", C.CYAN)
    cprint("  │  0. Exit                                        │", C.CYAN)
    cprint("  └─────────────────────────────────────────────────┘", C.CYAN)
    print()
    return ask("Enter your choice [0-4]:")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print_banner()

    # Basic environment checks
    if check_root():
        warn("Running as root is not recommended — dconf settings are per-user.")
        warn("Consider running as your regular user instead.\n")

    if not check_gnome_running():
        warn(
            "It doesn't look like you're inside a GNOME session "
            "(XDG_CURRENT_DESKTOP is not 'GNOME')."
        )
        warn("dconf/gsettings commands may still work if your session bus is reachable.\n")

    while True:
        choice = show_menu()

        if choice == "0":
            cprint("\n  Goodbye!\n", C.CYAN)
            sys.exit(0)

        elif choice == "4":
            check_gnome_version()
            check_dependencies()

        elif choice in ("1", "2"):
            # Step 1: dependencies
            check_dependencies()

            # Step 2: install extension files
            install_extensions(skip_download=False)

            # Step 3: apply settings
            if choice == "1":
                header("Applying Default Settings")
                apply_settings_from_file(SETTINGS_DEFAULT)
            else:
                header("Applying Your Custom Settings")
                apply_settings_from_file(SETTINGS_CUSTOM)

            # Step 4: log-out prompt
            prompt_logout()

        elif choice == "3":
            revert_all()
            prompt_logout()

        else:
            warn("Invalid choice. Please enter 0, 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
