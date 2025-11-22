#ifndef HEADERS_H_INCLUDED
#define HEADERS_H_INCLUDED

#include <stdio.h>
#include <stdlib.h>

typedef struct cell
{
    int value;
    struct cell* next;
} cellule;

void initialize_list(cellule**, int);
void add_head(cellule**, int);
void concatenate_two_lists(cellule**, cellule**, cellule**);
void read_list(cellule*);



#endif // HEADERS_H_INCLUDED
