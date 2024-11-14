from django import template
from django.urls import reverse
from django.utils.http import urlencode

from helpdesk import settings as helpdesk_settings

register = template.Library()


@register.simple_tag
def helpdesk_iframe(queue=None, title=None, body=None, submitter_email=None, **kwargs):
    if not helpdesk_settings.HELPDESK_KB_ENABLED:
        return

    url = reverse('helpdesk:submit_iframe')
    query_args = kwargs
    if queue:
        query_args['queue'] = queue
    if title:
        query_args['title'] = title
    if body:
        query_args['body'] = body
    if submitter_email:
        query_args['submitter_email'] = submitter_email

    return f'{url}?{urlencode(query_args)}'


@register.simple_tag
def kb_iframe(slug):
    url = reverse('helpdesk:kb_category_iframe', kwargs={'slug': slug})
    return url
