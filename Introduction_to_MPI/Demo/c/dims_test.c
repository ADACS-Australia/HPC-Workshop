#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]){

int rank,size,i;
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	int ndims=3;
	int* dims = (int*) malloc(ndims*sizeof(int));
	for (i=0; i<ndims; i++)
		dims[i]=0;	
	MPI_Dims_create(size, ndims, dims);
	if(rank==0)	
	for ( i=0; i<ndims; i++)
		printf("[%d] dim[%d]=%d  total_tasks=%d\n",rank,i,dims[i],size);
	MPI_Finalize();


}
