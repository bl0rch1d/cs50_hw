import sys

PUNCTUATION_MARKS = [32, 36, 33, 44, 46, 63]


def encrypt(text, key):
    result = ''

    key = key.lower()
    shift = [ord(char) - 97 for char in key]

    key_counter = 0
    for char in text:
        if not char.isalpha():
            result += char
            continue
        elif (char.isupper()):
            result += chr((ord(char) + shift[key_counter] - 65) % 26 + 65)
        else:
            result += chr((ord(char) + shift[key_counter] - 97) % 26 + 97)

        key_counter = key_counter + 1

        if key_counter == len(shift):
            key_counter = 0

    return result


def check_text(text):
    if len(text) == 0:
        return False

    for char in text:
        if not char.isalpha() and not ord(char) in PUNCTUATION_MARKS:
            return False

    return True


def check_key(key):
    if len(key) == 0:
        return False

    for char in key:
        if not char.isalpha():
            return False

    return True


def main():
    plaintext = ''

    if len(sys.argv) != 2 or not check_key(sys.argv[1]):
        print('Usage: python vigenere.py key')
        exit(1)

    key = sys.argv[1]

    while not check_text(plaintext):
        plaintext = str(input("plaintext: "))

    result = encrypt(plaintext, key)

    print(f'ciphertext: {result}')


if __name__ == '__main__':
    main()
