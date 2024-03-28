/*

For false sharing, since the wrong value being accessed is handled by the OS (through a dirty bit), we'll instead observe how constant back-and-forth (ping-pong) memory access slows down our program.

*/

#include <stdio.h> 
#include <pthread.h> 
#include <time.h>
#include <unistd.h>

int array[100];
#define NUM_ITER 100000000

void* func(void* param) {
    int index = *((int*)param);
    int i;
    for (i = 0; i < NUM_ITER; i++) {
        array[index] += 3;
    }

    return NULL;
}

void subtract_time(struct timespec t1, struct timespec t2, struct timespec* td) {
    td->tv_nsec = t2.tv_nsec - t1.tv_nsec;
    td->tv_sec = t2.tv_sec - t1.tv_sec;
    if (td->tv_sec > 0 && td->tv_nsec < 0) {
        td->tv_nsec += 1000000000;
        td->tv_sec--;
    }
    else if (td->tv_sec < 0 && td->tv_nsec > 0) {
        td->tv_nsec -= 1000000000;
        td->tv_sec++;
    }
}

int main(int argc, char* argv[]) {
    int       first_elem = 0;
    int       bad_elem = 1;
    int       good_elem = 32;
    pthread_t     thread_1;
    pthread_t     thread_2;

    struct timespec start, finish, delta_seq, delta_false, delta_true;
    clock_gettime(CLOCK_REALTIME, &start);
    func(&first_elem);
    func(&bad_elem);
    clock_gettime(CLOCK_REALTIME, &finish);
    subtract_time(start, finish, &delta_seq);

    clock_gettime(CLOCK_REALTIME, &start);
    pthread_create(&thread_1, NULL, func, (void*)&first_elem);
    pthread_create(&thread_2, NULL, func, (void*)&bad_elem);
    pthread_join(thread_1, NULL);
    pthread_join(thread_2, NULL);
    clock_gettime(CLOCK_REALTIME, &finish);
    subtract_time(start, finish, &delta_false);

    /* Just to show that parallel threads in best case *can* improve efficiency */
    clock_gettime(CLOCK_REALTIME, &start);
    pthread_create(&thread_1, NULL, func, (void*)&first_elem);
    pthread_create(&thread_2, NULL, func, (void*)&good_elem);
    pthread_join(thread_1, NULL);
    pthread_join(thread_2, NULL);
    clock_gettime(CLOCK_REALTIME, &finish);
    subtract_time(start, finish, &delta_true);

    printf("%d %d %d\n", array[first_elem], array[bad_elem], array[good_elem]);

    printf("Time taken for seq\t:%d.%.9lds\n", (int)delta_seq.tv_sec, delta_seq.tv_nsec);
    printf("Time taken for false\t:%d.%.9lds\n", (int)delta_false.tv_sec, delta_false.tv_nsec);
    printf("Time taken for true\t:%d.%.9lds\n", (int)delta_true.tv_sec, delta_true.tv_nsec);
    return 0;
}
