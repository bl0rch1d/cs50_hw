#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[]) {
  char *infile = argv[1];

  FILE *inptr = fopen(infile, "rb");
  int image_count = 0;

  fseek(inptr, 0L, SEEK_END);
  int filesize = ftell(inptr);
  rewind(inptr);

  int file = 0;
  FILE *img;
  for (int i = 0; i < 512 * 2; i++) {
    BYTE *test = malloc(512);

    fread(test, 512, 1, inptr);

    printf("\n====================================================================================== NEW BLOCK #%d ==============================================================================\n", i);
    for (int i = 0; i < 512; i++) {
      printf("0x%x\t", test[i]);
    }

    if (test[0] == 0xff && test[1] == 0xd8 && test[2] == 0xff && (test[3] & 0xf0) == 0xe0) {
      image_count++;
      sprintf(test, "%03i.jpg", image_count);
      img = fopen(test, "w");
      // file = 1;
    }

    fwrite(test, 512, 1, img);

    printf("\n====================================================================================================================================================================================\n");
    // free(test);
    // fclose(inptr);
  }

  printf("%d\n", image_count);

  // free(test);
  fclose(inptr);
}
