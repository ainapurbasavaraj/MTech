#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

#define N 3
#define MAX_NUM 10

void mtxMul(int c[][N], int a[][N], int b[][N], int n) {
#pragma omp parallel for collapse(2)
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            c[i][j] = 0;
            for (int k = 0; k < n; k++)
                c[i][j] += a[i][k] * b[k][j];
        }
    return;
}

void display(int result[][N], int n) {
    printf("\nOutput Matrix:\n");
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            printf("%d  ", result[i][j]);
            if (j == n - 1)
                printf("\n");
        }
    }
}

int main(int argc, char* argv[]) {
    int arr1[N][N], arr2[N][N], mult[N][N];
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            arr1[i][j] = rand() % MAX_NUM;
            arr2[i][j] = rand() % MAX_NUM;
        }
    }
    mtxMul(mult, arr1, arr2, N);
    display(arr1, N);
    display(arr2, N);
    display(mult, N);
    return 0;
}