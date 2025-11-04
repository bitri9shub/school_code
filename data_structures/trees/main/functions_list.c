#include "headers.h"

void initialize_node(node** new_node, int v)
{
    *new_node = (node*) malloc(sizeof(node));
    (*new_node)->value = v;
    (*new_node)->left_child = NULL;
    (*new_node)->right_child = NULL;
}

void insert_node(node** tree_header, int v)
{
    if(*tree_header == NULL)
    {
        initialize_node(tree_header, v);
        return;
    }

    if (v < (*tree_header)->value)
    {
        insert_node(&((*tree_header)->left_child), v);
    }
    else if (v > (*tree_header)->value)
    {
        insert_node(&((*tree_header)->right_child), v);
    }
}
