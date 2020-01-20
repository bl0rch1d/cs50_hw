class CardValidator:
    def __init__(self, card_number):
        self.card_number = card_number
        self.num_len = len(card_number)

    def call(self):
        self.__convert_to_list()
        self.__cnl.reverse()
        self.__step_1()
        self.__step_2()
        self.__cnl.reverse()
        self.__step_3()

    def __convert_to_list(self):
        self.__cnl = [int(x) for x in self.card_number]

    def __step_1(self):
        result = 0
        temp = []
        for i in range(self.num_len):
            if i % 2 != 0:
                temp.append(self.__cnl[i])

        for i in range(len(temp)):
            temp[i] = temp[i] * 2

        for i in temp:
            digits_list = []
            mid_sum = 0
            if i > 9:
                digits_list = [int(x) for x in str(i)]
                for digit in digits_list:
                    mid_sum = mid_sum + digit
            else:
                mid_sum = i

            result = result + mid_sum

        self.__step_1_res = result

    def __step_2(self):
        total_sum = self.__step_1_res
        for i in range(self.num_len):
            if i % 2 == 0:
                total_sum = total_sum + self.__cnl[i]

        if total_sum % 10 != 0:
            print('INVALID')
            exit(1)

    def __step_3(self):
        if self.__cnl[0:2] in [[3, 7], [3, 4]]:
            print('AMEX')
        elif self.__cnl[0:2] in [[5, 1], [5, 2], [5, 3], [5, 4], [5, 5]]:
            print('MASTERCARD')
        elif self.__cnl[0] == 4:
            print('VISA')
        else:
            print('INVALID')


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def main():
    card_number = 0
    while True:
        card_number = input('Number: ')

        if (isint(card_number) and int(card_number) > 0):
            break

    cv = CardValidator(card_number)
    cv.call()


if __name__ == '__main__':
    main()
