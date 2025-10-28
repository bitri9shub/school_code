#include "headers.h"

int main()
{
    // Déclaration et initialisation de la tête
    cellule* head;
    head = initialize_cell(30);

    // Création des elements de la liste
    head = add_head(head, 20);
    head = add_head(head, 10);
    head = add_tail(head, 15);
    head = add_tail(head, 5);
    head = add_head(head, 1);

    // Affichage de la liste
    read_list(head);


    return 0;
}
