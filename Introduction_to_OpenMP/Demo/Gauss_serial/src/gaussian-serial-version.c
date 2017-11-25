#include "gaussian-serial.h"
extern input* parms;


void* check_malloc(size_t bytes, char* msg){
	void* p = malloc (bytes);
	if (p == NULL)
		printf("%s\n",msg);
	return (p);
}

void Read_command_line_arguments(int* argc,char** argv, input* parms){
	int i;
	if (*argc > 1){
		for (i=0; i< *argc; i++){
			if ( argv[i][0] == '-'){
				if (argv[i][1] == 'n'){
					parms->neq = atoi(argv[i+1]);
					parms->num_row=parms->neq;
					parms->num_col=parms->neq+1;
				}
				else if (argv[i][1] == 'f'){
					parms->filename=(char*) malloc (256*sizeof(char));
					sprintf(parms->filename,"%s",argv[i+1]);
				}
			}
		}    
	}
}

float** allocate_mat(int rows, int cols){
        float** A;
        A = (float**) check_malloc(rows * sizeof(float*),"Allocation of augmented matrix failed");
        for (int i =0; i<rows;i++){
                A[i] = (float*) check_malloc( cols * sizeof(float),"Allocation of augmented matrix failed");
        }
        for (int i=0; i<rows; i++){
                for (int j=0; j<cols; j++){
                        A[i][j] = 0.0;
                }
        }
        return A;
}


void set_to_default_system(float** A){
	A[0][0] = 3.0;  A[0][1] = 1.0;  A[0][2] = 9.0;   A[0][3] = 5.0;  A[0][4] = 1.0;

	A[1][0] = 3.0;  A[1][1] = 5.0;  A[1][2] = 3.0;   A[1][3] = 4.0/3.0;  A[1][4] = 4.0;

	A[2][0] = 4.0/3.0;  A[2][1] = 4.0/3.0;  A[2][2] = 2.0;   A[2][3] = 3.0;  A[2][4] = 9.0/4.0;

	A[3][0] = 4.0/3.0;  A[3][1] = 1.0/2.0;  A[3][2] = 5.0/3.0;   A[3][3] = 7.0;  A[3][4] = 8.0;

}

void read_in_system(int neq, float** A,char* filename){
	int i,j;
	FILE* f= fopen(filename,"r");
	for (i =0; i<parms->num_row; i++){
		fread(A[i],sizeof(float),parms->num_col,f);
	}
	fclose(f);
}

void write_out(int neq , float** A){
	for (int i =0; i<neq; i++){
		for (int j=0;j<neq+1; j++){
			printf("%-3.5f   ",A[i][j]);
		}
		printf("\n");
	}
		printf("\n\n");
}

//Forward elimination to produce an upper triangular matrix
float* solve(int N, float** A){
	float* x = (float*) check_malloc(N*sizeof(float),"Allocation failed for Solution vector in function solve.");
	//There can be only N pivots
	for (int i = 0; i < N-1; i++) {
		//Traversing on N rows, starting from (i+1)th row 
		for (int j = i+1; j < N; j++) { 
			float ratio = A[j][i]/A[i][i];
			//Traversing on N+1 colums starting from (i)th column
			for (int k = i; k < N+1; k++) {
				A[j][k] -= (ratio*A[i][k]); 
			}
		}
	} 
	x=backward_substitution(N,A);
	return x;
}

//Backward subsititution to evaluate the soultion vector containing all the unkowns in the given
//system of linear equations.
float* backward_substitution(int N, float** A){
	//Solution vector
	float* x= (float*) check_malloc(N*sizeof(float),"Allocation failed for Solution vector in function solve.");
	for (int i=N-1; i>=0; i--){
		x[i] = A[i][N];
		for (int j=(N-1); j>i; j--){
			x[i] -= (A[i][j] * x[j]);
		}
		x[i] = x[i]/A[i][i];
	}

	return x;

}

void validation(float* x,float** A){

	int i , j;
	float* b = (float*) check_malloc(parms->num_row*sizeof(float),"Allocation failed for soultion vector b in validation");
	for (i=0; i< parms->num_row; i++){
		b[i]=0.0;
		for (j=0; j < parms->num_col-1 ; j++){
			b[i]= b[i] + A[i][j]*x[j];
		}
	}
	FILE *fw;
	fw = fopen("solution.out","w+");
	printf("\n Writing solution to file\n");
	fprintf(fw,"    B_orignl    |    B_approx    |    Sol vect    |\n"); 
	fprintf(fw,"-----------------------------------------------------------\n");
	for (i=0; i< parms->num_row; i++)
		fprintf(fw,"    %3.5f   |    %3.5f   |    %3.5f    \n",A[i][parms->num_col-1],b[i],x[i]);

	fclose(fw);


}

