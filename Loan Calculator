import argparse
from math import ceil, log, floor


def calculate_annuity_payment(p, i, n):
    return ceil(p * i * (1 + i) ** n / ((1 + i) ** n - 1))


def calculate_differentiated_payment(p, i, n):
    diff_month_pay = []
    for m in range(n):
        diff_month_pay.append(ceil(p / n + i * p * (1 - m / n)))
    return diff_month_pay


def calculate_loan_principal(a, i, n):
    denominator = i * (1 + i) ** n / ((1 + i) ** n - 1)
    return floor(a / denominator)


def calculate_payments_periods(a, p, i):
    month = ceil(log(a / (a - i * p), 1 + i))
    return month // 12, month % 12, month


parser = argparse.ArgumentParser(description="Loan Calculator")
parser.add_argument("-t", "--type", choices=["annuity", "diff"],
                    help='indicates the type of payment: "annuity" or "diff"')
parser.add_argument("--payment", type=float,
                    help='is the monthly payment amount.')
parser.add_argument("--principal", type=float,
                    help='you can get its value if you know the interest, annuity payment, and number of months.')
parser.add_argument("--periods", type=int,
                    help='denotes the number of months needed to repay the loan.')
parser.add_argument("--interest", type=float,
                    help='specified without a percent sign.')
parser_set = {'interest', 'periods', 'principal', 'payment', 'type'}
args_dict = vars(parser.parse_args())
args_set = set(key for key in args_dict if args_dict[key])
command = parser_set - args_set
neg_input = any(args_dict[key] < 0 for key in (args_set - {'type'}))
if not args_dict['interest'] \
        or (args_dict['type'] == 'diff' and args_dict['payment'] is not None) \
        or neg_input \
        or len(args_set) < 4:
    print('Incorrect parameters')
elif args_dict['type'] == 'annuity':
    if 'payment' in command:
        loan_principal = args_dict['principal']
        months = args_dict['periods']
        loan_interest = args_dict['interest'] / 12 / 100  # i
        monthly_payment = calculate_annuity_payment(loan_principal, loan_interest, months)
        print(f'Your monthly payment = {monthly_payment}!')

    elif 'periods' in command:
        loan_principal = args_dict['principal']
        monthly_payment = args_dict['payment']
        loan_interest = args_dict['interest'] / 12 / 100  # i
        years, month12, months = calculate_payments_periods(monthly_payment, loan_principal, loan_interest)
        years_str = f"{years} year{'s' if years > 1 else ''}"
        months_str = f" and {month12} month{'s' if month12 > 1 else ''}" if month12 > 0 else ''
        print('It will take ' + years_str + months_str + ' to repay this loan!')

    elif 'principal' in command:
        monthly_payment = args_dict['payment']
        months = args_dict['periods']
        loan_interest = args_dict['interest'] / 12 / 100  # i
        loan_principal = calculate_loan_principal(monthly_payment, loan_interest, months)
        print(f'Your loan principal = {loan_principal}!')

    overpayment = int(months * monthly_payment - loan_principal)
    print(f'Overpayment = {overpayment}')

elif args_dict['type'] == 'diff':
    if 'payment' in command:
        loan_principal = args_dict['principal']
        months = args_dict['periods']
        loan_interest = args_dict['interest'] / 12 / 100  # i
        monthly_payment = calculate_differentiated_payment(loan_principal, loan_interest, months)
        for mn, month_pay in enumerate(monthly_payment):
            print(f'Month {mn + 1}: payment is {month_pay}')
        overpayment = int(sum(monthly_payment) - loan_principal)
        print(f'Overpayment = {overpayment}')
