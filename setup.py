from setuptools import setup, find_packages

setup(
    name="cmarkcffi",
    version="0.1.0",
    description="cffi bindings to cmark",
    url="https://github.com/pegov/cmarkcffi",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],
    cffi_modules=["src/cmarkcffi/cmark_build.py:ffibuilder"],
    include_package_data=True,
)
