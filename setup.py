from setuptools import setup, Extension

module = Extension(
    "pytago_core",
    sources=[
        "src/wrappers/python_core.c",
        "src/core/masks.c",
    ],
    include_dirs=["src/core"],
    extra_compile_args=[
        "-O3",
        "-march=native",
        "-mtune=native",
        "-flto",
        "-funroll-loops",
        "-fstrict-aliasing",
        "-ffast-math",
    ],
    extra_link_args=["-flto"],
)

setup(
    name="pytago_core",
    version="1.0",
    ext_modules=[module],
)
