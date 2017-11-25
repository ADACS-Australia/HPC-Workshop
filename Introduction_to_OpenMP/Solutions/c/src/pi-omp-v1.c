/********************************************************
 * Calculating Pi with using midpoint rectangle method: *
 *  integral 4.0/(1+x^2) dx = pi	     		*
 *  or 							*
 *  summation (for i=0 to n) 4.0/(1+x_i^2)              *
 *  	where x_i = (i + 1/2) * delta x			*
 * 	   OpenMP Version 1          			*
 ********************************************************/
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double PI_ref=3.1415926535897932;

static long long num_rects=100000000000;
double step;
int main (int argc, char* argv[]){
	double start,stop,diff_time;

	long long i;
	start= omp_get_wtime();
	double x,
	       sum=0.0,pi=0.0;
	step = 1.0 / (double) num_rects;
	int nthreads=0;
#pragma omp parallel private(i,x) firstprivate(sum) shared(pi,nthreads)
	{	
		//All threads retrieve their thread id
		int tid= omp_get_thread_num();
//Any one of the threads retrieve the total number of threads in the shared variable nthreads
#pragma omp single 
		{

			nthreads = omp_get_num_threads();

		}
		//Partition the work into block cyclic manner store local sum in a private variable
		for (i=tid; i<num_rects; i+=nthreads){
			x= step * ((double) i+0.5);
			sum = sum+4.0/(1.0+(x*x));
		}	

		
		//Each thread does the following one at a time.
#pragma omp critical (summation)
		{
			pi += (step * sum);
		}
		

	}

	stop= omp_get_wtime();
	diff_time = (double) (stop-start);
	printf ("Estimated value of pi = %2.16lf\n",pi);
	printf ("Error = %2.16lf\n",fabs(PI_ref - pi));
	printf ("Compute time= %2.5lf seconds\n",diff_time);

}
