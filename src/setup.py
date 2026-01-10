import os
from setuptools import setup, Extension


"""
is_android = "ANDROID_ARGUMENT" in os.environ


opt_flags = ["-O3", "-funroll-loops"]
host_flags = [] if is_android else ["-flto", "-march=native", "-mtune=native"]

compile_args = opt_flags + host_flags
link_args = [] if is_android else ["-flto"]
"""

core_module = Extension(
    "wrappers.pytago_core",
    sources=[
        "wrappers/python_core.c",
        "core/masks.c",
    ],
    include_dirs=["core"],
    extra_compile_args=["-O3", "-funroll-loops"]
    #extra_link_args=link_args,
)

ai_module = Extension(
    "wrappers.pytago_ai",
    sources=[
        "wrappers/python_ai.c",
        "ai/pytago_ai.c",
        "core/masks.c",
    ],
    include_dirs=["core", "ai"],
    extra_compile_args=["-O3", "-funroll-loops"]
    #extra_link_args=link_args,
)


setup(
    name="pytago_lib",
    version="1.0",
    #package_dir={"": "."},
    packages=["ui", "wrappers"],
    ext_modules=[core_module, ai_module],
    #ext_package="pytago_lib"
)
