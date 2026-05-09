from django import template

register = template.Library()


@register.filter
def split_lines(value):
    """Return non-empty stripped lines for rendering newline-separated fields as lists."""
    if not value:
        return []
    return [line.strip() for line in str(value).splitlines() if line.strip()]