#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdlib.h>

typedef uint8_t BYTE;

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[]) {
  // Filename for reading
  char *infile = argv[1];

  // Open file for reading
  FILE *inptr = fopen(infile, "rb");

  // Count length of file to read
  fseek(inptr, 0L, SEEK_END);
  int filesize = ftell(inptr);
  rewind(inptr);

  int file = 0;
  int image_counter = 0;
  FILE *img;
  for (int i = 0; i < (filesize / BLOCK_SIZE); i++) {
    // Initialize and read block of file
    BYTE *block = malloc(BLOCK_SIZE);
    fread(block, BLOCK_SIZE, 1, inptr);

    // Check if block includes a JPEG headers
    if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0) {
      file++;
      image_counter++;

      // Create and open file for new image
      char filename[10];
      sprintf(filename, "%03i.jpg", image_counter);
      img = fopen(filename, "w");
    }

    // Write data to image file
    if (file > 0) fwrite(block, BLOCK_SIZE, 1, img);

    free(block);
  }

  fclose(inptr);
}
