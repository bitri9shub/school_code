#ifndef HEADERS_H_INCLUDED
#define HEADERS_H_INCLUDED
#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int value;
    struct node* left_child;
    struct node* right_child;
} node;

void initialize_node(node**, int);
void insert_node(node*, int);

#endif // HEADERS_H_INCLUDED
