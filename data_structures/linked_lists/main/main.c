#include "headers.h"

int main()
{
    // Déclaration et initialisation de la tête
    cellule* head;
    int index;
    //head = initialize_cell_by_value(30);
    initialize_cell_by_address(&head, 30);

    // Opérations sur elements de la liste
    head = add_head_by_value(head, 20);
    head = add_head_by_value(head, 10);
    head = add_tail_by_value(head, 15);
    head = add_tail_by_value(head, 5);
    head = add_head_by_value(head, 1);
    index = search_index_by_value(head, 20);
    head = delete_cell_value_by_value(head, 15);
    head = delete_cell_value_by_value(head, 20);
    add_head_by_address(&head, 12);

    // Affichage de la liste
    read_list(head);

    // Affichage indice
    printf("index: %d", index);

    return 0;
}
