#include <omp.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>


void main (){

#pragma omp parallel
	{
		int thread_id =omp_get_thread_num();
		char* hostname = (char*) malloc(256*sizeof(char));
		gethostname(hostname,256*sizeof(char));
		printf("Hello world from thread %d on node %s\n",thread_id,hostname);
	}
}
