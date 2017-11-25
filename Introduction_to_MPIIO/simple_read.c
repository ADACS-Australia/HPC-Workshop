/*
 * This is a simple example program demonstrating how to do
 * file per process I/O with MPI-IO. Each MPI process first
 * writes to its a row in its own file. Every process then 
 * reads from each a column entry from each row.
 */


#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>


int main (int argc , char* argv[])
{

	/* Initialize MPI*/
	MPI_Init(&argc,&argv);
	int rank, nprocs;
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&nprocs);
	MPI_Status status;

	int data_r[nprocs];
	int i;

	/* Initialize the data buffer to write in the file*/
	for (i=1; i<=nprocs; i++){
		data_r[i-1]=0;
	}

	/* Declaring MPI file pointer/handle*/
	MPI_File fh;
	char filename[256];
	sprintf(filename,"simple.data");

	/* All MPI processes must call file_open with correct amode.*/
	MPI_File_open(MPI_COMM_WORLD,filename,MPI_MODE_RDONLY, MPI_INFO_NULL,&fh);

	/* All MPI processes must set their view of the file where they are going to write
	 * their share of data*/
	// displacemnet will be offset by number of bytes written by (rank-1) process
	MPI_Offset disp = rank * nprocs * sizeof(int);
	printf("%d: %ld\n",rank,disp);
	// Since we are writing interger, then
	MPI_Datatype etype=MPI_INT, filetype=MPI_INT;
	char data_rep[64];
	sprintf(data_rep,"native");	
	MPI_File_set_view(fh,disp,etype,filetype,data_rep, MPI_INFO_NULL);

	// Now that all MPI processes have a view of the shared file, each can write into its space in file.
	MPI_File_read(fh,data_r,nprocs,MPI_INT, &status);

	MPI_File_close(&fh);

	// Lets print what we got.
	printf("[%d] %d %d %d %d \n",rank,data_r[0],data_r[1],data_r[2],data_r[3]);

	MPI_Finalize();
}
