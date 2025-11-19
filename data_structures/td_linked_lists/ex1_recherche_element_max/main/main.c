#include "headers.h"

int main()
{
    // Déclaration et initialisation de la tête
    cellule* head;
    int list_max_iterative;
    int list_max_recursive;
    initialize_cell(&head, 10);

    // Ajout d'éléments à la liste
    add_tail(&head, 11);
    add_tail(&head, 12);
    add_tail(&head, 13);
    add_tail(&head, 15);
    add_tail(&head, 95);
    add_tail(&head, 35);
    add_tail(&head, 9);
    add_tail(&head, 72);

    // I. Recherche d'élément maximal

    // I.1 Approche itérative
    list_max_iterative = find_max_iterative(head);
    list_max_recursive = find_max_recursive(head);

    // I.2 Approche récursive


    // Lecture de la liste
    read_list(head);
    printf("(Iterative)Le maximum de la liste: %d\n", list_max_iterative);
    printf("(Recursive)Le maximum de la liste: %d", list_max_recursive);


    return 0;
}
