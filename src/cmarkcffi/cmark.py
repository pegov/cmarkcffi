from cmarkcffi._cmark import ffi as _ffi
from cmarkcffi._cmark import lib as _lib


class Options:
    DEFAULT = _lib.CMARK_OPT_DEFAULT
    SOURCEPOS = _lib.CMARK_OPT_SOURCEPOS
    HARDBREAKS = _lib.CMARK_OPT_HARDBREAKS
    UNSAFE = _lib.CMARK_OPT_UNSAFE
    NOBREAKS = _lib.CMARK_OPT_NOBREAKS
    VALIDATE_UTF8 = _lib.CMARK_OPT_VALIDATE_UTF8
    SMART = _lib.CMARK_OPT_SMART


def markdown_to_html(md: str, options: int = Options.DEFAULT) -> str:
    md_bytes = md.encode("utf-8")
    raw = _lib.cmark_markdown_to_html(md_bytes, len(md_bytes), options)
    return _ffi.string(raw).decode("utf-8")
