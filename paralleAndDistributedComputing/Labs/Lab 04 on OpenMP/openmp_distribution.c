#include <omp.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    long int max, sum = 0;
    sscanf(argv[1], "%ld", &max);
#pragma omp parallel for reduction (+:sum) schedule(runtime)
    for (int i = 1; i <= max; i++) {
        printf("%2d @ %d\n", i, omp_get_thread_num());
        sleep(i < 4 ? i + 1 : 1);
        sum += i;
    }
    printf("%ld\n", sum);
    return 0;
}