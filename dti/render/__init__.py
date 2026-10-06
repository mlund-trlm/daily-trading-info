"""HTML email rendering. Templates use inline styles so they survive Outlook."""

from jinja2 import Environment, PackageLoader, select_autoescape

_env = Environment(
    loader=PackageLoader("dti", "render/templates"),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(name: str, **ctx) -> str:
    return _env.get_template(name).render(**ctx)
