coins = [0.25, 0.1, 0.05, 0.01]
change = 0
coins_amount = 0

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

while True:
    change = input("Change owed: ")

    if isfloat(change) and float(change) > 0:
        change = float(change)
        break

for i in coins:
    while (change >= i):
        change = round(change - i, 2)
        coins_amount = coins_amount + 1
    
print(coins_amount)
