card_number = 0
cn = []

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

while True:
    card_number = input('Number: ')

    if (isint(card_number) and int(card_number) > 0):
        cn = [int(x) for x in card_number]
        break

print(cn.reverse()[1::2])
exit(1)

odd_digits = []
for i in reversed:
    cn.reverse()
    # rev = cn
    # rev.reverse()
    print(cn[i])
    # if i % 2 != 0:
    #     print(rev[i])
    #     odd_digits.append(rev[i])

exit(1)

sum_of_odd_digits = 0
for i in range(len(odd_digits)):
    odd_digits[i] = odd_digits[i] * 2

for i in odd_digits:
    temp_arr = []
    mid_sum = 0
    if i > 9:
        temp_arr = [int(x) for x in str(i)]
        for el in temp_arr:
            mid_sum = mid_sum + el
    else:
        mid_sum = i

    sum_of_odd_digits = sum_of_odd_digits + mid_sum


total_sum = sum_of_odd_digits
for i in range(len(cn)):
    if i % 2 != 0:
        total_sum = total_sum + cn[i]

print(total_sum)

if total_sum % 10 != 0:
    print("INVALID")
    exit(1)

if cn[0] in [37,34]:
    print('AMEX')
elif cn[0] in [51,52,53,54,55]:
    print('MASTERCARD')
elif cn[0] == 4:
    print('VISA')
else:
    print('INVALID')
