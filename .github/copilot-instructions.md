# WTF Modpack Launcher - AI Coding Agent Instructions

## Project Overview
This is a **Python-based Minecraft launcher** specifically designed for the WTF Modpack (Minecraft 1.20.1 + Forge 47.3.33). The launcher handles automated installation, updates, and launching of a curated modpack while providing offline gameplay capabilities.

## Architecture & Core Components

### Main Application (`main.py`)
- **GUI Framework**: `tkinter` + `ttkbootstrap` for modern dark theme UI
- **Single-file architecture**: ~1400 lines containing the entire launcher logic
- **Class-based design**: `WTFModpackLauncher` class manages all functionality
- **Key patterns**:
  - JSON-based configuration in `settings.json`
  - Thread-based operations for downloads/installations
  - Resource path handling for PyInstaller compilation
  - Process monitoring for Minecraft instances

### Auto-Updater System (`updater.py`)
- **Self-updating launcher** that checks GitHub releases API
- **Cross-platform support** (Windows/Linux) with OS-specific update scripts
- **Safe update patterns**:
  - Creates backup before replacement
  - Generates batch/shell scripts for post-exit updates
  - Handles PyInstaller executable detection
  - Graceful launcher restart after updates

### Build System
- **PyInstaller compilation** via `main.spec` configuration
- **Single executable output**: `WTF_Modpack_Launcher.exe`
- **Resource embedding**: Fonts, icons, and data files included
- **Automated builds**: GitHub Actions workflow for releases

## Critical Dependencies & Integration Points

### External Services
- **GitHub API**: Modpack downloads from `jamnaga/wtf-modpack` repository
- **Minecraft Launcher Lib**: Core Minecraft/Forge installation logic
- **Direct JAR downloads**: Mod files via zip extraction

### System Integration
- **Java Detection**: Automatic JDK discovery and validation
- **Memory Management**: RAM allocation with 4GB minimum requirement
- **Process Control**: Minecraft launch and monitoring
- **File System**: `.minecraft` directory management and mod installation

## Key Development Patterns

### Configuration Management
```python
# Settings are stored in settings.json with this structure:
{
    "User-info": [{"username": null, "UUID": null, "AUTH_TYPE": "offline"}],
    "allocated_ram": "4G",
    "wtf_modpack_version": null,
    "wtf_modpack_installed": false,
    "auto_update_launcher": true
}
```

### Threading Pattern for Long Operations
```python
def operation_with_gui_updates():
    def background_thread():
        # Heavy operation here
        self.window.after(0, lambda: self.update_gui_status("Status", "Detail"))
    
    Thread(target=background_thread, daemon=True).start()
```

### Error Handling Philosophy
- **Progressive fallbacks**: Try automatic methods first, then manual
- **User-friendly messages**: Italian language with emoji indicators
- **Graceful degradation**: Continue operation when possible
- **Debug output**: Comprehensive console logging for troubleshooting

### Resource Path Management
```python
def resource_path(relative_path):
    """Handle both development and PyInstaller execution"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
```

## Development Workflows

### Building Executable
1. Run `compile.bat` (Windows) to trigger PyInstaller
2. Output: `dist/WTF_Modpack_Launcher.exe`
3. GitHub Actions automates this for releases

### Testing Update Process
- Use `test_update.py` for update system validation
- Test both fresh installs and existing executable updates
- Verify executable detection across different deployment scenarios

### Version Management
- Version stored in `launcher_version.txt`
- Auto-updater compares with GitHub release tags
- Update process preserves user settings and configurations

## Common Pitfalls & Solutions

### GUI Thread Safety
- **Always use** `self.window.after(0, callback)` for GUI updates from threads
- Never call GUI methods directly from background threads

### PyInstaller Resource Access
- Use `resource_path()` for all asset loading
- Include all dependencies in `main.spec` hidden imports
- Test both development and compiled modes

### Update System Complexity
- The updater handles multiple scenarios: compiled exe, Python script, missing executable
- Update scripts must handle file locks and process termination
- Always create backups before replacement operations

### Memory and Performance
- Minimum 4GB RAM allocation for modpack functionality
- Download progress callbacks must be exception-safe
- Process monitoring prevents zombie Minecraft instances

## File Modification Guidelines

### Adding New Features
- Follow the existing JSON configuration pattern for settings
- Use the established threading pattern for long operations
- Add appropriate error handling with Italian user messages

### Modifying Update Logic
- Test extensively with both development and compiled versions
- Ensure backward compatibility with existing `settings.json`
- Verify cross-platform compatibility for update scripts

### UI Changes
- Maintain the dark theme consistency (`#1c1c1c` background, `#15d38f` accent)
- Use emoji prefixes for user-facing messages
- Follow the existing layout patterns with status cards and progress indicators

This launcher represents a self-contained Minecraft modpack distribution system with sophisticated auto-update capabilities and user-friendly offline gameplay support.