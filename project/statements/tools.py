import csv

from django.core.exceptions import ValidationError
from statements.models import Account, Statement, StatementItem
from django.db import transaction

def statement_import(file_handler):
    idx = 0
    accounts_cache = {}
    statements_cache = {}

    # TODO: TASK → in case of errors database must not change
    with transaction.atomic():
        # TODO: TASK → optimize database queries during import
        
        for row in csv.DictReader(file_handler):
            account_name = row['account']
            currency = row['currency']
            date = row['date']

            # Cache Account get_or_create
            if account_name not in accounts_cache:
                account = Account.objects.get_or_create(
                    name=account_name,
                    defaults={'currency': currency}
                )[0]
                accounts_cache[account_name] = account
            else:
                account = accounts_cache[account_name]

            if account.currency != currency:
                raise ValidationError('Invalid currency currency')

            # Cache Statement get_or_create
            statement_key = (account.id, date)
            if statement_key not in statements_cache:
                statement = Statement.objects.get_or_create(
                    account=account,
                    date=date
                )[0]
                statements_cache[statement_key] = statement
            else:
                statement = statements_cache[statement_key]

            StatementItem.objects.create(
                statement=statement,
                amount=row['amount'],
                currency=currency,
                title=row['title'],
                comments=row.get('comments', ''),
            )
            idx += 1

    return idx

