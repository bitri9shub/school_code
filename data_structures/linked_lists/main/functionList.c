#include "headers.h"

// Passage par valeurs

cellule* initialize_cell_by_value(int v)
{
    cellule* new_cell;
    new_cell = (cellule*) malloc(sizeof(cellule));
    new_cell->value = v;
    new_cell->next = NULL;
    return new_cell;
}

cellule* add_head_by_value(cellule* head, int v)
{
    cellule* new_cell = initialize_cell_by_value(v);
    new_cell->next = head;
    head = new_cell;
    return head;
}

cellule* add_tail_by_value(cellule* head, int v)
{
    cellule* temp_head = head;
    while(head->next != NULL)
    {
        head = head->next;
    }
    cellule* new_cell = initialize_cell_by_value(v);
    head->next = new_cell;
    return temp_head;
}

int search_index_by_value(cellule* head, int v)
{
    int count = 0;
    while(head != NULL)
    {
        count++;
        if(head->value == v)
        {
            return count;
        }else if (head->next != NULL)
        {
            head = head->next;
        }else
        {
            return -1;
        }
    }
}

cellule* delete_cell_value_by_value(cellule* head, int v)
{
    cellule* temp_head = head;
    int isCellExists = search_index_by_value(head, v);
    if(isCellExists != -1)
    {
        while(head->next != NULL)
        {
            if(head->next->value == v)
            {
                head->next = head->next->next;
            }
            head = head->next;
        }
    }
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

// Passage par adresse
void initialize_cell_by_address(cellule** new_cell, int v)
{
    *new_cell = (cellule*) malloc(sizeof(cellule));
    (*new_cell)->value = v;
    (*new_cell)->next = NULL;
}
//

void add_head_by_address(cellule** head, int v)
{
    cellule* new_cell;
    initialize_cell_by_address(&new_cell, v);
    new_cell->next = *head;
    *head = new_cell;
}
