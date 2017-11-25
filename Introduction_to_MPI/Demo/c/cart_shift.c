#include<mpi.h>
#include <stdio.h>
#define TRUE 1
#define FALSE 0
int main(int argc, char *argv[]) {
	int rank;
	MPI_Init(&argc, &argv); 
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);

	MPI_Comm vu;			//New communicator name 
	int 	dim[2],  		//Number of dimensions
		period[2],		//The preiodicity boolean on each director
		reorder,coords[2];	//Place holders to record reordered ranks and coordinates in new Cartisian communicator
	int up,down,right,left;		//Record nearest neighbours


	dim[0]=4; dim[1]=4;
	period[0]=TRUE; period[1]=FALSE;
	reorder=TRUE;

	MPI_Cart_create(MPI_COMM_WORLD,2,dim,period,reorder,&vu); 		//Communicator constructor
	MPI_Cart_shift(vu,0,1,&up,&down);					//Shift and record ranks an 0 dimension
	MPI_Cart_shift(vu,1,1,&left,&right);					//Shift and record ranks in 1 dimension
	MPI_Cart_coords (vu, rank, 2,coords);					//Get my Cartisian coordinates 	
	printf("P:%d My neighbors are r: %d d:%d l:%d u:%d coords=(%d,%d)\n",rank,right,down,left,up,coords[0],coords[1]);
	MPI_Finalize();
}
