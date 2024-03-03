#include <stdio.h>
#include <pthread.h>

void* function_write();
void* function_read();
FILE* fptr;
pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;

int main() {
    int rc1, rc2;
    fptr = fopen("./mutex.txt", "w");
    fprintf(fptr, "The Answer to the Ultimate Question of Life, the Universe, and Everything is: ??");
    fclose(fptr);
    pthread_t thread1, thread2;
    int one = 1, two = 2;

    if ((rc1 = pthread_create(&thread1, NULL, &function_write, (void*)&one))) {
        printf("Thread creation failed: %d\n", rc1);
    }
    pthread_join(thread1, NULL);
    if ((rc2 = pthread_create(&thread2, NULL, &function_read, (void*)&two))) {
        printf("Thread creation failed: %d\n", rc2);
    }
    pthread_join(thread2, NULL);
    return 0;
}

void* function_write(void* param) {
    pthread_mutex_lock(&mtx);
    fptr = fopen("./mutex.txt", "a");
    fprintf(fptr, "\b\b42.\n");
    fclose(fptr);
    pthread_mutex_unlock(&mtx);
}

void* function_read(void* param) {
    pthread_mutex_lock(&mtx);
    fptr = fopen("./mutex.txt", "r");
    char dataToRead[50];
    while (fgets(dataToRead, 50, fptr) != NULL) {
        printf("%s", dataToRead);
    }
    fclose(fptr);
    pthread_mutex_unlock(&mtx);
}