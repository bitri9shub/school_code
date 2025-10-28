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
    cellule* tete;
    cellule* cell_2;
    cellule* cell_3;
    // cellule* tête; Aulieu de définir la tête ensuite la lier avec la premiere cellule,
    // il suffit de prendre dès le départ la premiere cellule comme tête

    // Allocation de mémoire pour les cellules
    tete = (cellule*) malloc(sizeof(cellule));
    cell_2 = (cellule*) malloc(sizeof(cellule));
    cell_3 = (cellule*) malloc(sizeof(cellule));
    // tete = cell_1; // tete et cell_1 pointent vers le même bloc mémoire

    // Initialisation des variables pour les cellules
    tete->value = 10;
    cell_2->value = 20;
    cell_3->value = 110;

    // Initialisation des adresses vers les quelles pointes chaque cellule
    tete->next = NULL;
    cell_2->next = NULL;
    cell_3->next = NULL;

    // Lier les cellules
    tete->next = cell_2; // cell_2 retourne l'adresse du premier element de cell_2
    cell_2->next = cell_3; // cell_3 retourne l'adresse du premier element de cell_3

    // Affichage des cellules
    printf("Affichage cellule 1:\n");
    printf("valeur 1: %d\n", tete->value);
    printf("adresse 1: %p\n", tete->next);
    printf("\n");

    printf("Affichage cellule 2:\n");
    printf("valeur 2: %d\n", cell_2->value);
    printf("adresse 2: %p\n", cell_2->next);
    printf("\n");

    printf("Affichage cellule 3:\n");
    printf("valeur 3: %d\n", cell_3->value);
    printf("adresse 3: %p\n", cell_3->next);
    printf("\n");

    return 0;
}
