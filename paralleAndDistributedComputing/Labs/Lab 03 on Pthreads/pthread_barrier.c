#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>

void* wait_thread(void* param);
typedef struct mylib_barrier_t mylib_barrier_t;
void mylib_init_barrier(mylib_barrier_t* b);
void mylib_barrier(mylib_barrier_t* b, int num_threads);

#define NTHREAD 2


struct mylib_barrier_t {
    pthread_mutex_t count_lock;
    pthread_cond_t ok_to_proceed;
    int count;
};

mylib_barrier_t myBarrier;
int t[NTHREAD];

int main(int argc, char const* argv[]) {
    pthread_t threadArr[NTHREAD];
    int threadIdArr[NTHREAD];
    for (int j = 0; j < NTHREAD; j++) {
        threadIdArr[j] = j;
    }

    mylib_init_barrier(&myBarrier);

    int i = 0;
    for (i = 0; i < NTHREAD; i++) {
        pthread_create(&threadArr[i], NULL, &wait_thread, &threadIdArr[i]);
    }

    for (int j = 0; j < NTHREAD; ++j) {
        pthread_join(threadArr[j], NULL);
    }

    return 0;
}

void* wait_thread(void* param) {
    int threadId = *(int*)param;
    int sleepTime = (threadId + 1) * 2;
    printf("Thread %d will perform computation for %ds.\n", threadId, sleepTime);
    sleep(sleepTime);
    t[threadId] = (threadId + 1) * 10;
    mylib_barrier(&myBarrier, NTHREAD);

    pthread_mutex_t printMutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_mutex_lock(&printMutex);
    printf("At threadId %d, value of: ", threadId);
    for (int i = 0; i < NTHREAD; i++) {
        printf("t%d = %d, ", i, t[i]);
    }
    printf("\n");
    pthread_mutex_unlock(&printMutex);

    return NULL;
}


void mylib_init_barrier(mylib_barrier_t* b) {
    b->count = 0;
    pthread_mutex_init(&(b->count_lock), NULL);
    pthread_cond_init(&(b->ok_to_proceed), NULL);
}

void mylib_barrier(mylib_barrier_t* b, int num_threads) {
    pthread_mutex_lock(&(b->count_lock));
    b->count++;
    if (b->count == num_threads) {
        b->count = 0;
        pthread_cond_broadcast(&(b->ok_to_proceed));
    }
    else
        while (pthread_cond_wait(&(b->ok_to_proceed), &(b->count_lock)) != 0);
    pthread_mutex_unlock(&(b->count_lock));
}