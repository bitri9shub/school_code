/*
    Binary search tree
*/

#include "headers.h"

int main()
{
    node* leaf;

    // Initialize a tree
    initialize_node(&leaf, 15);
    printf("%d %p %p\n", leaf->value, leaf->right_child, leaf->left_child);


    // Insert element to a tree
    insert_node(&leaf, 20);
    insert_node(&leaf, 9);
    printf("%d %d %d", leaf->value, leaf->right_child->value, leaf->left_child->value);

    // Search for an element in a tree
    // Remove element in a tree
    return 0;
}
