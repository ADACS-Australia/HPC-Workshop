#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

#define MASTER 0
int main (int argc , char* argv[]){
	/* Initialize MPI*/
	MPI_Init(&argc,&argv);
	int rank, nprocs,size=512;
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&nprocs);

	MPI_File fh;
	char filename[512];
	if (argc < 2){
		printf ("%d by %d square matrix will be generated\n",size,size);
	}
	else if (argc > 2){
		printf ("No more than 1 argument can be passed to the program\n");
		exit(1);
	}
	else
		size=atoi(argv[1]);

	sprintf(filename,"%dby%d.mat",size,size);

	int i=0,j=0;
	int rows=size, cols=size+1,block=rows/nprocs;
	int my_rows;
	if (rank==nprocs-1)
		my_rows=(rows%nprocs) + block;
	else
		my_rows=block;

	MPI_Status status;
	MPI_Offset disp,offset;
	MPI_Info info;
	MPI_Info_create(&info);
	// Set stripe count and size respectively
	MPI_Info_set(info,"striping_factor","4");
	MPI_Info_set(info,"striping_unit","1048576");
	MPI_File_open(MPI_COMM_WORLD,filename,MPI_MODE_CREATE | MPI_MODE_WRONLY,info,&fh);
	
	int count=my_rows*cols;
	int bytes= count*sizeof(float);
	int indx=0;
	float* buf = (float*) malloc(bytes);
	//So that each rank produces different random number sequence, randomize the seed
	int seed = (rank+1);
    	srand(seed);
	for (i=0; i< my_rows; i++){
		for(j=0; j< cols; j++){
			buf[indx]= (float)rand()/(float)RAND_MAX; 
			indx++;
		}
	}

	printf("%d: my_rows=%d , cols=%d , count=%d, indx=%d\n",rank,my_rows,cols,count,indx);
	offset=rank*count;
	MPI_File_write_shared(fh,buf,count,MPI_FLOAT,&status);
	
	//Finalizing MPI
	MPI_Info_free(&info);
	MPI_File_close(&fh);
	MPI_Finalize();

}

