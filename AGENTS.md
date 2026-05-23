# AGENTS.md — Project Overview for AI Coding Agents

This file describes the structure, conventions, and key components of `cpp_example_project` to help AI coding agents navigate and contribute effectively.

---

## Project Purpose

A batteries-included, modern C++ starter template maintained by the Zühlke Germany Modern C++ Topic Group. It provides a fully configured CMake + Conan 2 project with static analysis, sanitizers, formatting, testing, documentation, and a collection of library integration examples.

---

## Repository Layout

```
.
├── CMakeLists.txt          # Root CMake — wires all modules and subdirectories
├── CMakePresets.json       # Entry point for CMake presets (includes cmake/presets/*.json)
├── conanfile.py            # Conan 2 package descriptor; exposes per-example options
├── ConanPresets.json       # Conan-generated CMake preset integration
│
├── cmake/                  # Reusable CMake modules (included from root CMakeLists.txt)
│   ├── Options.cmake       # All CMake options (sanitizers, tools, examples, …)
│   ├── CompilerWarnings.cmake
│   ├── Sanitizers.cmake
│   ├── StaticAnalyzers.cmake
│   ├── Cache.cmake         # ccache / sccache support
│   ├── Doxygen.cmake
│   ├── CodeFormat.cmake    # clang-format / cmake-format targets
│   ├── Conan.cmake         # conan_provider.cmake integration
│   ├── PrecompiledHeader.cmake
│   ├── InterproceduralOptimization.cmake
│   ├── GitInformation.cmake
│   ├── ProjectSettings.cmake
│   ├── StandardProjectSettings.cmake
│   ├── BuildingConfig.cmake
│   ├── PreventInSourceBuilds.cmake
│   ├── Utilities.cmake
│   ├── VCEnvironment.cmake
│   ├── presets/            # CMake configure/build/test presets split by platform
│   │   ├── base.json
│   │   ├── linux-gcc.json
│   │   ├── linux-clang.json
│   │   ├── windows.json
│   │   └── special.json
│   └── arm-cortex-gnu/     # Cross-compilation toolchain for ARM Cortex-M
│       ├── ArmCortexGnuToolchain.cmake
│       └── ArmCortexM4Gnu.cmake
│
├── src/                    # Application source code
│   ├── CMakeLists.txt      # Conditionally adds each sub-project
│   ├── main.cpp            # Minimal standalone entry point
│   ├── sml/                # Boost.SML compile-time state machine example
│   ├── boost.beast/        # HTTP/WebSocket server (Boost.Beast)
│   ├── crow/               # Lightweight REST API (Crow)
│   ├── open62541/          # OPC UA server & client (open62541)
│   ├── open62541pp/        # C++ OPC UA wrapper (open62541pp, FetchContent)
│   ├── protobuf.cppzmq/    # Pub/sub messaging (Protobuf + cppzmq)
│   ├── imgui/              # Cross-platform GUI (Dear ImGui, GLFW + OpenGL3)
│   ├── slint/              # Declarative UI (Slint, FetchContent)
│   ├── qt/                 # Qt 6 QML timer app with C++ backend
│   └── embedded/           # Bare-metal ARM Cortex-M4 cross-compilation example
│
├── test/                   # Unit and constexpr tests
│   ├── CMakeLists.txt
│   ├── catch2/             # Catch2 test suite
│   └── gtest/              # GoogleTest test suite
│
├── fuzz_test/              # libFuzzer harness (enabled with ENABLE_FUZZING=ON)
│   ├── CMakeLists.txt
│   └── fuzz_tester.cpp
│
├── templates/
│   └── version.hpp.in      # Version header template; configured into build dir
│
├── docker/                 # Docker / Dev Container support
│   ├── Dockerfile
│   ├── docker-compose-dev.yml
│   ├── docker-compose-ci.yml
│   ├── build-dev-image.sh
│   ├── build-ci-image.sh
│   └── ccache.conf
│
└── scripts/                # Helper Python scripts for tooling
    ├── run-clang-format.py
    ├── run-clang-tidy.py
    └── run-clang-tidy-diff.py
```

---

## Build System

- **CMake ≥ 3.25** with CMakePresets v6.
- **Conan 2** is used as the package manager via `conan_provider.cmake`; it is invoked automatically during CMake configure.
- The `CMakePresets.json` at the root includes platform-specific preset files from `cmake/presets/`.

### Common configure commands

```bash
# Linux, GCC, Debug
cmake --preset linux-gcc-debug

# Linux, Clang, Release
cmake --preset linux-clang-release

# Windows, MSVC, Debug
cmake --preset windows-msvc-debug
```

---

## Key CMake Options

Defined in `cmake/Options.cmake` and controllable via `-D` flags or preset `cacheVariables`:

| Option | Default | Purpose |
|---|---|---|
| `ENABLE_TESTING` | `ON` | Build Catch2 / GTest suites |
| `ENABLE_FUZZING` | `OFF` | Build libFuzzer harness |
| `ENABLE_CLANG_TIDY` | `OFF` | Run clang-tidy during build |
| `ENABLE_CPPCHECK` | `OFF` | Run cppcheck during build |
| `ENABLE_SANITIZER_ADDRESS` | `OFF` | Enable ASan |
| `ENABLE_SANITIZER_UNDEFINED_BEHAVIOR` | `OFF` | Enable UBSan |
| `ENABLE_SANITIZER_THREAD` | `OFF` | Enable TSan (mutex with ASan/LSan) |
| `ENABLE_SANITIZER_MEMORY` | `OFF` | Enable MSan (Clang only) |
| `WARNINGS_AS_ERRORS` | `ON` | Treat warnings as errors |
| `ENABLE_PCH` | `OFF` | Enable precompiled headers |
| `ENABLE_CACHE` | `ON` | Use ccache/sccache |
| `ENABLE_DOXYGEN` | `OFF` | Generate Doxygen docs |
| `ENABLE_IPO` | `OFF` | Link-time optimisation |
| `CPP_STARTER_USE_SML` | `OFF` | Build SML example |
| `CPP_STARTER_USE_BOOST_BEAST` | `OFF` | Build Boost.Beast example |
| `CPP_STARTER_USE_CROW` | `OFF` | Build Crow example |
| `CPP_STARTER_USE_OPEN62541` | `OFF` | Build open62541 example |
| `CPP_STARTER_USE_OPEN62541PP` | `OFF` | Build open62541pp example |
| `CPP_STARTER_USE_SLINT` | `OFF` | Build Slint example |
| `CPP_STARTER_USE_IMGUI` | `OFF` | Build Dear ImGui example |
| `CPP_STARTER_USE_QT` | `OFF` | Build Qt 6 example |
| `CPP_STARTER_USE_EMBEDDED_TOOLCHAIN` | `OFF` | Cross-compile ARM Cortex-M4 example |

---

## Interface Libraries

Two CMake `INTERFACE` libraries act as configuration carriers — link them to any target:

- **`project_options`** — C++ standard, sanitizer flags, compile features.
- **`project_warnings`** — Compiler warning flags (see `cmake/CompilerWarnings.cmake`).

---

## Testing

Tests live under `test/` and are built when `ENABLE_TESTING=ON` (default). CTest is used as the test runner.

```bash
cmake --build --preset linux-gcc-debug
ctest --preset linux-gcc-debug
```

- `test/catch2/` — Catch2 tests (includes constexpr test examples).
- `test/gtest/` — GoogleTest tests (includes constexpr test examples).

---

## Fuzz Testing

Enabled with `-DENABLE_FUZZING=ON`. Requires a Clang build with `-fsanitize=fuzzer`. The harness is in `fuzz_test/fuzz_tester.cpp`.

---

## Dev Container / Docker

The recommended development environment is the Docker-based dev container:

```bash
docker compose -f docker/docker-compose-dev.yml up -d
```

Or open the folder in VS Code and choose **Reopen in Container**.

The container ships with all required compilers (GCC, Clang), CMake, Conan, clang-tidy, cppcheck, and ccache pre-installed.

---

## Code Style

- C++ formatted with **clang-format** (run `cmake --build <build_dir> --target clang-format-fix`).
- CMake formatted with **cmake-format**.
- Static analysis targets: `clang-tidy-check`, `clang-tidy-diff-check`, `cppcheck`.
- GNU extensions are disabled (`CMAKE_CXX_EXTENSIONS OFF`).

---

## Generated Files

`templates/version.hpp.in` is configured by CMake into `<build_dir>/generated/include/version.hpp`, which embeds the project version and current Git hash.

---

## Adding a New Example Sub-project

1. Create `src/<name>/CMakeLists.txt` with your target definition.
2. Add an option `CPP_STARTER_USE_<NAME>` in `cmake/Options.cmake`.
3. Wire it in `src/CMakeLists.txt` with a matching `if(CPP_STARTER_USE_<NAME>)` block.
4. Add a corresponding Conan option in `conanfile.py` if external dependencies are needed.
5. Document the example in `README.md`.
6. Register the example in `scripts/customize-project.py` by adding a new entry to the `EXAMPLES` list with the matching `key`, `label`, `cmake_var`, `src_dir`, and `conan_opt` fields.

> **Maintenance note:** Whenever the example sub-project structure changes — new examples added, existing ones renamed/removed, test frameworks added, or the layout of `cmake/Options.cmake`, `src/CMakeLists.txt`, or `conanfile.py` changes — `scripts/customize-project.py` must be updated accordingly so that the prune and configure modes stay in sync with the project.
