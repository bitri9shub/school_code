#include <stdio.h>
#include <stdlib.h>

typedef struct cell
{
    int value;
    struct cell* next;
} cellule;

int main()
{
    // Declaration des cellules
    cellule* cell_1;
    cellule* cell_2;
    cellule* cell_3;

    // Allocation de mémoire pour les cellules
    cell_1 = (cellule*) malloc(sizeof(cellule));
    cell_2 = (cellule*) malloc(sizeof(cellule));
    cell_3 = (cellule*) malloc(sizeof(cellule));

    // Initialisation des variables pour les cellules
    cell_1->value = 10;
    cell_2->value = 20;
    cell_3->value = 110;

    // Initialisation des adresses vers les quelles pointes chaque cellule
    cell_1->next = NULL;
    cell_2->next = NULL;
    cell_3->next = NULL;

    // Lier les cellules
    cell_1->next = cell_2; // cell_2 retourne l'adresse du premier element de cell_2
    cell_2->next = cell_3; // cell_3 retourne l'adresse du premier element de cell_3

    // Affichage des cellules
    printf("Affichage cellule 1\n");
    printf("%d\n", cell_1->value);
    printf("%p\n", cell_1->next);

    printf("Affichage cellule 2\n");
    printf("%d\n", cell_2->value);
    printf("%p\n", cell_2->next);

    printf("Affichage cellule 1\n");
    printf("%d\n", cell_3->value);
    printf("%p\n", cell_3->next);



    return 0;
}
