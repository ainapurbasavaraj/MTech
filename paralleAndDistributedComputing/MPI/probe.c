#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){

	int rank;
	int size;
	MPI_Init(NULL, NULL);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	if (rank == 0){
		int MAX = 100;
		int numbers[MAX];

		srand(time(NULL));
    		int number_amount = (rand() / (float)RAND_MAX) * MAX;
		MPI_Send(numbers, number_amount,MPI_INT, 1, 0, MPI_COMM_WORLD);
	}
	else if (rank == 1){
		MPI_Status status;

		MPI_Probe(0, 0, MPI_COMM_WORLD, &status);

		int count;
		MPI_Get_count(&status, MPI_INT, &count);

		int *buf = (int*)malloc(sizeof(int)*count);
		MPI_Recv(buf,count,MPI_INT, 0 , 0, MPI_COMM_WORLD, &status);

		printf("Received %d count from process %d and tag %d\n", count, status.MPI_SOURCE, status.MPI_TAG);

		free(buf);
	}

	MPI_Finalize();
}
