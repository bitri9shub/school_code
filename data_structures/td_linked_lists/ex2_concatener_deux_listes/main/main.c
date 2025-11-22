#include "headers.h"

int main()
{
    cellule* head_1;
    initialize_list(&head_1, 30);
    add_head(&head_1, 35);
    add_head(&head_1, 40);
    // read_list(head_1);

    cellule* head_2;
    initialize_list(&head_2, 10);
    add_head(&head_2, 15);
    add_head(&head_2, 20);
    // read_list(head_2);

    cellule* concat_list;
    concatenate_two_lists(&concat_list, &head_1, &head_2);
    read_list(concat_list);


    return 0;
}
