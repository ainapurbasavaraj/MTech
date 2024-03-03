#include<stdio.h>
#include<stdatomic.h>
#include<stdlib.h>

//the node type in the stack
typedef struct _Node
{
    int data;
    struct _Node* next;
}Node;
//the stack
typedef struct _lfstack_t
{
    Node *head;
}lfstack_t;

//the push function
void lfstack_push(_Atomic lfstack_t *lfstack, int value)
{
    lfstack_t next;
    lfstack_t orig = atomic_load(lfstack); //here we need a local copy of lfstack, however, lfstack is a pointer
                                           //we could not get the content from a struct pointer atomically by assignment
                                           //C11 provides us a function for us to atomically get the content from the location that 
                                           //a atomic type pointer points to.
    Node *node = malloc(sizeof(Node)); //the new node, step 1
    node->data = value;
    do{
        node->next = orig.head; //step 2
        next.head = node; //local change of head
    }while(!atomic_compare_exchange_weak(lfstack,&orig,next)); //if the lfstack is not changed by others, apply the local change of head to it
	
}

//pop function
int lfstack_pop(_Atomic lfstack_t *lfstack)
{
    lfstack_t next;
    lfstack_t orig = atomic_load(lfstack);
    do{
        if(orig.head == NULL) //return when the stack is empty
        {
            return -1;
        }
        next.head = orig.head->next; //set the head to the next node
    }while(!atomic_compare_exchange_weak(lfstack,&orig,next)); //if the head of stack is not changed, update the stack
    printf("poping value %d\n",orig.head->data); //just want to see the poping value.
    free(orig.head); // free the poping node
    return 0;
}