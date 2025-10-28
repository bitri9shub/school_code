#ifndef HEADERS_H_INCLUDED
#define HEADERS_H_INCLUDED
#include <stdio.h>
#include <stdlib.h>

typedef struct cell
{
    int value;
    struct cell* next;
} cellule;

cellule* initialize_cell(int);
cellule* add_head(cellule*,int);
cellule* add_tail(cellule*, int);
void read_cell(cellule*);
void read_list(cellule*);


#endif // HEADERS_H_INCLUDED
