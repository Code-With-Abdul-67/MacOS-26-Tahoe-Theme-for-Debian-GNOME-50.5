# GNOME macOS Tahoe Recreation Script – Full System Analysis & Automation

## System Context
I am currently using:
- **OS**: Debian Testing
- **Desktop Environment**: GNOME 50.5
- **Customization Goal**: Make GNOME look and behave as close as possible to **macOS 26 Tahoe**

I have already installed and carefully configured a large number of GNOME Shell extensions and system settings to achieve this look. I want you to fully analyze my current setup.

---

## What You Must Do

### 1. Full System Analysis
- Inspect all currently installed GNOME Shell extensions
- Read and document every setting I have changed inside those extensions
- Check related GNOME settings (via `dconf`, `gsettings`, extension schemas, etc.)
- Identify any dependencies, themes, icons, cursors, or other packages that are part of this customization

### 2. Create Documentation
Produce a complete **Markdown documentation file** that includes:
- List of all extensions used
- Explanation of what each extension does in this setup
- Summary of the key custom settings I applied
- Any important notes or known issues

### 3. Create Configuration Files
Generate two separate configuration files:

1. **Default Settings File**  
   Contains the list of extensions + their original/default settings (preferably in JSON format).

2. **Custom Settings File**  
   Contains the exact same extensions but with **all of my personal settings** applied (also preferably JSON).

You may choose a different format only if it is clearly better for this use case (explain why).

### 4. Create a Python Script
Write a robust, user-friendly Python script that presents a simple interactive menu with the following options:

1. **Install all extensions with default settings**
2. **Install all extensions with my custom settings**
3. **Revert everything** (uninstall the extensions and restore original GNOME settings as much as possible)

#### Script Requirements:
- Automatically detect the system and check for missing dependencies
- Install any required system packages or Python libraries automatically
- Work on the latest Debian with GNOME 50 or newer
- Be well-commented and easy to understand
- Handle errors gracefully
- After successful installation, ask the user:
> “Installation complete. You need to log out of GNOME Shell for the changes to take full effect. Do you want to log out now? (yes/no)”
- If the user answers **yes**, automatically log them out of the current GNOME session
- After the user logs back in, everything (extensions + settings) should work correctly without errors

---

## Expected Deliverables
1. One comprehensive Markdown documentation file
2. Two configuration files (default + custom)
3. One high-quality Python script that performs all the above tasks

Please start by analyzing my current system and extensions thoroughly, then build the complete solution based on what you find.