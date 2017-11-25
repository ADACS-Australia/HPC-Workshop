#include "gaussian-mpi.h"                                   

input* parms;
int main (int argc, char* argv[]){
	MPI_Init(&argc,&argv);
	double diff_time;
	double t1=0.0,t2=0.0,t=0.0;
	//Default values
	t1 = MPI_Wtime();
	parms= (input*) check_malloc(sizeof(input),"Allocation of parms structure failed");
	parms->neq = 4;
	parms->num_row=parms->neq;
	parms->num_col=parms->neq+1;;
	parms->filename=NULL;
	Read_command_line_arguments(&argc,argv,parms);
	int rank,num_tasks;
	check_flag(MPI_Comm_rank(MPI_COMM_WORLD,&rank),1);
	check_flag(MPI_Comm_size(MPI_COMM_WORLD,&num_tasks),2);

	//Check if MPI-tasks are less than equations, in which case abort
	if (rank==MASTER){	
		if ( parms->neq < num_tasks){
			printf("MPI-tasks must not exceed the number of equations\n");
			MPI_Abort(MPI_COMM_WORLD,911);
		}
	}

	float** A;
	if (rank == MASTER)
		A = allocate_mat(parms->num_row, parms->num_col);

#ifdef PARALLEL_IO 

	// Get decomposition information to allocate A and read columns for each MPI-task
	get_decomposition(rank,num_tasks); 
	//Allocating an augmented matrix of size NEQ x NEQ+1
	if (parms->filename != NULL){
		printf("[%d]: Reading in the System of linear equations from file %s in parallel\n",rank,parms->filename);
		t=MPI_Wtime();
		read_in_system_parallel_io(rank,parms->filename);
		t=MPI_Wtime() - t;
		printf("[%d] Reading took %lf s\nMPI_Wtick=%lf\n",rank,t,MPI_Wtick());
	}
	else{
		if (rank == MASTER)
			printf("No user defined System of linear equations found.\nSetting the problem to default set.\n");
		//set_to_default_system(A);
	}

#else
	if (rank== MASTER){	
		//Allocating an augmented matrix of size NEQ x NEQ+1
		A = allocate_mat(parms->num_row, parms->num_col);
		if (parms->filename != NULL){
			printf("Reading in the System of linear equations from file %s\n",parms->filename);
			t=MPI_Wtime();
			read_in_system(parms->neq,A,parms->filename);
			t=MPI_Wtime() - t;
			printf("Reading took %lf s\nMPI_Wtick=%lf\n",t,MPI_Wtick());
		}else{
			printf("No user defined System of linear equations found.\nSetting the problem to default set.\n");
			set_to_default_system(A);
		}
	}
	distribute_columns(rank,num_tasks,A);
#endif
	solve_mpi(rank,num_tasks);
	gather_columns(rank,num_tasks,A);	
	if (rank==MASTER){
		float* x = (float*) check_malloc(parms->neq*sizeof(float),"Allocation failed for soultion vector x in main");
		x=backward_substitution(parms->neq,A);
		validation(x,A);
	}
	t2 = MPI_Wtime();
	diff_time = t2 - t1;
	double recv_time[num_tasks];
	check_flag(MPI_Gather(&diff_time,1,MPI_DOUBLE,recv_time,1,MPI_DOUBLE,MASTER,MPI_COMM_WORLD),15);
	if (rank==MASTER){
		double avg_time=0.0;
		for (int i=0; i< num_tasks; i++)
			avg_time += recv_time[i];
		printf("Average compute time = %2.8lf \n",(double) avg_time/num_tasks);
	}

	MPI_Finalize();

}


