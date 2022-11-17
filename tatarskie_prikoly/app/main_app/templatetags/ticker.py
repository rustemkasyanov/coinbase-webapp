from django import template
from main_app.models import TickerData

register = template.Library()

@register.inclusion_tag('base/ticker.html', takes_context=True)
def ticker(context):
    currencies = TickerData.objects.all()
    context = {'ticker_currencies': currencies}
    return context