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
    node* new_leaf;
    if((*tree_header)->value > v)
    {
        if(!(*tree_header)->right_child)
        {
            tree_header = tree_header->right_child;
        } else
        {
            (*tree_header)->right_child = initialize_node(&new_leaf, v);
        }
    } else if ((*tree_header)->value < v)
    {
        if(!(*tree_header)->left_child)
        {
            tree_header = tree_header->left_child;
        } else
        {
            tree_header->left_child = initialize_node(&new_leaf, v);
        }
    }
}
