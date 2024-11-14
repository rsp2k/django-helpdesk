#!/usr/bin/python
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

scripts/escalate_tickets.py - Easy way to escalate tickets based on their age,
                              designed to be run from Cron or similar.
"""

from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from helpdesk.lib import safe_template_context
from helpdesk.models import EscalationExclusion, Queue, Ticket


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-q',
            '--queues',
            nargs='*',
            choices=list(Queue.objects.values_list('slug', flat=True)),
            help='Queues to include (default: all). Enter the queues slug as space separated list.'
        )
        parser.add_argument(
            '-x',
            '--escalate-verbosely',
            action='store_true',
            default=False,
            help='Display escalated tickets'
        )

    def handle(self, *args, **options):
        verbose = options['escalate_verbosely']
        queue_slugs = options['queues']

        # Only include queues with escalation configured
        queues = Queue.objects.filter(escalate_days__isnull=False).exclude(escalate_days=0)
        if queue_slugs is not None:
            queues = queues.filter(slug__in=queue_slugs)

        if verbose:
            self.stdout.write(f"Processing: {queues}")

        for queue in queues:
            tickets = queue.objects.escalate_tickets()
            if verbose:
                for ticket in tickets:
                    self.stdout.write(f"  - Escalating {ticket.ticket} from {ticket.priority + 1}>{ticket.priority}")
