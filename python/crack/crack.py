import sys
import hashlib

POSSIBLE_PASSWORDS = [
    'password',
    'passwd',
    'qwerty',
    'lol',
    'kek',
    '12345',
    'admin',
    'root'
]


def check_hash(hash_str):
    if len(hash_str) == 0:
        return False

    for char in hash_str:
        if not char.isalpha() and not char.isdigit():
            return False

    return True


def crack(hash_str):
    for password in POSSIBLE_PASSWORDS:
        if hashlib.md5(str(password).encode()).hexdigest() == hash_str:
            return password
    return False


def main():
    if len(sys.argv) != 2 or not check_hash(sys.argv[1]):
        print('Usage: python crack.py hash')
        exit(1)

    result = crack(sys.argv[1])

    if result:
        print(f'Found: {result}')
    else:
        print('No matches found')


if __name__ == '__main__':
    main()
