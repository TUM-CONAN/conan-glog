from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibGlogConan(ConanFile):
    name = "glog"
    package_revision = "-r1"
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
    license="BSD 3-Clause"
    description = "C++ implementation of the Google logging module."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        self.requires("common/1.0.0@sight/stable")

    def source(self):
        tools.get("https://github.com/google/glog/archive/v{0}.tar.gz".format(self.upstream_version))
        os.rename("glog-" + self.upstream_version, self.source_subfolder)

    def build(self):
        #Import common flags and defines
        import common
        glog_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")

        cmake = CMake(self)
        
        #Set common flags
        cmake.definitions["CMAKE_C_FLAGS"] = common.get_c_flags()
        cmake.definitions["CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        
        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["WITH_GFLAGS"] = "OFF"
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
