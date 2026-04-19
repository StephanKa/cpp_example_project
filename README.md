# cpp_example_project

[![CMake](https://github.com/Zuehlke/cpp_example_project/workflows/CMake/badge.svg)](https://github.com/Zuehlke/cpp_example_project/actions)

Ongoing project of the Zühlke Germany **Modern C++ Topic Group**.

This project provides a batteries-included starting point for modern C++ projects — both desktop and embedded — with a strong focus on tooling, static analysis, and best practices.

Inspired by and adapted from:
- [Jason Turner's cpp_starter_project](https://github.com/lefticus/cpp_starter_project)
- [cmake_conan_boilerplate_template](https://github.com/cpp-best-practices/cmake_conan_boilerplate_template)
- [cmake_template](https://github.com/cpp-best-practices/cmake_template)

---

## Features

| Area | Details |
|---|---|
| **Build system** | CMake ≥ 3.25 with [CMakePresets v6](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html) |
| **Package manager** | [Conan 2](https://docs.conan.io/2/) with `conan_provider.cmake` |
| **Compilers** | GCC 10–15, Clang 12–21, MSVC 2019/2022 |
| **C++ standard** | C++17/20/23/26 (configurable) |
| **Static analysis** | clang-tidy, cppcheck, include-what-you-use |
| **Sanitizers** | ASan, LSan, UBSan, TSan, MSan (mutually exclusive where required) |
| **Formatting** | clang-format, cmake-format |
| **Testing** | Catch2, GoogleTest, libFuzzer |
| **Documentation** | Doxygen + Graphviz |
| **Caching** | ccache / sccache |
| **CI** | GitHub Actions (multi-compiler matrix) |
| **Dev container** | VS Code devcontainer + Docker Compose |

### Example sub-projects

| Example | Library | Description |
|---|---|---|
| `src/sml` | [Boost.SML](https://boost-ext.github.io/sml/) | Compile-time state machine |
| `src/boost.beast` | [Boost.Beast](https://www.boost.org/doc/libs/release/libs/beast/) | HTTP/WebSocket server |
| `src/crow` | [Crow](https://crowcpp.org/) | Lightweight REST API |
| `src/open62541` | [open62541](https://www.open62541.org/) | OPC UA server & client |
| `src/open62541pp` | [open62541pp](https://github.com/open62541pp/open62541pp) | C++ OPC UA wrapper |
| `src/protobuf.cppzmq` | Protobuf + cppzmq | Pub/sub messaging |
| `src/imgui` | [Dear ImGui](https://github.com/ocornut/imgui) (GLFW + OpenGL3) | Cross-platform GUI |
| `src/slint` | [Slint](https://slint.dev/) | Declarative UI (FetchContent) |
| `src/qt` | Qt 6 QML | QML timer app with C++ backend |
| `src/embedded` | ARM Cortex-M4 | Bare-metal cross-compilation |
| `test/catch2` | Catch2 | Unit + constexpr tests |
| `test/gtest` | GoogleTest | Unit + constexpr tests |
| `fuzz_test` | libFuzzer | Fuzz testing harness |

## Getting Started

### Use as a GitHub template

Click the green **Use this template** button near the top of this page, fill in a repository name, and clone:

```bash
git clone https://github.com/<user>/<your_new_repo>.git
```

### Dev Container (recommended)

The fastest way to get a fully configured environment is via the VS Code Dev Container or Docker Compose:

```bash
# Dev environment with all compilers, tools, and Conan pre-installed
docker compose -f docker/docker-compose-dev.yml up -d
```

Or open the folder in VS Code and click **Reopen in Container** when prompted.

---

## Prerequisites

### Required

| Tool | Minimum version | Install |
|---|---|---|
| CMake | 3.25 | `apt install cmake` · `choco install cmake` · `brew install cmake` |
| Conan | 2.x | `pip install conan` · `choco install conan` · `brew install conan` |
| GCC **or** Clang | gcc 10+ / clang 12+ | see below |

<details>
<summary>GCC install</summary>

```bash
# Debian/Ubuntu
sudo apt install build-essential          # GCC system version
sudo apt install gcc-14 g++-14            # specific version

# macOS
brew install gcc

# Windows
choco install mingw -y
```
</details>

<details>
<summary>Clang install</summary>

```bash
# Debian/Ubuntu (installs any version via LLVM script)
bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"

# macOS
brew install llvm

# Windows (bundled with Visual Studio, or standalone)
choco install llvm -y
```
</details>

<details>
<summary>Visual Studio 2019/2022</summary>

```powershell
choco install -y visualstudio2022community --package-parameters `
  "add Microsoft.VisualStudio.Workload.NativeDesktop --includeRecommended --passive"

# Add MSVC + Clang + vcvarsall to PATH
choco install vswhere -y; refreshenv
$clpath       = vswhere -products * -latest -find **/Hostx64/x64/*
$clangpath    = vswhere -products * -latest -find **/Llvm/bin/*
$vcvarsall    = vswhere -products * -latest -find **/Auxiliary/Build/*
$path = [Environment]::GetEnvironmentVariable("PATH","User")
[Environment]::SetEnvironmentVariable("Path","$path;$clpath;$clangpath;$vcvarsall","User")
refreshenv
```
</details>

### Optional tools

| Tool | Purpose | Install |
|---|---|---|
| [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) | Static analysis | bundled with LLVM |
| [cppcheck](http://cppcheck.sourceforge.net/) | Static analysis | `apt install cppcheck` |
| [include-what-you-use](https://include-what-you-use.org/) | Header analysis | [build from source](https://github.com/include-what-you-use/include-what-you-use#how-to-install) |
| [ccache](https://ccache.dev/) | Compiler cache | `apt install ccache` |
| [Doxygen](https://www.doxygen.nl/) + Graphviz | API docs | `apt install doxygen graphviz` |

---

## Build Instructions

Presets are split across `cmake/presets/` and follow a consistent naming scheme:

| Stage | Pattern | Example |
|---|---|---|
| Configure | `<preset-name>` | `unixlike-gcc-14-debug` |
| Build | `build-<preset-name>` | `build-unixlike-gcc-14-debug` |
| Test | `test-<preset-name>` | `test-unixlike-gcc-14-debug` |

### 1. Install Conan dependencies

```bash
conan install . --build=missing -pr:h=default -pr:b=default
```

### 2. Configure

```bash
# List all available presets
cmake --list-presets

# Example: GCC 14 debug on Linux/macOS
cmake --preset unixlike-gcc-14-debug

# Example: Clang 18 release
cmake --preset unixlike-clang-18-release

# Windows (Visual Studio 2022)
cmake --preset windows-msvc-debug
```

### 3. Build

```bash
cmake --build --preset build-unixlike-gcc-14-debug
```

### 4. Test

```bash
ctest --preset test-unixlike-gcc-14-debug
```

### Available compiler presets

<details>
<summary>GCC (Linux)</summary>

`unixlike-gcc-{10..15}-{debug,release}`

</details>

<details>
<summary>Clang (Linux)</summary>

`unixlike-clang-{12..21}-{debug,release}`

Static analysis variants (clang-tidy + cppcheck):
`unixlike-clang-{15..21}-{debug,release}-static-analysis`

</details>

<details>
<summary>Windows</summary>

`windows-msvc-{debug,release}`, `windows-clang-cl-{debug,release}`

</details>

<details>
<summary>Special</summary>

- ARM cross-compile: `arm-cortex-m4`
- Fuzzing (Clang): `fuzzing-clang-{12..21}`
- Qt: `unixlike-qt-clang-{15..21}-debug`

</details>

### Enabling example sub-projects

Pass `-D` options during configuration, or set them in your `CMakeUserPresets.json`:

```bash
cmake --preset unixlike-gcc-14-debug \
  -DCPP_STARTER_USE_SML=ON \
  -DCPP_STARTER_USE_IMGUI=ON \
  -DCPP_STARTER_USE_QT=ON
```

> **Note:** Make sure the corresponding Conan options are enabled too (see Conan section).

---

## CMake Options Reference

### Build tooling

| Option | Default | Description |
|---|---|---|
| `WARNINGS_AS_ERRORS` | `ON` | Treat compiler warnings as errors |
| `ENABLE_PCH` | `OFF` | Precompiled headers |
| `ENABLE_CACHE` | `ON` | ccache/sccache if available |
| `ENABLE_IPO` | `OFF` | Link-time optimisation (LTO) |
| `ENABLE_DOXYGEN` | `OFF` | Generate Doxygen docs |
| `ENABLE_COVERAGE` | `OFF` | GCov/LCOV coverage |
| `ENABLE_BUILD_WITH_TIME_TRACE` | `OFF` | `-ftime-trace` JSON (Clang only) |
| `BUILD_SHARED_LIBS` | `OFF` | Shared libraries |

### Static analysis

| Option | Default | Description |
|---|---|---|
| `ENABLE_CLANG_TIDY` | `OFF` | Run clang-tidy |
| `ENABLE_CPPCHECK` | `OFF` | Run cppcheck |
| `ENABLE_INCLUDE_WHAT_YOU_USE` | `OFF` | Run iwyu |

### Testing

| Option | Default | Description |
|---|---|---|
| `ENABLE_TESTING` | `ON` | Build test targets |
| `ENABLE_FUZZING` | `OFF` | Build libFuzzer target (Clang only) |
| `CPP_STARTER_USE_CATCH2` | `ON` | Catch2 test suite |
| `CPP_STARTER_USE_GTEST` | `ON` | GoogleTest suite |

### Sanitizers

Sanitizers are mutually exclusive where required — CMake enforces this automatically.

| Option | Default | Conflicts with |
|---|---|---|
| `ENABLE_SANITIZER_ADDRESS` | `OFF` | TSan, MSan |
| `ENABLE_SANITIZER_LEAK` | `OFF` | TSan, MSan |
| `ENABLE_SANITIZER_UNDEFINED_BEHAVIOR` | `OFF` | — |
| `ENABLE_SANITIZER_THREAD` | `OFF` | ASan, LSan, MSan |
| `ENABLE_SANITIZER_MEMORY` | `OFF` | ASan, TSan, LSan |

### Example sub-projects

| Option | Default | Description |
|---|---|---|
| `CPP_STARTER_USE_SML` | `OFF` | Boost.SML state machine |
| `CPP_STARTER_USE_BOOST_BEAST` | `OFF` | HTTP/WebSocket server |
| `CPP_STARTER_USE_CROW` | `OFF` | REST API server |
| `CPP_STARTER_USE_CPPZMQ_PROTO` | `OFF` | Protobuf + ZeroMQ messaging |
| `CPP_STARTER_USE_OPEN62541` | `OFF` | OPC UA (C) |
| `CPP_STARTER_USE_OPEN62541PP` | `OFF` | OPC UA (C++ wrapper) |
| `CPP_STARTER_USE_SLINT` | `OFF` | Slint declarative UI |
| `CPP_STARTER_USE_IMGUI` | `OFF` | Dear ImGui (GLFW + OpenGL3) |
| `CPP_STARTER_USE_QT` | `OFF` | Qt 6 QML example |
| `CPP_STARTER_USE_EMBEDDED_TOOLCHAIN` | `OFF` | ARM Cortex-M4 cross-compile |

---

## Conan Options

Feature options in `conanfile.py` control which libraries are fetched. They mirror the CMake options above.

```bash
conan install . --build=missing \
  -o use_sml=True \
  -o use_imgui=True \
  -o use_qt=True
```

| Option | Default |
|---|---|
| `use_sml` | `True` |
| `use_boost_beast` | `True` |
| `use_crow` | `True` |
| `use_cppzmq_proto` | `False` |
| `use_qt` | `False` |
| `use_open62541` | `True` |
| `use_open62541pp` | `True` |
| `use_slint` | `True` |
| `use_imgui` | `True` |

> `slint` and `open62541pp` are fetched via CMake FetchContent at configure time, not through Conan, but the options still control whether their CMake targets are built.

---

## Project Structure

```
cmake/              # CMake modules and toolchain files
cmake/presets/      # Preset definitions (base, gcc, clang, windows, special)
src/                # Source examples (one subdirectory per library)
test/               # Test suites (Catch2, GoogleTest)
fuzz_test/          # libFuzzer harness
templates/          # version.hpp.in for git-hash stamping
docker/             # Dockerfile + docker-compose for CI and dev
.devcontainer/      # VS Code Dev Container configuration
```

---

## Troubleshooting

### Update Conan

```bash
pip install --user --upgrade conan
```

### Clear Conan cache

```bash
conan remove -c '*'
```

### Regenerate CMake build directory

```bash
rm -rf cmake-build-*/   # or the specific build dir
cmake --preset <preset>
```

---

## Testing

- [Catch2 tutorial](https://github.com/catchorg/Catch2/blob/master/docs/tutorial.md)
- [GoogleTest primer](http://google.github.io/googletest/)

## Fuzz testing

Fuzzing targets require a Clang-based preset with `ENABLE_FUZZING=ON` or a `fuzzing-clang-*` preset:

```bash
cmake --preset fuzzing-clang-18
cmake --build --preset build-fuzzing-clang-18
./fuzz_test/fuzz_tester -max_total_time=60
```

See the [libFuzzer tutorial](https://github.com/google/fuzzing/blob/master/tutorial/libFuzzerTutorial.md) for details.
