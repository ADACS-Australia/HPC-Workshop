/********************************************************
 * Calculating Pi with using midpoint rectangle method: *
 *  integral 4.0/(1+x^2) dx = pi	     		*
 *  or 							*
 *  summation (for i=0 to n) 4.0/(1+x_i^2)              *
 *  	where x_i = (i + 1/2) * delta x			*
 * 	   Serial Version	     			*
 ********************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
/* Including OpenMP header to call the timing function from API
 * to estimate compute_time*/
#include <omp.h>

// Reference value to estimate error
double PI_ref=3.1415926535897932;

static long num_rects=1000000000;
double step;
int main (int argc, char* argv[]){
  double start,stop;
  double diff_time;
  long i;
  double x,pi,sum=0.0;

  printf ("Requested number of steps = %ld\n",num_rects);
  start= omp_get_wtime();   
 // Calculate delta x. Hint: reciprocal of num_rects
  step = 1/(double) num_rects;
  
        
  for (i=0; i<num_rects; i++){
/*
 * Write an algorithm which first evaluates the 
 * 	evaluate midpoint of ith rectangle (x_i)
 * 	updates the sum by evaluating f(x) at x
 */
  }

  //Update value of pi 
  stop= omp_get_wtime();
  diff_time = stop-start;
  printf ("Estimated value of pi = %2.15lf\n",pi);
  printf ("Error = %2.15lf\n",fabs(PI_ref - pi));
  printf ("Compute time= %2.5lf seconds\n",diff_time);

}
