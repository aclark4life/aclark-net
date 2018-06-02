from django.db.models import F
from django.db.models import Sum
from decimal import Decimal


def get_total(field=None, invoices=None, projects=None, times=None, team=None):
    """
    Get amount, cost, hours based on object and field requested.
    """
    if field == 'amount' and invoices:
        amount = invoices.aggregate(amount=Sum(F('amount')))['amount']
        return amount
    elif field == 'cost' and projects:
        cost = projects.aggregate(cost=Sum(F('cost')))['cost']
        return cost
    elif field == 'hours' and times:
        hours = {}
        hours['total'] = 0.0
        total_hours = times.aggregate(hours=Sum(F('hours')))['hours']
        if total_hours:
            hours['total'] = total_hours
        if team:
            hours['users'] = {}
            for user in team:
                hours['users'][user] = 0.0
                times_user = times.filter(user=user)
                hours_user = times_user.aggregate(
                    hours=Sum(F('hours')))['hours']
                if hours_user:
                    hours['users'][user] = hours_user
        return hours


def set_total(times, estimate=None, invoice=None, project=None):
    """
    Set amount, cost totals based on object type.
    """
    invoice_amount = 0
    time_amount = 0
    for time_entry in times:
        hours = time_entry.hours
        if time_entry.task:
            rate = time_entry.task.rate
            if rate:
                time_amount = rate * hours
        time_entry.amount = '%.2f' % time_amount
        invoice_amount += time_amount
    if invoice:
        invoice.amount = '%.2f' % invoice_amount
        invoice.save()
    elif estimate:
        estimate.amount = '%.2f' % invoice_amount
        estimate.save()
    elif project:
        cost = 0
        team = project.team.all()
        if team:
            hours = get_total(field='hours', times=times, team=team)
            for user in hours['users']:
                rate = user.profile.rate
                if rate:
                    cost += rate * Decimal(hours['users'][user])
        project.amount = '%.2f' % invoice_amount
        project.cost = '%.2f' % cost
        project.save()
    return times
