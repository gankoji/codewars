import random

sizes = [2, 4, 6, 10, 20, 50, 100, 150]
outfile = 'test_cases.py'

with open(outfile, 'w') as f:
    f.write(f'cases = []\n')
    for size in sizes:
        suppliers = [random.randint(1, 10000) for _ in range(size)]
        consumers = [random.randint(1, 10000) for _ in range(size)]
        costs = [[random.randint(0, 100) for _ in range(size)] for _ in range(size)]
        expected = random.randint(1,10000000)
        f.write(f'suppliers = {str(suppliers)}\n')
        f.write(f'consumers = {str(consumers)}\n')
        f.write(f'costs = [\n')
        for row in costs:
            f.write(f'\t{str(row)},\n')
        f.write(f']\n')
        f.write(f'expected = {expected}\n')
        f.write(f'cases.append([suppliers, consumers, costs, expected])\n')