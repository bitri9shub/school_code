#include "headers.h"

void initialize_cell(cellule** new_cell, int v)
{
    *new_cell = (cellule*) malloc(sizeof(cellule));
    (*new_cell)->value = v;
    (*new_cell)->next = NULL;
}

void add_tail(cellule** head, int v)
{
    cellule* temp = *head;

    while((*head)->next != NULL)
    {
        *head = (*head)->next;
    }
    cellule* new_cell;
    initialize_cell(&new_cell, v);
    (*head)->next = new_cell;
    *head = temp;
}

int find_max_iterative(cellule* head)
{
    int max;
    max = head->value;
    do {
        if(head->value > max)
        {
            max = head->value;
        }
        head = head->next;
    } while (head != NULL);
    return max;
}

int find_max_recursive(cellule* head)
{
    if (head->next == NULL) {
        return head->value;
    }

    int max_reste = find_max_recursive(head->next);

    if (head->value > max_reste) {
        return head->value;
    } else {
        return max_reste;
    }
}

void read_list(cellule* head)
{
    do {
        printf("cellule:\n");
        printf("valeur: %d\n", head->value);
        printf("adresse suivant: %p\n", head->next);
        printf("\n");
        head = head->next;
    } while(head != NULL);
}
