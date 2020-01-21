import sys

PUNCTUATION_MARKS = [32, 33, 44, 46, 63]


def encrypt(text, key):
    result = ""

    for char in text:
        if not char.isalpha():
            result += char
        elif (char.isupper()):
            result += chr((ord(char) + key - 65) % 26 + 65)
        else:
            result += chr((ord(char) + key - 97) % 26 + 97)

    return result


def check_text(text):
    if len(text) == 0:
        return False

    for char in text:
        if not char.isalpha() and not ord(char) in PUNCTUATION_MARKS:
            return False

    return True


def check_key(key):
    try:
        int(key)
        return True
    except ValueError:
        return False


def main():
    plaintext = ''

    if len(sys.argv) != 2 or not check_key(sys.argv[1]):
        print('Usage: python caesar.py k')
        exit(1)

    key = int(sys.argv[1])

    while not check_text(plaintext):
        plaintext = str(input("plaintext: "))

    result = encrypt(plaintext, key)

    print(f"ciphertext: {result}")


if __name__ == '__main__':
    main()
