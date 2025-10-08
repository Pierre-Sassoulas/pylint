# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Everything related to the 'pylint-config upgrade' command."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pylint.config import find_default_config_files
from pylint.config._breaking_changes import (
    CONFIGURATION_BREAKING_CHANGES,
    BreakingChange,
    Condition,
    Information,
    Intention,
    Solution,
)
from pylint.config.config_file_parser import _RawConfParser

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def handle_upgrade_command(linter: PyLinter) -> int:
    """Handle 'pylint-config upgrade'."""
    config_path = next(find_default_config_files(), None)
    if not config_path or not config_path.exists():
        print("Error: No configuration file found to upgrade. Exiting", file=sys.stderr)
        return 1

    print(f"Upgrading configuration file: {config_path}")

    # Parse the current configuration
    config_data, _ = _RawConfParser.parse_config_file(config_path, verbose=False)

    # Get the current pylint version
    from pylint import __version__

    current_version = __version__

    # Get upgraded-to version from config
    upgraded_to = config_data.get("upgraded-to", None)

    if upgraded_to == current_version:
        print(
            f"Configuration is already at version {current_version}. No upgrade needed."
        )
        return 0

    print(f"Current configuration version: {upgraded_to or 'unknown'}")
    print(f"Pylint version: {current_version}")

    # Find breaking changes between versions
    breaking_changes = get_breaking_changes_to_apply(
        linter, upgraded_to, current_version
    )

    if not breaking_changes:
        print("No breaking changes detected.")
        if linter.config.interactive:
            # Still update the upgraded-to field
            update_upgraded_to_field(config_path, current_version)
        return 0

    print(f"\nFound {len(breaking_changes)} breaking change(s) to address:")

    if linter.config.interactive:
        return handle_interactive_upgrade(
            linter, config_path, config_data, breaking_changes, current_version
        )
    else:
        return handle_automatic_upgrade(
            linter, config_path, config_data, breaking_changes, current_version
        )


def get_breaking_changes_to_apply(
    linter: PyLinter, from_version: str | None, to_version: str
) -> list[tuple[str, BreakingChange, Information, list[Condition], dict]]:
    """Get list of breaking changes that apply between versions."""
    changes_to_apply = []

    for version, changes in CONFIGURATION_BREAKING_CHANGES.items():
        # Skip if this version is before the from_version or after to_version
        if from_version and version <= from_version:
            continue
        if version > to_version:
            continue

        for change_type, info, conditions, solutions in changes:
            # Check if conditions are met
            if all(
                check_condition(linter, condition, info) for condition in conditions
            ):
                changes_to_apply.append(
                    (version, change_type, info, conditions, solutions)
                )

    return changes_to_apply


def check_condition(linter: PyLinter, condition: Condition, info: Information) -> bool:
    """Check if a condition is met."""
    if condition == Condition.MESSAGE_IS_ENABLED:
        return linter.is_message_enabled(info.msgid_or_symbol)
    elif condition == Condition.MESSAGE_IS_NOT_ENABLED:
        return not linter.is_message_enabled(info.msgid_or_symbol)
    elif condition == Condition.MESSAGE_IS_DISABLED:
        return info.msgid_or_symbol in linter.config.disable
    elif condition == Condition.MESSAGE_IS_NOT_DISABLED:
        return info.msgid_or_symbol not in linter.config.disable
    elif condition == Condition.EXTENSION_IS_LOADED:
        return info.extension in linter.config.load_plugins
    elif condition == Condition.EXTENSION_IS_NOT_LOADED:
        return info.extension not in linter.config.load_plugins
    elif condition == Condition.OPTION_IS_PRESENT:
        # Check if option is present in config
        if isinstance(info.option, list):
            return any(
                hasattr(linter.config, opt.replace("-", "_")) for opt in info.option
            )
        return hasattr(linter.config, info.option.replace("-", "_"))
    return False


def handle_interactive_upgrade(
    linter: PyLinter,
    config_path: Path,
    config_data: dict[str, str],
    breaking_changes: list,
    target_version: str,
) -> int:
    """Handle interactive upgrade with user prompts."""
    modifications = {}

    for version, change_type, info, conditions, solutions in breaking_changes:
        print(f"\n{'=' * 60}")
        print(f"Version {version}: {change_type.value.format(**_info_to_dict(info))}")
        print(f"{'=' * 60}")

        if info.description:
            print(f"\nDescription: {info.description}")

        # Present solutions
        if len(solutions) == 1:
            intention = list(solutions.keys())[0]
            print(f"\nRecommended action: {intention.value}")
            response = input("Apply this fix? (y/n, default=y): ").lower().strip()
            if response in ("", "y", "yes"):
                apply_solutions(modifications, solutions[intention], info)
        else:
            print("\nAvailable options:")
            intentions = list(solutions.keys())
            for i, intention in enumerate(intentions, 1):
                print(f"  {i}. {intention.value}")

            while True:
                response = input(
                    f"Choose option (1-{len(intentions)}, default=1): "
                ).strip()
                if not response:
                    response = "1"
                try:
                    choice = int(response)
                    if 1 <= choice <= len(intentions):
                        apply_solutions(
                            modifications, solutions[intentions[choice - 1]], info
                        )
                        break
                except ValueError:
                    pass
                print("Invalid choice. Please try again.")

    # Apply modifications to config file
    if modifications or breaking_changes:
        write_upgraded_config(config_path, config_data, modifications, target_version)
        print(f"\n✓ Configuration upgraded successfully to version {target_version}")
        return 0

    return 0


def handle_automatic_upgrade(
    linter: PyLinter,
    config_path: Path,
    config_data: dict[str, str],
    breaking_changes: list,
    target_version: str,
) -> int:
    """Handle automatic upgrade without user interaction."""
    modifications = {}
    warnings = []

    for version, change_type, info, conditions, solutions in breaking_changes:
        print(f"\nVersion {version}: {change_type.value.format(**_info_to_dict(info))}")

        # Apply automatic fixes where possible
        if Intention.FIX_CONF in solutions:
            apply_solutions(modifications, solutions[Intention.FIX_CONF], info)
            print("  → Automatically fixed")
        elif Intention.USE_DEFAULT in solutions:
            apply_solutions(modifications, solutions[Intention.USE_DEFAULT], info)
            print("  → Using default behavior")
        else:
            # Cannot auto-fix, add to warnings
            warnings.append((change_type, info))
            print("  ⚠ Requires manual intervention")

    # Apply modifications
    if modifications or breaking_changes:
        write_upgraded_config(config_path, config_data, modifications, target_version)
        print(
            f"\n✓ Automatic fixes applied. Configuration upgraded to version {target_version}"
        )

    if warnings:
        print("\n⚠ The following changes require manual review:")
        for change_type, info in warnings:
            print(f"  - {change_type.value.format(**_info_to_dict(info))}")
        print("\nRun 'pylint-config upgrade --interactive' for guided fixes.")
        return 1

    return 0


def apply_solutions(
    modifications: dict, solution_list: list[Solution], info: Information
) -> None:
    """Apply a list of solutions to the modifications dict."""
    for solution in solution_list:
        if solution == Solution.ADD_EXTENSION:
            modifications.setdefault("load-plugins", {"add": [], "remove": []})
            modifications["load-plugins"]["add"].append(info.extension)
        elif solution == Solution.REMOVE_EXTENSION:
            modifications.setdefault("load-plugins", {"add": [], "remove": []})
            modifications["load-plugins"]["remove"].append(info.extension)
        elif solution == Solution.ENABLE_MESSAGE_EXPLICITLY:
            modifications.setdefault("enable", {"add": [], "remove": []})
            modifications["enable"]["add"].append(info.msgid_or_symbol)
        elif solution == Solution.ENABLE_MESSAGE_IMPLICITLY:
            modifications.setdefault("disable", {"add": [], "remove": []})
            modifications["disable"]["remove"].append(info.msgid_or_symbol)
        elif solution == Solution.DISABLE_MESSAGE_EXPLICITLY:
            modifications.setdefault("disable", {"add": [], "remove": []})
            modifications["disable"]["add"].append(info.msgid_or_symbol)
        elif solution == Solution.DISABLE_MESSAGE_IMPLICITLY:
            modifications.setdefault("enable", {"add": [], "remove": []})
            modifications["enable"]["remove"].append(info.msgid_or_symbol)
        elif solution == Solution.REMOVE_OPTION:
            if isinstance(info.option, list):
                for opt in info.option:
                    modifications.setdefault("remove", [])
                    modifications["remove"].append(opt)
            else:
                modifications.setdefault("remove", [])
                modifications["remove"].append(info.option)
        elif solution == Solution.REVIEW_OPTION:
            # Mark for review but don't auto-modify
            modifications.setdefault("review", [])
            if isinstance(info.option, list):
                modifications["review"].extend(info.option)
            else:
                modifications["review"].append(info.option)


def write_upgraded_config(
    config_path: Path,
    config_data: dict[str, str],
    modifications: dict,
    target_version: str,
) -> None:
    """Write the upgraded configuration back to file."""
    # Read the original file content
    with open(config_path, encoding="utf-8") as f:
        content = f.read()

    # Apply modifications based on file type
    if config_path.suffix == ".toml":
        content = apply_toml_modifications(content, modifications, target_version)
    else:
        content = apply_ini_modifications(content, modifications, target_version)

    # Write back
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)


def apply_toml_modifications(content: str, modifications: dict, version: str) -> str:
    """Apply modifications to TOML content."""
    import tomlkit

    doc = tomlkit.parse(content)

    # Ensure tool.pylint section exists
    if "tool" not in doc:
        doc["tool"] = {}
    if "pylint" not in doc["tool"]:
        doc["tool"]["pylint"] = {}

    # Add upgraded-to field
    doc["tool"]["pylint"]["upgraded-to"] = version

    # Apply modifications
    for key, changes in modifications.items():
        if key == "remove":
            # Remove options
            for section in doc.get("tool", {}).get("pylint", {}).values():
                if isinstance(section, dict):
                    for opt in changes:
                        section.pop(opt, None)
        elif key in ("enable", "disable", "load-plugins"):
            # Modify list-based options
            _modify_toml_list_option(doc, key, changes)

    return tomlkit.dumps(doc)


def apply_ini_modifications(content: str, modifications: dict, version: str) -> str:
    """Apply modifications to INI content."""
    import configparser

    parser = configparser.ConfigParser()
    parser.read_string(content)

    # Ensure MAIN section exists
    if not parser.has_section("MAIN"):
        parser.add_section("MAIN")

    # Add upgraded-to field
    parser.set("MAIN", "upgraded-to", version)

    # Apply modifications
    for key, changes in modifications.items():
        if key == "remove":
            for section in parser.sections():
                for opt in changes:
                    parser.remove_option(section, opt)
        elif key in ("enable", "disable", "load-plugins"):
            _modify_ini_list_option(parser, key, changes)

    # Write to string
    from io import StringIO

    output = StringIO()
    parser.write(output)
    return output.getvalue()


def _modify_toml_list_option(doc: dict, option: str, changes: dict) -> None:
    """Modify a list-based option in TOML."""
    section = doc.get("tool", {}).get("pylint", {}).get("messages control", {})
    if option not in section:
        section[option] = []

    current = section[option]
    if isinstance(current, str):
        current = [x.strip() for x in current.split(",")]

    for item in changes.get("add", []):
        if item not in current:
            current.append(item)

    for item in changes.get("remove", []):
        if item in current:
            current.remove(item)

    section[option] = current


def _modify_ini_list_option(parser, option: str, changes: dict) -> None:
    """Modify a list-based option in INI."""
    section = "messages control"
    if not parser.has_section(section):
        parser.add_section(section)

    current = parser.get(section, option, fallback="")
    items = [x.strip() for x in current.split(",") if x.strip()]

    for item in changes.get("add", []):
        if item not in items:
            items.append(item)

    for item in changes.get("remove", []):
        if item in items:
            items.remove(item)

    parser.set(section, option, ",".join(items))


def update_upgraded_to_field(config_path: Path, version: str) -> None:
    """Update only the upgraded-to field."""
    with open(config_path, encoding="utf-8") as f:
        content = f.read()

    if config_path.suffix == ".toml":
        import tomlkit

        doc = tomlkit.parse(content)
        if "tool" not in doc:
            doc["tool"] = {}
        if "pylint" not in doc["tool"]:
            doc["tool"]["pylint"] = {}
        doc["tool"]["pylint"]["upgraded-to"] = version
        content = tomlkit.dumps(doc)
    else:
        import configparser

        parser = configparser.ConfigParser()
        parser.read_string(content)
        if not parser.has_section("MAIN"):
            parser.add_section("MAIN")
        parser.set("MAIN", "upgraded-to", version)
        from io import StringIO

        output = StringIO()
        parser.write(output)
        content = output.getvalue()

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)


def _info_to_dict(info: Information) -> dict:
    """Convert Information to dict for string formatting."""
    return {
        "symbol": info.msgid_or_symbol,
        "msgid": info.msgid_or_symbol,
        "extension": info.extension,
        "option": (
            info.option
            if isinstance(info.option, str)
            else ", ".join(info.option or [])
        ),
        "description": info.description or "",
    }


def check_upgrade_needed(linter: PyLinter) -> list[str]:
    """Check if configuration upgrade is needed."""
    from pylint import __version__

    upgraded_to = getattr(linter.config, "upgraded_to", None)

    if upgraded_to is None:
        return [
            "Configuration file does not have 'upgraded-to' field. "
            "Run 'pylint-config upgrade' to update your configuration."
        ]

    if upgraded_to != __version__:
        breaking_changes = get_breaking_changes_to_apply(
            linter, upgraded_to, __version__
        )
        if breaking_changes:
            return [
                f"Configuration is at version {upgraded_to} but pylint is {__version__}. "
                f"Found {len(breaking_changes)} breaking change(s). "
                "Run 'pylint-config upgrade' to update your configuration."
            ]

    return []


def emit_upgrade_warnings(linter: PyLinter) -> None:
    """Emit warnings if upgrade is needed."""
    warnings = check_upgrade_needed(linter)
    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
