from django.contrib.auth.models import User
from accounts.models import Day

from django import template
from django.template import RequestContext

register = template.Library()

@register.simple_tag(takes_context=True)
def calendar_year(context):
	u = context['request'].user
	d = Day.objects.filter(user_id=u.id).latest('date')
	return d.date.year

@register.simple_tag(takes_context=True)
def calendar_month(context):
	u = context['request'].user
	d = Day.objects.filter(user_id=u.id).latest('date')
	return d.date.month