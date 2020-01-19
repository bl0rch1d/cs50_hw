#include <stdio.h>
#include <cs50.h>
#include <math.h>

#define cent25 25
#define cent10 10
#define cent5 5
#define cent1 1

int main() {
  float amount;
  int coins;

  int a = 0;
  int b = 0;
  int c = 0;
  int d = 0;

  int result;

  amount = get_float("Enter amount: ");

  coins = round(amount * 100);

  while (coins - cent25 >= 0) {
    coins = coins - cent25;
    a++;
  }

  while (coins - cent10 >= 0) {
    coins = coins - cent10;
    b++;
  }

  while (coins - cent5 >= 0) {
    coins = coins - cent5;
    c++;
  }

  while (coins - cent1 >= 0) {
    coins--;
    d++;
  }

  result = a + b + c + d;

  printf("%d\n", result);
}
