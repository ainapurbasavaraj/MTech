#include <mpi.h>
#include <stdio.h>

int main(){

	int rank;
	int size;
	MPI_Init(NULL, NULL);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD,  &rank);

	int token = -1;
	if (rank != 0){
		MPI_Recv(&token, 1, MPI_INT, rank-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		printf("Recieved from %d\n", rank-1);
	}

	MPI_Send(&token, 1 , MPI_INT, (rank+1) % size, 0, MPI_COMM_WORLD);
	if (rank == 0){
		MPI_Recv(&token, 1, MPI_INT, size-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		printf("Recieved from %d\n", size-1);
	}

	MPI_Finalize();
	return 0;
}
