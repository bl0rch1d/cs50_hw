#include <stdio.h>
#include <cs50.h>

void pyramid_generator(int h) {
  for (int i = 1; i <= h; i++) {
    int left = 1;
    int right = 1;
    int indent = h - i;

    // Print identation
    for (int s = 0; s < indent; s++) {
      printf(" ");
    }

    // Print left side layer
    while (left <= i) {
      printf("#");

      left++;
    }

    // Set whitespace
    printf(" ");

    // Print right side layer
    while (right <= i) {
      printf("#");

      right++;
    }

    // Set enter
    printf("\n");
  }
}

int get_height(void) {
  int h = 0;

  while (h <= 0 || h > 8) {
    h = get_int("Enter height: ");
  }

  return h;
}

void main() {
  int height = get_height();
  pyramid_generator(height);
}
