 #include "lf_stack.c"
 #include <stdio.h>
 #include <pthread.h>
 _Atomic lfstack_t top = {NULL};
 void *push(void *input)
 {
     for(int i=0; i<100; i++)
     {
         lfstack_push(&top, i);
         printf("push %d\n",i);
     }    
     pthread_exit(NULL);
 }

 void *pop(void *input)
 {
     for(int i=0; i<100;)
     {
         int result;
         result = lfstack_pop(&top);
         if(result == -1)
             printf("the stack is empty\n");
         else
         {
             i++;
         }

     }
     pthread_exit(NULL);
 }
 int main()
 {
     pthread_t tid[200];
     for(int i=0; i<100; i++)
         pthread_create(&tid[i],NULL,push,NULL);
     for(int i=100; i<200; i++)
         pthread_create(&tid[i],NULL,pop,NULL);
     for(int i=0; i<200; i++)
         pthread_join(tid[i],NULL);  
     return 0;
 }