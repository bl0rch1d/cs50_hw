#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

bool check_args_quantity(int x);
bool check_numericality(char x[]);

int main(int argc, char *argv[]) {
  char *key = argv[1];

  // Check that args are equal to 2
  if (argc > 2 ) {
    printf("Usage: ./caesar key\n");
    return 1;
  }

  // Check that all elements in string are numbers
  int i = 0;
  while (key[i] != '\0') {
    if ((int)key[i] < 47 || (int)key[i] > 58) {
      printf("Usage: ./caesar key\n");
      return 1;
    }

    i++;
  }

  // Convert key to int
  int shift = 0;
  for (int i = 0; i < strlen(key); i++) {
    shift += (key[i] - '0') * (int) pow(10, (strlen(key) - (i + 1)));
  }

  // Get plain text from user
  char plain_text[50];
  printf("plaintext: ");
  scanf("%[^\n]%*c", plain_text);

  // Calculate size of string entered by user
  size_t size = strlen(plain_text);

  // Encrypt
  char result[50];
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

  // Print encrypted message
  printf("ciphertext: %s\n", result);
}
