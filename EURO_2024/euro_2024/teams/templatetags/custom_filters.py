from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='italic_bold_positions')
def italic_bold_positions(value):
    positions = ['goalkeeper', 'midfielder', 'defender', 'attacker']
    for position in positions:
        value = re.sub(f'(?i)({position}s?)', r'<em><strong>\1</strong></em>', value)
    return mark_safe(value)
