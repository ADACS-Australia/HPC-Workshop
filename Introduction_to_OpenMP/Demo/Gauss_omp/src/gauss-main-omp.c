#include "gaussian.h"
#include <time.h>
/********************************************
 * This example implements the solution of a *
 * System of Linear Equations using Gaussian *	
 * Elimination (no pivoting) method.	    *
 *               SERIAL VERSION		    *
 ********************************************/
input *parms;
int main (int argc, char* argv[]){
	double t1=0.0,t2=0.0;
	double diff_time;
	//Default values
	
	parms= (input*) check_malloc(sizeof(input),"Allocation of parms structure failed");
	parms->neq = 4;
	parms->filename=NULL;
	Read_command_line_arguments(&argc,argv,parms);
	//Allocating an augmented matrix of size NEQ+1 x NEQ+1
	float** A = allocate_mat(parms->neq, parms->neq+1);
	if (parms->filename != NULL){
		printf("Reading in the System of linear equations from file %s\n",parms->filename);
		read_in_system(parms->neq,A,parms->filename);
	}else{
		printf("No user defined System of linear equations found.\nSetting the problem to default set.\n");
		set_to_default_system(A);
	}
	float* x = (float*) check_malloc(parms->neq*sizeof(float),"");

 	parms->num_row=parms->neq;
 	parms->num_col=parms->neq+1;

	t1=omp_get_wtime();
	x = solve(parms->neq,A);
	t2=omp_get_wtime();
	diff_time=(t2-t1);
	printf("Execution time=%lf\n",diff_time);
	validation(x,A);
	free(parms);
	return 0;	
}

