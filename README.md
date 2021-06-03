# cmarkcffi

cffi bindings to cmark.

## Usage

```python
from cmarkcffi import markdown_to_html

html = markdown_to_html("*text*")
```

```python
from cmarkcffi import Options, markdown_to_html

html = markdown_to_html(md_text, Options.UNSAFE | Options.SMART)
```

