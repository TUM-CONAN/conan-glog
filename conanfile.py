from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.util import files
import os
import shutil

class LibGlogConan(ConanFile):
    name = "glog"
    version = "0.3.5-rev-8d7a107"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = [
        "patches/CMakeProjectWrapper.txt"
    ]
    url = "https://gitlab.lan.local/conan/conan-glog"
    license="BSD 3-Clause"
    description = "C++ implementation of the Google logging module."
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    short_paths = False

    def source(self):
        rev = "8d7a107d68c127f3f494bb7807b796c8c5a97a82"
        tools.get("https://github.com/google/glog/archive/{0}.tar.gz".format(rev))
        os.rename("glog-" + rev, self.source_subfolder)

    def build(self):
        glog_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeProjectWrapper.txt", "CMakeLists.txt")

        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["WITH_GFLAGS"] = "OFF"
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
