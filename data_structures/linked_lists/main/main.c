#include "headers.h"

int main()
{
    // D�claration et initialisation de la t�te
    cellule* head;
    head = initialize_cell(30);

    // Cr�ation des elements de la liste
    head = add_head(head, 20);
    head = add_head(head, 10);
    head = add_tail(head, 15);
    head = add_tail(head, 5);
    head = add_head(head, 1);

    // Affichage de la liste
    read_list(head);


    return 0;
}
