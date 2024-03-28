#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

int i;

void* thread_func() {
    //  int i = 0;
    while (1) {
        printf("child thread: %d\n", i++);
        sleep(1);
    }
}
int main() {
    pthread_t t1;
    pthread_create(&t1, NULL, thread_func, NULL);
    //int i = 0;
    while (1) {
        printf("main thread: %d\n", i++);
        sleep(1);
    }
}