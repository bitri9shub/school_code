#include "headers.h"

// Passage par valeurs

cellule* initialize_cell(int v)
{
    cellule* new_cell;
    new_cell = (cellule*) malloc(sizeof(cellule));
    new_cell->value = v;
    new_cell->next = NULL;
    return new_cell;
}

cellule* add_head(cellule* head, int v)
{
    cellule* new_cell = initialize_cell(v);
    new_cell->next = head;
    head = new_cell;
    return head;
}

cellule* add_tail(cellule* head, int v)
{
    cellule* temp_head = head;
    while(head->next != NULL)
    {
        head = head->next;
    }
    cellule* new_cell = initialize_cell(v);
    head->next = new_cell;
    return temp_head;
}

void read_cell(cellule* cell)
{
    printf("cellule:\n");
    printf("valeur: %d\n", cell->value);
    printf("adresse: %p\n", cell->next);
    printf("\n");
}

void read_list(cellule* head)
{
    do {
        printf("cellule:\n");
        printf("valeur: %d\n", head->value);
        printf("adresse: %p\n", head->next);
        printf("\n");
        head = head->next;
    }
    while(head != NULL);
}
