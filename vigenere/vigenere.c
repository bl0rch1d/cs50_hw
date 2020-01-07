#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>

const int MAX_ARGS = 2;
const int STRING_MAX_LENGTH = 50;
const char ERR_MSG[] = "Usage: ./vigenere keyword\n";
const int CONVERTATION_INDEX = 97;
const int ALPHA_ASCII_SHIFT = 26;

bool check_args_quantity(int x);
bool validate_key(char *key);
int convert_to_shift(char chr);
char * get_plaintext(void);
char * encrypt(char *key, char *plaintext);

int main(int argc, char *argv[]) {
  char *key = argv[1];

  if (!check_args_quantity(argc)) {
    printf("%s", ERR_MSG);
    return 1;
  }

  if (!validate_key(key)) {
    printf("%s", ERR_MSG);
    return 1;
  }

  char *plaintext = get_plaintext();
  char *result = encrypt(key, plaintext);

  printf("ciphertext: %s\n", result);
}

// Check that args are equal to 2
bool check_args_quantity(int x) {
  return x == MAX_ARGS;
}

// Check that all elements in string are numbers
bool validate_key(char *key) {
  int i = 0;

  while (key[i] != '\0') {
    if (!isalpha(key[i])) return false;

    i++;
  }

  return true;
}

// Convert character to shift
int convert_to_shift(char chr) {
  return (int) tolower(chr) - CONVERTATION_INDEX;
}

// Get plain text from user
char *get_plaintext(void) {
  char *plaintext = malloc(STRING_MAX_LENGTH * sizeof(char));

  printf("plaintext: ");
  scanf("%[^\n]%*c", plaintext);

  return plaintext;
}

// Encrypt
char * encrypt(char *key, char *plaintext) {
  int shift;
  char current_char;
  int kc = 0;
  int shifted_code;

  // Calculate lenght of string entered by user
  size_t str_len = strlen(plaintext);

  // Calculate size of length
  size_t key_len = strlen(key);

  // Define result array 
  char *result = malloc(str_len * sizeof(char));

  for (int i = 0; i <= str_len; i++) {
    current_char = plaintext[i];

    if (!isalpha(current_char)) {
      result[i] = current_char;
    } else {
      shift = convert_to_shift(key[kc]);
      shifted_code = current_char + shift;

      if (islower(current_char) && shifted_code > 122 || isupper(current_char) && shifted_code > 90) {
        shifted_code = shifted_code - 26;
      }

      result[i] = (char) shifted_code;
      kc++;

      if (kc > key_len - 1) kc = 0;
    }
  }

  return result;
}
