import distutils.ccompiler
import distutils.dist
import glob
import os

from cffi import FFI

PACKAGE_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.abspath(os.path.join(PACKAGE_SRC_DIR, "../../"))
CMARK_SRC_DIR = os.path.join(PACKAGE_ROOT, "third_party/cmark/src")

UNIX_GENERATED_SRC_DIR = os.path.join(PACKAGE_ROOT, "generated", "unix")
WIN_GENERATED_SRC_DIR = os.path.join(PACKAGE_ROOT, "generated", "win")

CMARK_DEF_H_PATH = os.path.join(PACKAGE_SRC_DIR, "cmark.cffi.h")

with open(CMARK_DEF_H_PATH, "r", encoding="utf-8") as f:
    CMARK_DEF_H = f.read()


def _get_sources(dir, exclude=[]):
    sources = glob.iglob(os.path.join(dir, "*.c"))
    return sorted(
        [
            os.path.relpath(path, start=PACKAGE_ROOT)
            for path in sources
            if os.path.basename(path) not in exclude
        ]
    )


SOURCES = _get_sources(CMARK_SRC_DIR, exclude=set(["main.c"]))


def _compiler_type():
    dist = distutils.dist.Distribution()
    dist.parse_config_files()
    cmd = dist.get_command_obj("build")
    cmd.ensure_finalized()
    compiler = distutils.ccompiler.new_compiler(compiler=cmd.compiler)
    return compiler.compiler_type


COMPILER_TYPE = _compiler_type()

if COMPILER_TYPE in ["unix", "mingw32"]:
    EXTRA_COMPILE_ARGS = ["-std=c99"]
    GENERATED_SRC_DIR = UNIX_GENERATED_SRC_DIR
elif COMPILER_TYPE == "msvc":
    EXTRA_COMPILE_ARGS = ["/TP"]
    GENERATED_SRC_DIR = WIN_GENERATED_SRC_DIR
else:
    raise RuntimeError(f"Unsupported compiler: {COMPILER_TYPE}")

ffibuilder = FFI()
ffibuilder.cdef(CMARK_DEF_H)
ffibuilder.set_source(
    "cmarkcffi._cmark",
    '#include "cmark.h"',
    sources=SOURCES,
    include_dirs=[CMARK_SRC_DIR, GENERATED_SRC_DIR],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
