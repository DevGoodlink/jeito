from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import F, Q, Sum, Case, When, Value
from django_filters.views import FilterView
from .filters import BalanceFilter, AccountFilter, EntryFilter, BudgetFilter
from .models import BankStatement, Transaction, Entry


class UserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class BudgetView(UserMixin, FilterView):
    template_name = "accounting/budget.html"
    filterset_class = BudgetFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list
        qs = qs.filter(account__number__regex=r'^[67]')
        qs = qs.values('analytic__id', 'analytic__title')
        qs = qs.annotate(solde_real=Sum(Case(When(entry__projected=False, then=F('revenue') - F('expense')),
                                             default=Value(0))),
                         solde_proj=Sum(Case(When(entry__projected=True, then=F('revenue') - F('expense')),
                                             default=Value(0))))
        qs = qs.order_by('analytic__title')
        for row in qs:
            row['solde_total'] = row['solde_real'] + row['solde_proj']
        context['data'] = qs
        context['solde_real'] = sum([account['solde_real'] for account in qs])
        context['solde_proj'] = sum([account['solde_proj'] for account in qs])
        context['solde_total'] = sum([account['solde_total'] for account in qs])
        return context


class ProjectionView(UserMixin, FilterView):
    template_name = "accounting/projection.html"
    filterset_class = BudgetFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list
        qs = qs.filter(account__number__regex=r'^[67]')
        qs = qs.values('account_id', 'account__number', 'account__title', 'analytic__id', 'analytic__title')
        qs = qs.order_by('account__number', 'analytic__title')
        qs = qs.annotate(solde=Sum(F('revenue') - F('expense')))
        context['data'] = qs
        context['solde'] = sum([account['solde'] for account in qs])
        return context


class AnalyticBalanceView(UserMixin, FilterView):
    template_name = "accounting/analytic_balance.html"
    filterset_class = BalanceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list
        qs = qs.filter(account__number__regex=r'^[67]')
        qs = qs.values('analytic__id', 'analytic__title')
        qs = qs.annotate(revenue=Sum('revenue'), expense=Sum('expense'))
        qs = qs.order_by('analytic__title')
        for analytic in qs:
            analytic['solde'] = analytic['revenue'] - analytic['expense']
        context['data'] = qs
        context['revenues'] = sum([analytic['revenue'] for analytic in qs])
        context['expenses'] = sum([analytic['expense'] for analytic in qs])
        context['solde'] = sum([analytic['solde'] for analytic in qs])
        return context


class BalanceView(UserMixin, FilterView):
    template_name = "accounting/balance.html"
    filterset_class = BalanceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list
        qs = qs.values('account__id', 'account__number', 'account__title')
        qs = qs.annotate(revenues=Sum('revenue'), expenses=Sum('expense'))
        qs = qs.order_by('account__number')
        for account in qs:
            account['solde'] = account['revenues'] - account['expenses']
        context['data'] = qs
        context['revenues'] = sum([account['revenues'] for account in qs])
        context['expenses'] = sum([account['expenses'] for account in qs])
        context['solde'] = sum([account['solde'] for account in qs])
        return context


class AccountView(UserMixin, FilterView):
    template_name = "accounting/account.html"
    filterset_class = AccountFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solde = 0
        revenue = 0
        expense = 0
        for transaction in self.object_list:
            solde += transaction.revenue - transaction.expense
            transaction.solde = solde
            revenue += transaction.revenue
            expense += transaction.expense
        context['revenue'] = revenue
        context['expense'] = expense
        context['solde'] = solde
        return context


class EntryListView(UserMixin, FilterView):
    template_name = "accounting/entry_list.html"
    filterset_class = EntryFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revenue = 0
        expense = 0
        balance = 0
        for entry in self.object_list:
            revenue += entry.revenue
            expense += entry.expense
            balance += entry.balance
        context['revenue'] = revenue
        context['expense'] = expense
        context['balance'] = balance
        return context


class BankStatementView(UserMixin, ListView):
    model = BankStatement


class ReconciliationView(UserMixin, DetailView):
    template_name = 'accounting/reconciliation.html'
    model = BankStatement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            previous = BankStatement.objects.filter(date__lt=self.object.date).latest('date')
        except BankStatement.DoesNotExist:
            cond = Q()
        else:
            cond = Q(reconciliation__gt=previous.date)
        transactions = Transaction.objects.filter(account__number=5120000)
        transactions = transactions.filter(entry__projected=False)
        cond = cond & Q(reconciliation__lte=self.object.date) | \
            Q(reconciliation=None, entry__date__lte=self.object.date)
        transactions = transactions.filter(cond)
        transactions = transactions.order_by('reconciliation', 'entry__date')
        context['transactions'] = transactions
        return context


class NextReconciliationView(UserMixin, ListView):
    template_name = 'accounting/next_reconciliation.html'

    def get_queryset(self):
        qs = Transaction.objects.filter(account__number=5120000, reconciliation=None, entry__projected=False)
        qs = qs.order_by('entry__date')
        return qs


class EntryView(UserMixin, DetailView):
    model = Entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = self.object.transaction_set.order_by('account__number', 'analytic__title')
        return context
