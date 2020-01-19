#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main() {
  long number, n;
  int i = 0;
  bool valid;

  number = get_long("Enter card number: ");

  n = number;
  while (n != 0) {
    n /= 10;
    i++;
  }

  int arr[i];

  n = number;
  while (n != 0) {
    i--;
    arr[i] = n % 10;
    n /= 10;
  }

  size_t arr_len = sizeof(arr) / sizeof(arr[0]);
  int a = 0;
  
  for (int j = 0; j < arr_len; j++) {
    if (j % 2 == 0) {
      int t = arr[j] * 2;
      while (t != 0) {
        a += t % 10;
        t /= 10;
      }
    }
  }

  int b = 0;
  for (int j = 0; j < arr_len; j++) {
    if (j % 2 != 0) {
      b += arr[j];
    }
  }

  int result = a + b;

  if (result % 10 == 0) {
    valid = true;
  }

  char brand[50];
  switch (arr_len) {
    case 15:
      if ((arr[0] + arr[1] == 7) || (arr[0] + arr[1] == 10)) {
        strcpy(brand, "AMEX");
        break;
      }
    case 16:
      if ((arr[0] + arr[1] == 6) || (arr[0] + arr[1] == 7) || (arr[0] + arr[1] == 8) || (arr[0] + arr[1] == 9) || (arr[0] + arr[1] == 10)) {
        strcpy(brand, "MASTERCARD");
        break;
      }
    case 13 || 16:
      if (arr[0] == 4) {
        strcpy(brand, "VISA");
        break;
      }
  }

  if (valid) {
    printf("%s\n", brand);
  } else {
    printf("INVALID\n");
  }
}
