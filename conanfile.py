from conans import ConanFile, CMake, tools
import os
import shutil


class LibGlogConan(ConanFile):
    name = "glog"
    package_revision = "-r2"
    upstream_version = "0.4.0"
    version = "{0}{1}".format(upstream_version, package_revision)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = [
        "patches/CMakeProjectWrapper.txt"
    ]
    url = "https://git.ircad.fr/conan/conan-glog"
    license = "BSD 3-Clause"
    description = "C++ implementation of the Google logging module."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def requirements(self):
        self.requires("common/1.0.1@sight/testing")

    def source(self):
        tools.get("https://github.com/google/glog/archive/v{0}.tar.gz".format(self.upstream_version))
        os.rename("glog-" + self.upstream_version, self.source_subfolder)

    def build(self):
        # Import common flags and defines
        import common

        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")

        cmake = CMake(self)

        # Export common flags
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_RELEASE"] = common.get_cxx_flags_release()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_DEBUG"] = common.get_cxx_flags_debug()
        cmake.definitions["SIGHT_CMAKE_CXX_FLAGS_RELWITHDEBINFO"] = common.get_cxx_flags_relwithdebinfo()

        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["WITH_GFLAGS"] = "OFF"
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
