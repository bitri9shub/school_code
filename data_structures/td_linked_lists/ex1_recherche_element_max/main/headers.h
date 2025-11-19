#ifndef HEADERS_H_INCLUDED
#define HEADERS_H_INCLUDED
#include <stdio.h>
#include <stdlib.h>

typedef struct cell
{
    int value;
    struct cell* next;
} cellule;

void initialize_cell(cellule**, int);
void read_list(cellule*);
void add_tail(cellule**, int);
int find_max_iterative(cellule*);
int find_max_recursive(cellule*);


#endif // HEADERS_H_INCLUDED
