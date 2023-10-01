#include <mpi.h>
#include <stdio.h>

int main(){
	
	int rank;
	int size;

	MPI_Init(NULL, NULL);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);

	char greetings[100] = "Hello from MPI";
	if (rank != 0){
		MPI_Send(greetings, strlen(greetings)+1, MPI_CHAR, 0, 0, MPI_COMM_WORLD);
		printf("Sent greeting from %d\n", rank);
	}else{
		for (int i=1; i<size; i++){
			MPI_Recv(greetings, 100, MPI_CHAR, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		       	printf("Received %s from %d\n", greetings,rank);
		}
	}

	MPI_Finalize();
	return 0;
}
