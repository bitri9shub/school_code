#include "headers.h"

void initialize_list(cellule** new_head, int v)
{
    *new_head = (cellule*) malloc(sizeof(cellule));
    (*new_head)->value = v;
    (*new_head)->next = NULL;
}

void add_head(cellule** head, int v)
{
    cellule* new_cell;
    initialize_list(&new_cell, v);
    new_cell->next = *head;
    *head = new_cell;
}

void concatenate_two_lists(cellule** concatenated_list, cellule** head_1, cellule** head_2)
{
    concatenated_list = head_1;
    while((*concatenated_list)->next != NULL)
    {
        *concatenated_list = (*concatenated_list)->next;
    }
    (*concatenated_list)->next = *head_2;
}

void read_list(cellule* head)
{
    do {
        printf("cellule:\n");
        printf("valeur: %d\n", head->value);
        printf("adresse du suivant: %p\n", head->next);
        printf("\n");
        head = head->next;
    } while (head != NULL);
}
