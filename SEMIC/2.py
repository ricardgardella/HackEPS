import decimal
from math import sqrt, exp, pi, e

def main(n):
    if n < 5000:
        count = 0
        vk_1 = [0] * (n + 1)
        vk = [0] * (n + 1)
        vk_1[0] = 1

        for k in range(1, n+1):
            for j in range(1, n+1):
                vk[j] = vk_1[j - 1] + (vk[j - k] if j - k >= 0 else 0)
            vk_1 = list(vk)
            count += vk[n]
    else:
        count = decimal.Decimal(1/(4*n*sqrt(3)))*decimal.Decimal(e)**(decimal.Decimal(pi)*decimal.Decimal(sqrt(2*n/3)))
    print("Case #{}: {}".format(n, count))

if __name__ == '__main__':
    n = 100
    main(n)