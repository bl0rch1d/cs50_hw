#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

const int STRING_MAX_LENGTH = 50;

bool check_args_quantity(int x);
bool check_numericality(char *x);
int to_int(char *key);
char * get_plaintext(void);
char * encrypt(int shift, int size, char *plain_text);

int main(int argc, char *argv[]) {
  char *key = argv[1];

  if (!check_args_quantity(argc)) {
    printf("Usage: ./caesar key\n");
    return 1;
  }

  if (!check_numericality(argv[1])) {
    printf("Usage: ./caesar key\n");
    return 1;
  }

  int shift = to_int(key);
  char *plain_text = get_plaintext();

  // Calculate size of string entered by user
  size_t size = strlen(plain_text);

  char *result = encrypt(shift, size, plain_text);

  // Print encrypted message
  printf("ciphertext: %s\n", result);
}

// Check that args are equal to 2
bool check_args_quantity(int x) {
  return x == 2;
}

// Check that all elements in string are numbers
bool check_numericality(char *x) {
  int i = 0;
  while (x[i] != '\0') {
    if ((int) x[i] < 48 || (int) x[i] > 57) return false;

    i++;
  }

  return true;
}

// Convert key to int
int to_int(char *key) {
  int shift = 0;
  for (int i = 0; i < strlen(key); i++) {
    shift += (key[i] - '0') * (int) pow(10, (strlen(key) - (i + 1)));
  }

  return shift;
}

// Get plain text from user
char *get_plaintext(void) {
  char *plain_text = malloc(STRING_MAX_LENGTH * sizeof(char));
  printf("plaintext: ");
  scanf("%[^\n]%*c", plain_text);

  return plain_text;
}

// Encrypt
char * encrypt(int shift, int size, char *plain_text) {
  char *result = malloc(STRING_MAX_LENGTH * sizeof(char));

  for (int j = 0; j < size + 1; j++) {
    char c = plain_text[j];

    if (c >= 'a' && c <= 'z') {
       c += shift;

      if (c > 'z') c = c - 'z' + 'a' - 1;

      result[j] = c;
    } else if (c >= 'A' && c <= 'Z') {
      c += shift;

      if (c > 'Z') c = c - 'Z' + 'A' - 1;

      result[j] = c;
    } else {
      result[j] = c;
    }
  }

  return result;
}
