#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>

#include "bmp.h"

const int ARGS_COUNT = 4;
const char ERR_MSG[] = "Usage: resize multiplier infile outfile\n";

bool check_args_quantity(int x);
bool check_numericality(char *x);
int to_int(char *resize_value);

int main(int argc, char *argv[]) {
    if (!check_args_quantity(argc)) {
        fprintf(stderr, ERR_MSG);
        return 1;
    }

    char *resize_arg = argv[1];

    if (!check_numericality(resize_arg)) {
        fprintf(stderr, ERR_MSG);
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // resize factor
    int resize_value = to_int(resize_arg);

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL) {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL) {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // pixels storage
    RGBTRIPLE triple[abs(bi.biHeight) * bi.biWidth];

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // iterate over infile's scanlines
    int read_counter = 0;
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // read RGB triple from infile
            fread(&triple[read_counter], sizeof(RGBTRIPLE), 1, inptr);
            read_counter++;
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    // Update headers
    bi.biSizeImage *= resize_value;
    bi.biHeight *= resize_value;
    bi.biWidth *= resize_value;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // null_bytes count per line
    int null_bytes = resize_value * padding % 4;

    // iterate over infile's scanlines
    int write_counter = 0;
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++) {
        if (i % resize_value != 0) write_counter -= bi.biWidth / resize_value;

        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++) {
            if (j % resize_value == 0 && j != 0) write_counter++;

            fwrite(&triple[write_counter], sizeof(RGBTRIPLE), 1, outptr);
        }

        write_counter++;

        // Write padding
        for (int k = 0; k < null_bytes; k++) fputc(0x00, outptr);
    }

    fclose(inptr);
    fclose(outptr);

    return 0;
}

// Convert key to int
int to_int(char *resize_value) {
  int result = 0;

  for (int i = 0; i < strlen(resize_value); i++) {
    result += (resize_value[i] - '0') * (int) pow(10, (strlen(resize_value) - (i + 1)));
  }

  return result;
}

// Check that args count are equal to ARGS_COUNT
bool check_args_quantity(int x) {
  return x == ARGS_COUNT;
}

// Check that all elements in string are numbers
bool check_numericality(char *x) {
  for (int i = 0; i < strlen(x); i++) {
    if (!isdigit(x[i])) return false;
  }

  return true;
}
