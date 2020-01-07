#include <crypt.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

const char *POSSIBLE_PASSWORDS[] = { "qwert", "12345", "1234", "lol", "kek", "super", "passw"  };
const int MAX_ARGS = 2;
const int SALT_LEN = 2;
const int HASH_LEN = 13;
const char ERR_MSG[] = "Usage: ./crack hash\n";

bool check_args_quantity(int q);

int main(int argc, char *argv[]) {
  if (!check_args_quantity(argc)) {
    printf("%s", ERR_MSG);
    return 1;
  }

  // Parse salt
  char salt[SALT_LEN] = { argv[1][0], argv[1][1] };

  // Parse hash
  char *hash = argv[1];

  // Initialize array for hashed possible password storage
  char hashed[HASH_LEN];
  
  for (int i = 0; i < strlen(*POSSIBLE_PASSWORDS); i++) {
    strcpy(hashed, crypt(POSSIBLE_PASSWORDS[i], salt));

    printf("[-] Trying: %s\n", POSSIBLE_PASSWORDS[i]);

    if (strcmp(hash, hashed) == 0) {
      printf("[+] Found: %s\n", POSSIBLE_PASSWORDS[i]);
      return 0;
    }
  }

  return 0;
}

// Check that arg quantity are valid
bool check_args_quantity(int x) {
  return x == MAX_ARGS;
}
