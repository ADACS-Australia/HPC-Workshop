#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
typedef struct{
	int neq; 
	int num_row,num_col;
	char* filename;
}input;


void* check_malloc(size_t, char*);
void Read_command_line_arguments(int*,char**, input*);
float** allocate_mat(int,int);
void set_to_default_system(float**);
void read_in_system(int, float**,char*);
void write_out(int , float** );
float* solve(int , float** );
float summation(int,float*, float**);
float* backward_substitution(int,float**);
void validation(float*,float**);


