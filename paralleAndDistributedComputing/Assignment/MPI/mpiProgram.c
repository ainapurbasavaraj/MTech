// Instructions
// compilation:  mpicc P1.c -o P1
// execution:  mpiexec -n 10 ./P1

#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv)
{
	int N;
    int rank;
	MPI_Init(NULL, NULL); //Initialize MPI
	
	MPI_Comm_size(MPI_COMM_WORLD, &N); //Initialize Num process

	// Process rank
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	
	// Assume process is non neutral
	int neutral = 0;
	
	// Processes work in 500 iterations.
    const int iterations = 500;
	for(int iteration = 0; iteration < iterations; iteration++)
	{
		// even iteration
		if(iteration%2 == 0)
		{
			// When a process receives many numbers in even iteration, it will
			// pickup the highest number
			int highest = -1;
			
			// a process i sends i to all processes.  
			for(int j = 0 ; j < N; j++)
			{
				// process i sends i to j and receives j from process j
				int rdata;
				MPI_Sendrecv(&i, 1, MPI_INT, j, 0, 
				             &rdata, 1, MPI_INT, j, 0,
							 MPI_COMM_WORLD, MPI_STATUS_IGNORE);

				// check for non neutral process
				if(neutral == 0)
				{
					//  pickup the highest number				
					if(rdata > highest)
						highest = rdata;
				}					
			}
			
			// check for non neutral process
			if(neutral == 0)
			{
				//if that number equals its own, it will not participate in the 
				//subsequent iterations. Such processes are called neutral processes.			
				if(highest == i)
				{
					printf("Iteration %03d(even) - Process %03d: Marked as neutral process as highest number %d equals to its own %d\n", iteration, i, highest, i);
					neutral = 1;
				}
			}
		}
		// During odd iterations
		else
		{
			// a process i sends i to its i+1 neighbhour. 
			// and receives i-1 from its i-1 neighbhour
			int rdata;
			MPI_Sendrecv(&i, 1, MPI_INT, (i+1)%N, 0, 
						 &rdata, 1, MPI_INT, (i-1+N)%N, 0,
						 MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			
			// check for non neutral process
			int sdata;
			if(neutral == 0)
			{
				// when a process receives zero, that process will become netral 
				// process.
				if(rdata == 0)
				{
					printf("Iteration %03d( odd) - Process %03d: Marked as neutral process as received data is %d\n", iteration, i, rdata);
					neutral = 1;
				}
				else
				{
					// Each process i subtracts one from the number it received
					// from the previous process
					sdata = rdata - 1;	
				}				
			}
							
			// Neutral processes will not subtract the number 
			if(neutral)
				sdata = rdata;
						 
			// sends to the next one i.e. i+1 process.
			MPI_Sendrecv(&sdata, 1, MPI_INT, (i+1)%N, 0, 
						 &rdata, 1, MPI_INT, (i-1+N)%N, 0,
						 MPI_COMM_WORLD, MPI_STATUS_IGNORE);
						 
			if(neutral == 0)
			{
				// when a process receives zero, that process will become netral 
				// process.
				if(rdata == 0)
				{
					printf("Iteration %03d( odd) - Process %03d: Marked as neutral process as received data is %d\n", iteration, i, rdata);
					neutral = 1;
				}
			}								 
		}		
	}	
	
	MPI_Finalize();
	return 0;
}

