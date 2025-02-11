// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

unsigned int words_count = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        int index = hash(word);

        node *new_node = malloc(sizeof(node));

        strncpy(new_node->word, word, sizeof(word));

        if (hashtable[index] != NULL) {
            new_node->next = hashtable[index];
        }

        hashtable[index] = new_node;

        words_count++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return words_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // int word_len = strlen(word);
    // char prepared_word[word_len + 1];

    // for (int i = 0; i < word_len; i++) {
    //     prepared_word[i] = tolower(word[i]);
    // }

    // TODO
    int index = hash(word);

    node *cursor = hashtable[index];

    while(cursor != NULL) {
        if (strcasecmp(cursor->word, word) != 0) {
            cursor = cursor->next;
        } else {
            return true;
        }
    }

    return false;
}

void destroy_node(node *node) {
    if (node->next != NULL) destroy_node(node->next);

    free(node);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++) {
        if (hashtable[i] != NULL) {
            destroy_node(hashtable[i]->next);
        }
    }

    return true;
}
