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

	/* Let's now read data from file. 
	 * Each rank reads a column from the file. 
	 * For this let's set the fileview for reading. 
	 * Though etype remains the same as we are reading integer, filtype will have a stride of 4 since we are reading columns.
	 * This can be done by constructing a derived a new datatype to use as filetype to set the file view.
	 * Since the offsets are going to be managed by newtype, each MPI process must read from the start, i.e. disp=0
	 */

	// displacemnet will be offset by number of bytes written by (rank-1) process
	MPI_Offset disp = 0;
	// Since we are writing interger, then
	MPI_Datatype etype,newtype;
	char data_rep[64];
	sprintf(data_rep,"native");	


	MPI_File_open(MPI_COMM_WORLD,filename,MPI_MODE_RDONLY, MPI_INFO_NULL,&fh);

	// Creating a new datatype
	int subarray[1][4];
	int sizes[2],subsizes[2],starts[2];
	sizes[0]=4;sizes[1]=4;
	subsizes[0]=4; subsizes[1]=1;
	starts[0]=0; starts[1]=rank;
	MPI_Type_create_subarray(2,sizes,subsizes,starts,MPI_ORDER_C,MPI_INT,&newtype);
	MPI_Type_commit(&newtype);
	etype=MPI_INT;
	disp=0;
	// Set the file view for each MPI type using the new strided datatype as filetype.
	MPI_File_set_view(fh,disp,etype,newtype,data_rep, MPI_INFO_NULL);
	
	// Read the data as usual. 
	MPI_File_read(fh,subarray,nprocs,MPI_INT, &status);
	
	// Lets print what we got.
	for ( i =0 ; i<1; i++)
		printf("[%d] %d %d %d %d \n",rank,subarray[i][0],subarray[i][1],subarray[i][2],subarray[i][3]);

	MPI_File_close(&fh);
	MPI_Finalize();
}
