#include <omp.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    int max, sum = 0;
    sscanf(argv[1], "%d", &max);
#pragma omp parallel for
    for (int i = 1; i <= max; i++)
#pragma omp atomic
        sum += i;
    printf("%d\n", sum);
    return 0;
}