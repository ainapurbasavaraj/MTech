#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void* mutex_function();
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
int  counter = 0;

int main() {
    int rc1, rc2;
    int one = 1, two = 2;
    pthread_t thread1, thread2;

    if ((rc1 = pthread_create(&thread1, NULL, &mutex_function, (void*)&one))) {
        printf("Thread creation failed: %d\n", rc1);
    }

    if ((rc2 = pthread_create(&thread2, NULL, &mutex_function, (void*)&two))) {
        printf("Thread creation failed: %d\n", rc2);
    }

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    exit(0);
}

void* mutex_function(int* param) {
    pthread_mutex_lock(&mutex1);
    counter++;
    printf("I'm in thread id %d, Counter value: %d\n", *param, counter);
    pthread_mutex_unlock(&mutex1);
}