#!/usr/bin/env python3
"""customize-project.py — Customization tool for cpp_example_project.

Lets you choose which library examples and which test framework to keep.

Modes
-----
configure (default)
    Writes CMakeUserPresets.json with a "custom-selection" preset that sets
    only the chosen cache variables.  Non-destructive; revert with:
        git checkout CMakeUserPresets.json
    Also prints the equivalent ``conan install`` command.

prune
    Removes unused source/test directories and strips the corresponding
    entries from cmake/Options.cmake, src/CMakeLists.txt,
    test/CMakeLists.txt, and conanfile.py.
    IRREVERSIBLE without version control — commit or stash first!

Usage
-----
    python scripts/customize-project.py # interactive
    python scripts/customize-project.py --list
    python scripts/customize-project.py --examples imgui sml --test-framework catch2
    python scripts/customize-project.py \\
        --examples imgui --test-framework gtest --mode prune --dry-run

Notes
-----
* The ARM cross-compilation block inside conanfile.py's requirements() is
  intentionally left untouched.  Review it manually if you target armv7.
* open62541 and open62541pp share a single Conan requires() block; the
  script adjusts it accordingly when only one of them is disabled.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

EXAMPLES = [
    {
        "key": "sml",
        "label": "SML (compile-time state machine)",
        "cmake_var": "CPP_STARTER_USE_SML",
        "src_dir": "sml",
        "conan_opt": "use_sml",
    },
    {
        "key": "boost_beast",
        "label": "Boost.Beast (HTTP/WebSocket server)",
        "cmake_var": "CPP_STARTER_USE_BOOST_BEAST",
        "src_dir": "boost.beast",
        "conan_opt": "use_boost_beast",
    },
    {
        "key": "crow",
        "label": "Crow (lightweight REST API)",
        "cmake_var": "CPP_STARTER_USE_CROW",
        "src_dir": "crow",
        "conan_opt": "use_crow",
    },
    {
        "key": "cppzmq_proto",
        "label": "Protobuf + cppzmq (pub/sub messaging)",
        "cmake_var": "CPP_STARTER_USE_CPPZMQ_PROTO",
        "src_dir": "protobuf.cppzmq",
        "conan_opt": "use_cppzmq_proto",
    },
    {
        "key": "qt",
        "label": "Qt 6 QML (declarative GUI)",
        "cmake_var": "CPP_STARTER_USE_QT",
        "src_dir": "qt",
        "conan_opt": "use_qt",
    },
    {
        "key": "open62541",
        "label": "open62541 (OPC UA server/client)",
        "cmake_var": "CPP_STARTER_USE_OPEN62541",
        "src_dir": "open62541",
        "conan_opt": "use_open62541",
    },
    {
        "key": "open62541pp",
        "label": "open62541pp (C++ OPC UA wrapper, via FetchContent)",
        "cmake_var": "CPP_STARTER_USE_OPEN62541PP",
        "src_dir": "open62541pp",
        "conan_opt": "use_open62541pp",
    },
    {
        "key": "slint",
        "label": "Slint (declarative UI, via FetchContent)",
        "cmake_var": "CPP_STARTER_USE_SLINT",
        "src_dir": "slint",
        "conan_opt": "use_slint",
    },
    {
        "key": "imgui",
        "label": "Dear ImGui (immediate-mode GUI)",
        "cmake_var": "CPP_STARTER_USE_IMGUI",
        "src_dir": "imgui",
        "conan_opt": "use_imgui",
    },
]

# open62541 / open62541pp share one conan requires() block and need special handling
_OPC_KEYS = {"open62541", "open62541pp"}

TEST_FRAMEWORKS = [
    {
        "key": "catch2",
        "label": "Catch2",
        "cmake_var": "CPP_STARTER_USE_CATCH2",
        "test_dir": "catch2",
        "conan_pkg": "catch2",
    },
    {
        "key": "gtest",
        "label": "GoogleTest",
        "cmake_var": "CPP_STARTER_USE_GTEST",
        "test_dir": "gtest",
        "conan_pkg": "gtest",
    },
]

# ---------------------------------------------------------------------------
# Interactive helpers
# ---------------------------------------------------------------------------


def _rule(char="-", width=60):
    return char * width


def prompt_multiselect(title, items):
    """Numbered multi-select; returns list of selected item dicts.
    Pressing Enter with no input selects all."""
    print(f"\n{title}")
    print(_rule())
    for i, item in enumerate(items, 1):
        print(f"  [{i:2}]  {item['label']}")
    print()
    while True:
        raw = input("  Numbers (space-separated), or Enter to select ALL: ").strip()
        if not raw:
            return list(items)
        parts = raw.split()
        try:
            indices = [int(p) - 1 for p in parts]
        except ValueError:
            print("  Please enter space-separated integers.\n")
            continue
        if any(i < 0 or i >= len(items) for i in indices):
            print(f"  Numbers must be between 1 and {len(items)}.\n")
            continue
        selected = [items[i] for i in indices]
        if not selected:
            print("  Select at least one item.\n")
            continue
        return selected


def prompt_choice(title, items):
    """Single-choice numbered list; returns the selected item dict."""
    print(f"\n{title}")
    print(_rule())
    for i, item in enumerate(items, 1):
        print(f"  [{i}]  {item['label']}")
    print()
    while True:
        raw = input("  Enter number: ").strip()
        try:
            idx = int(raw) - 1
        except ValueError:
            print("  Please enter a number.\n")
            continue
        if 0 <= idx < len(items):
            return items[idx]
        print(f"  Number must be between 1 and {len(items)}.\n")


# ---------------------------------------------------------------------------
# Configure mode: write CMakeUserPresets.json
# ---------------------------------------------------------------------------


def _collect_all_presets(json_path, visited=None):
    """Recursively follow ``include`` arrays and return every configurePreset entry."""
    if visited is None:
        visited = set()
    path = Path(json_path).resolve()
    if path in visited:
        return []
    visited.add(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    results = list(data.get("configurePresets", []))
    for inc in data.get("include", []):
        results.extend(_collect_all_presets(path.parent / inc, visited))
    return results


def _public_preset_names(repo_root):
    """Return the names of all non-hidden configurePresets."""
    all_presets = _collect_all_presets(repo_root / "CMakePresets.json")
    return [p["name"] for p in all_presets if not p.get("hidden", False)]


def run_configure(repo_root, enabled_examples, enabled_fw_keys, dry_run):
    enabled_keys = {e["key"] for e in enabled_examples}

    # Build cacheVariables block
    cache_vars = {}
    for ex in EXAMPLES:
        cache_vars[ex["cmake_var"]] = "ON" if ex["key"] in enabled_keys else "OFF"
    for fw in TEST_FRAMEWORKS:
        cache_vars[fw["cmake_var"]] = "ON" if fw["key"] in enabled_fw_keys else "OFF"

    preset = {
        "name": "custom-selection",
        "displayName": "Custom selection (customize-project.py)",
        "description": (
            "Enables only the chosen examples and test framework. "
            "Inherits compiler/build settings from conf-common. "
            "Override CMAKE_CXX_COMPILER etc. as needed."
        ),
        "inherits": "conf-common",
        "cacheVariables": cache_vars,
    }
    output = {"version": 6, "configurePresets": [preset]}

    out_path = repo_root / "CMakeUserPresets.json"
    if dry_run:
        print(f"\n[dry-run] Would write {out_path}:")
        print(json.dumps(output, indent=2))
    else:
        out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        print(f"  Written: CMakeUserPresets.json")
        print(f"  Use with:  cmake --preset custom-selection -DCMAKE_CXX_COMPILER=<your-compiler>")

    # Print equivalent conan install command
    print("\n  Equivalent conan install command:")
    print("    conan install . \\")
    for ex in EXAMPLES:
        val = "True" if ex["key"] in enabled_keys else "False"
        print(f"      -o {ex['conan_opt']}={val} \\")
    print("      --build=missing")

    # Print cmake -D flags alternative
    print("\n  Or pass cache variables directly to cmake:")
    flags = " ".join(
        f"-D{ex['cmake_var']}={'ON' if ex['key'] in enabled_keys else 'OFF'}"
        for ex in EXAMPLES
    )
    print(f"    cmake <build-dir> {flags}")


# ---------------------------------------------------------------------------
# Prune mode: regex helpers
# ---------------------------------------------------------------------------


def _remove_cmake_if_block(content, cmake_var):
    """Remove the if(CMAKE_VAR)...endif() block, plus an optional preceding comment."""
    # Matches: optional preceding blank line, optional "# Comment\n", then the if block.
    pattern = (
        r"\n?"
        r"(?:[ \t]*#[^\n]*\n)?"  # optional comment line
        r"if\(" + re.escape(cmake_var) + r"\)"
        r".*?"
        r"endif\(\)"
        r"[ \t]*\n?"
    )
    result = re.sub(pattern, "\n", content, flags=re.DOTALL)
    # Collapse runs of 3+ newlines that may result from removal
    return re.sub(r"\n{3,}", "\n\n", result)


def _remove_option_line(content, cmake_var):
    """Remove a single option(...) line for the given variable."""
    return re.sub(
        r"[ \t]*option\(" + re.escape(cmake_var) + r"[^\n]*\n",
        "",
        content,
    )


def _remove_conan_option_entry(content, conan_opt):
    """Remove  \"use_x\": [True, False], ...  from the options dict.
    The trailing [^\n]* handles optional inline comments on the same line."""
    return re.sub(
        r'[ \t]+"' + re.escape(conan_opt) + r'":\s*\[True,\s*False\],?[^\n]*\n',
        "",
        content,
    )


def _remove_conan_default_option(content, conan_opt):
    """Remove  \"use_x\": True/False,  from the default_options dict."""
    return re.sub(
        r'[ \t]+"' + re.escape(conan_opt) + r'":\s*(?:True|False),?\n',
        "",
        content,
    )


def _remove_conan_cache_var_line(content, cmake_var):
    """Remove  tc.cache_variables[\"CMAKE_VAR\"] = ...  line from generate()."""
    return re.sub(
        r'[ \t]+tc\.cache_variables\["' + re.escape(cmake_var) + r'"\][^\n]*\n',
        "",
        content,
    )


def _remove_conan_test_require(content, conan_pkg):
    """Remove  self.test_requires(\"<pkg>/...\")  line from build_requirements()."""
    return re.sub(
        r'[ \t]+self\.test_requires\("' + re.escape(conan_pkg) + r'[^"]*"\)\n',
        "",
        content,
    )


def _remove_conan_requirements_block(content, conan_opt):
    """Remove  if self.options.<opt>:\\n    self.requires(...)...  block (8-space indent)."""
    pattern = (
        r"\n?"
        r"        if self\.options\." + re.escape(conan_opt) + r":\n"
        r"(?:            self\.requires\([^\n]+\)\n)+"
    )
    result = re.sub(pattern, "\n", content)
    return re.sub(r"\n{3,}", "\n\n", result)


def _patch_qt_disabled(content):
    """
    Handle the Qt-specific blocks in conanfile.py when Qt is disabled.

    Three places need to be cleaned up:
    1. The ``# Qt-only build`` requirements block that ends with ``return``
       (not handled by the generic _remove_conan_requirements_block because
       of the extra ``return`` statement).
    2. The standalone ``if self.options.use_qt:`` block in generate() that
       only sets one cache variable.
    3. The outer guard ``if ... and not self.options.use_qt:`` in generate()
       which should be simplified to ``if self.settings.arch != \"armv7\":``.
    """
    # 1. Qt-only requirements block (comment + if + requires + return)
    content = re.sub(
        r"\n?[ \t]*#[^\n]*[Qq][Tt][^\n]*\n"
        r"[ \t]+if self\.options\.use_qt:\n"
        r"(?:[ \t]+self\.requires\([^\n]+\)\n)?"
        r"[ \t]+return\n",
        "\n",
        content,
    )
    # 2. Standalone generate() Qt block
    content = re.sub(
        r"\n?[ \t]+if self\.options\.use_qt:\n"
        r"[ \t]+tc\.cache_variables\[\"CPP_STARTER_USE_QT\"\][^\n]*\n",
        "\n",
        content,
    )
    # 3. Simplify the outer arch/qt guard
    content = content.replace(
        'if self.settings.arch != "armv7" and not self.options.use_qt:',
        'if self.settings.arch != "armv7":',
    )
    return re.sub(r"\n{3,}", "\n\n", content)


def _handle_opc_shared_block(content, keep_open62541, keep_open62541pp):
    """
    Handle the combined open62541 / open62541pp requires block:
        if self.options.use_open62541 or self.options.use_open62541pp:
            self.requires("open62541/...")
    """
    old_cond = "if self.options.use_open62541 or self.options.use_open62541pp:"
    if keep_open62541 and keep_open62541pp:
        return content  # nothing to do
    if not keep_open62541 and not keep_open62541pp:
        # Remove the entire block
        pattern = (
            r"\n?"
            r"        if self\.options\.use_open62541 or self\.options\.use_open62541pp:\n"
            r"(?:            self\.requires\([^\n]+\)\n)+"
        )
        result = re.sub(pattern, "\n", content)
        return re.sub(r"\n{3,}", "\n\n", result)
    # One remains: narrow the condition
    new_cond = (
        "if self.options.use_open62541:"
        if keep_open62541
        else "if self.options.use_open62541pp:"
    )
    return content.replace(old_cond, new_cond)


def _apply_to_file(path, modifier, dry_run, label):
    """Read file, apply modifier, write back; skip if unchanged."""
    original = path.read_text(encoding="utf-8")
    modified = modifier(original)
    if modified == original:
        print(f"  (unchanged) {label}")
        return
    if dry_run:
        print(f"  [dry-run] Would modify: {label}")
    else:
        path.write_text(modified, encoding="utf-8")
        print(f"  Modified:  {label}")


def _delete_dir(path, dry_run):
    if not path.exists():
        print(f"  (not found) {path.name}/")
        return
    if dry_run:
        print(f"  [dry-run] Would delete: {path}")
    else:
        shutil.rmtree(path)
        print(f"  Deleted:   {path}")


# ---------------------------------------------------------------------------
# Prune mode: orchestration
# ---------------------------------------------------------------------------


def run_prune(repo_root, enabled_examples, enabled_fw_keys, dry_run):
    enabled_keys = {e["key"] for e in enabled_examples}
    disabled_examples = [e for e in EXAMPLES if e["key"] not in enabled_keys]
    disabled_fws = [fw for fw in TEST_FRAMEWORKS if fw["key"] not in enabled_fw_keys]

    keep_open62541 = "open62541" in enabled_keys
    keep_open62541pp = "open62541pp" in enabled_keys

    # ------------------------------------------------------------------
    print("\n--- Removing source directories ---")
    for ex in disabled_examples:
        _delete_dir(repo_root / "src" / ex["src_dir"], dry_run)

    print("\n--- Removing test directories ---")
    for fw in disabled_fws:
        _delete_dir(repo_root / "test" / fw["test_dir"], dry_run)

    # ------------------------------------------------------------------
    print("\n--- Patching cmake/Options.cmake ---")

    def patch_options(content):
        for ex in disabled_examples:
            content = _remove_option_line(content, ex["cmake_var"])
        for fw in disabled_fws:
            content = _remove_option_line(content, fw["cmake_var"])
        return content

    _apply_to_file(repo_root / "cmake" / "Options.cmake", patch_options, dry_run, "cmake/Options.cmake")

    # ------------------------------------------------------------------
    print("\n--- Patching src/CMakeLists.txt ---")

    def patch_src_cmake(content):
        for ex in disabled_examples:
            content = _remove_cmake_if_block(content, ex["cmake_var"])
        return content

    _apply_to_file(repo_root / "src" / "CMakeLists.txt", patch_src_cmake, dry_run, "src/CMakeLists.txt")

    # ------------------------------------------------------------------
    print("\n--- Patching test/CMakeLists.txt ---")

    def patch_test_cmake(content):
        for fw in disabled_fws:
            content = _remove_cmake_if_block(content, fw["cmake_var"])
        return content

    _apply_to_file(repo_root / "test" / "CMakeLists.txt", patch_test_cmake, dry_run, "test/CMakeLists.txt")

    # ------------------------------------------------------------------
    print("\n--- Patching conanfile.py ---")

    def patch_conanfile(content):
        for ex in disabled_examples:
            content = _remove_conan_option_entry(content, ex["conan_opt"])
            content = _remove_conan_default_option(content, ex["conan_opt"])
            # qt: _patch_qt_disabled removes the whole if-block in generate();
            # removing the cache_var line first would leave an empty if-shell.
            if ex["key"] != "qt":
                content = _remove_conan_cache_var_line(content, ex["cmake_var"])
            # open62541/open62541pp and qt need special handling — skip generic removal
            if ex["key"] not in _OPC_KEYS and ex["key"] != "qt":
                content = _remove_conan_requirements_block(content, ex["conan_opt"])
        # Qt has a return statement in its requirements block — special handling
        if "qt" not in enabled_keys:
            content = _patch_qt_disabled(content)
        # Handle the shared OPC UA requires() block
        content = _handle_opc_shared_block(content, keep_open62541, keep_open62541pp)

        for fw in disabled_fws:
            content = _remove_conan_test_require(content, fw["conan_pkg"])

        return content

    _apply_to_file(repo_root / "conanfile.py", patch_conanfile, dry_run, "conanfile.py")

    print()
    print("  Note: The armv7 cross-compilation block inside conanfile.py's")
    print("  requirements() was NOT modified.  Review it manually if targeting ARM.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _example_keys():
    return [e["key"] for e in EXAMPLES]


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["configure", "prune"],
        default="configure",
        help=(
            "configure (default): write CMakeUserPresets.json; "
            "prune: delete files and edit CMakeLists / conanfile"
        ),
    )
    parser.add_argument(
        "--examples",
        nargs="+",
        metavar="KEY",
        help=(
            "Examples to KEEP (space-separated). "
            f"Valid keys: {', '.join(_example_keys())}"
        ),
    )
    parser.add_argument(
        "--test-framework",
        choices=["catch2", "gtest", "both"],
        dest="test_framework",
        metavar="FRAMEWORK",
        help="Test framework to keep: catch2, gtest, or both",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing any files",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available example keys and exit",
    )
    return parser.parse_args()


def _find_repo_root():
    """Walk up from the script location to find the project root."""
    candidate = Path(__file__).resolve().parent
    for _ in range(4):  # search at most 4 levels up
        if (candidate / "CMakeLists.txt").exists() and (candidate / "conanfile.py").exists():
            return candidate
        candidate = candidate.parent
    return None


def main():
    args = parse_args()

    if args.list:
        print("\nAvailable example keys:")
        for ex in EXAMPLES:
            print(f"  {ex['key']:<16}  {ex['label']}")
        print("\nTest framework keys: catch2, gtest, both")
        return

    repo_root = _find_repo_root()
    if repo_root is None:
        sys.exit(
            "ERROR: Could not locate project root (needs CMakeLists.txt + conanfile.py). "
            "Run this script from inside the repository."
        )

    # ------------------------------------------------------------------
    # Resolve example selection
    # ------------------------------------------------------------------
    if args.examples:
        valid = set(_example_keys())
        unknown = set(args.examples) - valid
        if unknown:
            sys.exit(
                f"ERROR: Unknown example key(s): {', '.join(sorted(unknown))}\n"
                f"Run with --list to see valid keys."
            )
        enabled_examples = [e for e in EXAMPLES if e["key"] in set(args.examples)]
    else:
        print("\ncpp_example_project — Project Customization")
        print("=" * 44)
        if args.mode == "prune":
            print(
                "\n[!] PRUNE mode: directories will be PERMANENTLY deleted and\n"
                "    CMakeLists.txt / conanfile.py will be modified.\n"
                "    Commit or stash your work before continuing.\n"
            )
        enabled_examples = prompt_multiselect("Select examples to KEEP:", EXAMPLES)

    # ------------------------------------------------------------------
    # Resolve test framework selection
    # ------------------------------------------------------------------
    if args.test_framework:
        fw_choice = args.test_framework
    else:
        fw_items = [
            *TEST_FRAMEWORKS,
            {"key": "both", "label": "Both frameworks (keep Catch2 and GoogleTest)"},
        ]
        fw_item = prompt_choice("Select test framework to keep:", fw_items)
        fw_choice = fw_item["key"]

    enabled_fw_keys = {"catch2", "gtest"} if fw_choice == "both" else {fw_choice}

    # ------------------------------------------------------------------
    # Print summary
    # ------------------------------------------------------------------
    print()
    print(_rule("="))
    print("Summary")
    print(_rule("="))
    print(f"  Mode        : {args.mode}")
    print(f"  Examples    : {', '.join(e['key'] for e in enabled_examples)}")
    print(f"  Test fw     : {', '.join(sorted(enabled_fw_keys))}")
    if args.dry_run:
        print("  Dry run     : YES — no files will be changed")
    print()

    if not enabled_examples:
        sys.exit("ERROR: At least one example must be selected.")

    # ------------------------------------------------------------------
    # Confirm before destructive prune
    # ------------------------------------------------------------------
    if args.mode == "prune" and not args.dry_run:
        confirm = input("Type 'yes' to proceed with destructive prune: ").strip().lower()
        if confirm != "yes":
            print("Aborted.")
            sys.exit(0)

    # ------------------------------------------------------------------
    # Execute
    # ------------------------------------------------------------------
    if args.mode == "configure":
        print("--- Writing CMakeUserPresets.json ---")
        run_configure(repo_root, enabled_examples, enabled_fw_keys, args.dry_run)
    else:
        run_prune(repo_root, enabled_examples, enabled_fw_keys, args.dry_run)

    print()
    print("Done.")


if __name__ == "__main__":
    main()
