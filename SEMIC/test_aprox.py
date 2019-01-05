import decimal
from math import sqrt, exp, pi, e

decimal.getcontext().prec = 1000

def main():
    n = 10000000
    p = decimal.Decimal(1/(4*n*sqrt(3)))*decimal.Decimal(e)**(decimal.Decimal(pi)*decimal.Decimal(sqrt(2*n/3)))
    print(p)


if __name__ == '__main__':
    main()