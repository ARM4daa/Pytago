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
        "-ffast-math",
    ],
    extra_link_args=["-flto"],
)

setup(
    name="pytago_core",
    version="1.0",
    ext_modules=[module],
)


module = Extension(
    "pytago_ai",
    sources=[
        "src/wrappers/python_ai.c",
        "src/ai/pytago_ai.c",
        "src/core/masks.c",
    ],
    include_dirs=["src/core", "src/ai"],
    extra_compile_args=[
        "-O3",
        "-march=native",
        "-mtune=native",
        "-flto",
        "-funroll-loops",
        "-ffast-math",
    ],
    extra_link_args=["-flto"],
)

setup(
    name="pytago_ai",
    version="1.0",
    ext_modules=[module],
)
