import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.43.0"

class BShoshanyThreadPoolConan(ConanFile):
    description = "BS::thread_pool: a fast, lightweight, and easy-to-use C++17 thread pool library"
    homepage = "https://github.com/bshoshany/thread-pool"
    license = "MIT"
    name = "bshoshany-thread-pool"
    no_copy_source = True
    settings = "arch", "build_type", "compiler", "os"
    topics = ("concurrency", "cpp17", "header-only", "library", "multi-threading", "parallel-computing", "thread-pool", "threads")
    url = "https://github.com/conan-io/conan-center-index"

    @property
    def _minimum_compilers_version(self):
        return {
            "apple-clang": "10",
            "clang": "5",
            "gcc": "8",
            "Visual Studio": "16"
        }

    @property
    def _minimum_cpp_standard(self):
        return 17

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def package(self):
        self.copy("BS_thread_pool.hpp", src=os.path.join(self._source_subfolder, "./"), dst="include")
        self.copy("LICENSE.txt", src=os.path.join(self._source_subfolder, "./"), dst="licenses")

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
        self.cpp_info.names["cmake_find_package"] = "bshoshany-thread-pool"
        self.cpp_info.names["cmake_find_package_multi"] = "bshoshany-thread-pool"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def validate(self):
        if self.settings.get_safe("compiler.cppstd"):
            tools.check_min_cppstd(self, self._minimum_cpp_standard)
        try:
            if tools.Version(self.settings.compiler.version) < self._minimum_compilers_version[str(self.settings.compiler)]:
                raise ConanInvalidConfiguration(f"{self.name} requires a compiler that supports C++{self._minimum_cpp_standard}. {self.settings.compiler}, {self.settings.compiler.version}")
        except KeyError:
            self.output.warn("Unknown compiler encountered. Assuming it supports C++17.")
