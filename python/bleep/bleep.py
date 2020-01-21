import sys


def parse_dictionary(filename):
    result = []

    with open(filename, mode='r') as f:
        for word in f:
            result.append(word.strip())

    return result


def main():
    if len(sys.argv) != 2:
        print('Usage: python bleep.py dictionary')
        exit(1)

    dictionary = parse_dictionary(sys.argv[1])

    text = str(input('What message would you like to censor?\n'))

    for word in dictionary:
        replace_with = len(word) * '*'

        if word in text:
            text = text.replace(word, replace_with)
        elif word.upper() in text:
            text = text.replace(word.upper(), replace_with)

    print(text)


if __name__ == "__main__":
    main()
