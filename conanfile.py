import os
from dataclasses import dataclass

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, cmake_layout, CMake
from conan.tools.files import get, copy, download


@dataclass
class Compiler:
    name: str
    version: str
    sha256: str
    extension: str


class CppExampleProjectConan(ConanFile):
    version = "0.0.1"
    name = "cpp_example_project"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    options = {
        "use_sml": [True, False],
        "use_boost_beast": [True, False],
        "use_crow": [True, False],
        "use_cppzmq_proto": [True, False],
        "use_qt": [True, False],
        "use_open62541": [True, False],
        "use_open62541pp": [True, False],  # fetched via FetchContent in CMake
        "use_slint": [True, False],         # fetched via FetchContent in CMake
        "use_imgui": [True, False],
    }

    default_options = {
        "use_sml": True,
        "use_boost_beast": True,
        "use_crow": True,
        "use_cppzmq_proto": False,
        "use_qt": False,
        "use_open62541": True,
        "use_open62541pp": True,
        "use_slint": True,
        "use_imgui": True,
        # library-level options
        "fmt/*:header_only": True,
        "spdlog/*:header_only": True,
        "qt/*:with_fontconfig": False,
        "open62541/*:cpp_compatible": True,
    }

    def _get_toolchain(self):
        if self.settings.os == "Windows":
            return Compiler(
                name="arm-none-linux-gnueabihf",
                version="14.3.rel1",
                sha256="fd0801c9fcb0327978e5f7594f38225b7dec0fd515006c1608f74c0460111312",
                extension=".zip",
            )
        return Compiler(
            name="arm-none-linux-gnueabihf",
            version="14.3.rel1",
            sha256="3ec0113af5154a2573b3851d74d9e9501a805abf9dfa0f82b04ef26fa0e6fc35",
            extension=".tar.xz",
        )

    def source(self):
        if self.settings.arch == "armv7":
            download(self, "https://developer.arm.com/GetEula?Id=37988a7c-c40e-4b78-9fd1-62c20b507aa8", "LICENSE", verify=False)

    # 3. call for conan install
    def requirements(self):
        # ARM cross-compilation: minimal dependency set
        if self.settings.arch == "armv7":
            self.requires("fmt/11.2.0")
            if self.options.use_sml:
                self.requires("sml/1.1.12")
            return

        # Qt-only build: only the Qt package is needed
        if self.options.use_qt:
            self.requires("qt/6.8.3")
            return

        # Standard desktop build
        self.requires("fmt/11.2.0")
        self.requires("spdlog/1.15.3")

        if self.options.use_sml:
            self.requires("sml/1.1.12")

        if self.options.use_boost_beast:
            self.requires("boost/1.88.0")
            self.requires("nlohmann_json/3.12.0")

        if self.options.use_crow:
            self.requires("crowcpp-crow/1.2.1")

        if self.options.use_cppzmq_proto:
            self.requires("cppzmq/4.11.0")
            self.requires("protobuf/6.30.1")

        if self.options.use_open62541 or self.options.use_open62541pp:
            self.requires("open62541/1.4.13")

        if self.options.use_imgui:
            self.requires("imgui/1.90.5")
            self.requires("implot/0.16")

    # 4. call for conan install
    def build_requirements(self):
        self.tool_requires("cmake/[>=4.0]")
        self.tool_requires("ninja/[>=1.11.0]")
        if self.settings.arch != "armv7":
            self.test_requires("catch2/3.10.0")
            self.test_requires("gtest/1.17.0")

    # 5. call for conan install
    def layout(self):
        cmake_layout(self)

    # 6. call for conan install
    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = "ConanPresets.json"
        tc.cache_variables["CMAKE_POLICY_VERSION_MINIMUM"] = "3.5"

        # Forward feature options to CMake cache variables for desktop builds
        if self.settings.arch != "armv7" and not self.options.use_qt:
            tc.cache_variables["CPP_STARTER_USE_SML"] = bool(self.options.use_sml)
            tc.cache_variables["CPP_STARTER_USE_BOOST_BEAST"] = bool(self.options.use_boost_beast)
            tc.cache_variables["CPP_STARTER_USE_CROW"] = bool(self.options.use_crow)
            tc.cache_variables["CPP_STARTER_USE_CPPZMQ_PROTO"] = bool(self.options.use_cppzmq_proto)
            tc.cache_variables["CPP_STARTER_USE_OPEN62541"] = bool(self.options.use_open62541)
            tc.cache_variables["CPP_STARTER_USE_OPEN62541PP"] = bool(self.options.use_open62541pp)
            tc.cache_variables["CPP_STARTER_USE_SLINT"] = bool(self.options.use_slint)
            tc.cache_variables["CPP_STARTER_USE_IMGUI"] = bool(self.options.use_imgui)

        if self.options.use_qt:
            tc.cache_variables["CPP_STARTER_USE_QT"] = True

        tc.generate()

        # Copy imgui backend bindings into the include path
        if self.options.use_imgui and "imgui" in self.dependencies:
            source_dir = os.path.join(self.dependencies["imgui"].package_folder, "res", "bindings")
            dest_dir = os.path.join(self.dependencies["imgui"].package_folder, "include", "backends")
            copy(self, "*", source_dir, dest_dir)

    # 1. call for conan build
    def build(self):
        if self.settings.arch == "armv7":
            compiler_definition = self._get_toolchain()
            get(
                self,
                f"https://developer.arm.com/-/media/Files/downloads/gnu/{compiler_definition.version}/binrel/"
                f"arm-gnu-toolchain-{compiler_definition.version}-x86_64-{compiler_definition.name}{compiler_definition.extension}",
                sha256=compiler_definition.sha256,
                strip_root=True,
            )

        cmake = CMake(self)
        cmake.configure()
        cmake.build()
