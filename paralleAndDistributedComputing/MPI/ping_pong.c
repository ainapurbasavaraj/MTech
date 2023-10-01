#include <mpi.h>
#include <stdio.h>

int main(){

	int rank;
	int num_processor;

	MPI_Init(NULL, NULL); //Initialize MPI
	//MPI_COMM_WORLD - is the communicator
	//size is the number of communicators
	//rank is the number assigned to each communicator
	MPI_Comm_size(MPI_COMM_WORLD, &num_processor);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);	

	int ping_pong_count = 0;
	int PING_PONG_LIMIT = 5;
	int partner_rank = (rank + 1) % 2;
	printf("partner_rank %d\n " , partner_rank);
	while (ping_pong_count < PING_PONG_LIMIT){
		if (rank == ping_pong_count %2){
			ping_pong_count++;
			MPI_Send(&ping_pong_count, 1, MPI_INT, partner_rank, 0, MPI_COMM_WORLD);
			printf("%d sent an incremented ping_pong_count %d to %d\n", rank, ping_pong_count, partner_rank);
		}else{
			MPI_Recv(&ping_pong_count, 1, MPI_INT, partner_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			printf("%d received ping_pong_count %d from %d\n", rank, ping_pong_count, partner_rank);
		}
	}

	MPI_Finalize();
	return 0;
}
