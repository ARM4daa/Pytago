from setuptools import setup, Extension

core_module = Extension(
    "pytago_core",
    sources=[
        "src/wrappers/python_core.c",
        "src/core/masks.c",
    ],
    include_dirs=["src/core"],
    extra_compile_args=[
        "-O3",
        "-flto",
        "-funroll-loops",
        "-march=native",
        "-mtune=native"
    ],
    extra_link_args=["-flto"],
)

ai_module = Extension(
    "pytago_ai",
    sources=[
        "src/wrappers/python_ai.c",
        "src/ai/pytago_ai.c",
        "src/core/masks.c",
    ],
    include_dirs=["src/core", "src/ai"],
    extra_compile_args=[
        "-O3",
        "-flto",
        "-funroll-loops",
        "-march=native",
        "-mtune=native"
    ],
    extra_link_args=["-flto"],
)

setup(
    name="pytago",
    version="1.0",
    ext_modules=[core_module, ai_module],
)
