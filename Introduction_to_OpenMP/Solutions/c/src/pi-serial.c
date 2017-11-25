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
#include <omp.h>

// Reference value to estimate error
double PI_ref=3.1415926535897932;

static long long num_rects=100000000000;
double step;
int main (int argc, char* argv[]){
  double start,stop;
  double diff_time;

  long long i;
  double x,pi,sum=0.0;

  start= omp_get_wtime();   
  step = 1.0 / (double) num_rects;
        
  for (i=0; i<num_rects; i++){
        x=(i+0.5) * step;
        sum = sum + 4.0/(1.0+(x*x));
  }

  pi = step * sum ;
  stop=omp_get_wtime();
  diff_time = stop-start;
  printf ("Estimated value of pi = %2.16lf\n",pi);
  printf ("Error = %2.16lf\n",fabs(PI_ref - pi));
  printf ("Compute time= %2.5lf seconds\n",diff_time);

}
