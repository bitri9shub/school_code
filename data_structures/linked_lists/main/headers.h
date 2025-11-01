#ifndef HEADERS_H_INCLUDED
#define HEADERS_H_INCLUDED
#include <stdio.h>
#include <stdlib.h>

typedef struct cell
{
    int value;
    struct cell* next;
} cellule;

cellule* initialize_cell_by_value(int);
cellule* add_head_by_value(cellule*,int);
cellule* add_tail_by_value(cellule*, int);
cellule* delete_cell_value_by_value(cellule*, int);
int search_index_by_value(cellule*, int);
void initialize_cell_by_address(cellule**, int);
void add_head_by_address(cellule**, int);
void read_cell(cellule*);
void read_list(cellule*);


#endif // HEADERS_H_INCLUDED
