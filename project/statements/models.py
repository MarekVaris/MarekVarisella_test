from decimal import Decimal
from django.db import models, connection
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import defaultdict


def report_turnover_by_year_month(period_begin, period_end):
    # TODO: TASK → make report using 1 database query without any math in python
    sql = """
        SELECT
            strftime('%%Y-%%m', s.date) AS month,
            si.currency,
            SUM(CASE WHEN si.amount >= 0 THEN si.amount ELSE 0 END) AS incomes,
            SUM(CASE WHEN si.amount < 0 THEN -si.amount ELSE 0 END) AS expenses
        FROM
            statements_statementitem si
        JOIN
            statements_statement s ON si.statement_id = s.id
        WHERE
            s.date BETWEEN %s AND %s
        GROUP BY
            month,
            si.currency
        ORDER BY
            month ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [period_begin, period_end])
        rows = cursor.fetchall()

    report = {}

    for ym, currency, incomes, expenses in rows:
        if ym not in report:
            report[ym] = {'incomes': {}, 'expenses': {}}

        if incomes > 0:
            report[ym]['incomes'][currency] = round(incomes, 2)
        if expenses > 0:
            report[ym]['expenses'][currency] = round(expenses, 2)

    return report

class Account(models.Model):
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # TODO: TASK → add field balance that will update automatically 

    # When StatementItem item is created balance is updated
    def update_balance(self):
        total = StatementItem.objects.filter(
            statement__account=self
        ).aggregate(total=Sum('amount'))['total'] 
        self.balance = total
        self.save(update_fields=['balance'])

    def __str__(self):
        return f'{self.name}[{self.currency}] {self.balance}'    


class Statement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    date = models.DateField()
    # TODO: TASK → make sure that account and date is unique on database level
    class Meta:
        unique_together = ('account', 'date')

    def __str__(self):
        return f'{self.account} → {self.date}'
    

class StatementItem(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    comments = models.TextField(blank=True, null=True)
    # TODO:  TASK → add field comments (type text)

    def __str__(self):
        return f'[{self.statement}] {self.amount} {self.currency} → {self.title} {self.comments}'


# Signal to update account balance after StatementItem is created
@receiver(post_save, sender=StatementItem)
def update_account_balance(sender, instance, created, **kwargs):
    if created:
        instance.statement.account.update_balance()
