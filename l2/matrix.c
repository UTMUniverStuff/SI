#include<stdio.h>
#include<stdlib.h>

struct MatrixHead{
	float **ptr;
	int m;
	int n;	
};

#define FOR2D(ptr, m, n) \
	for(int i=0; i<m; i++)    \
		for(int j=0; j<n; j++)


#define FORM(mat) FOR2D(mat->ptr, mat->m, mat->n)

struct MatrixHead
matrix_allocate(int m, int n)
{
	struct MatrixHead matrix_head;
	matrix_head.m = m;
	matrix_head.n = n;

	matrix_head.ptr = calloc(m, sizeof(float*));
	matrix_head.ptr[0] = calloc(m*n, sizeof(float));

	for(int i=1; i<m; i++)
		matrix_head.ptr[i] = matrix_head.ptr[0] + n*i;
	return matrix_head;
}

void
matrix_free(struct MatrixHead * matrix_head)
{
	free(matrix_head->ptr[0]);
	free(matrix_head->ptr);
	matrix_head->ptr = 0;
}

void
matrix_stdin(struct MatrixHead *matrix_head)
{
	printf("Input %dx%d numbers\n", matrix_head->n, matrix_head->m);
	FOR2D(matrix_head->ptr, matrix_head->m, matrix_head->n)
		scanf("%f", matrix_head->ptr[i] + j);
}

void
matrix_stdout(struct MatrixHead *matrix_head)
{
	for(int i=0; i<matrix_head->m; i++)
	{
		for(int j=0; j<matrix_head->n; j++)
		{
			printf("%9.4f ", matrix_head->ptr[i][j]);
		}
		puts("\n");
	}
}

struct MatrixHead
matrix_op(struct MatrixHead left, struct MatrixHead right, float (*func)(float, float))
{
	struct MatrixHead result = {}; 
	if (left.ptr && right.ptr && left.m == right.m && left.n == right.n)
	{
		result = matrix_allocate(left.m, left.n);
		FOR2D(result.ptr, result.m, result.n)
			result.ptr[i][j] = func(left.ptr[i][j], right.ptr[i][j]);
	}
	return result;
}
float add(float a, float b) { return a+b;}
float sub(float a, float b) { return a-b; }
float dot(float a, float b) { return a*b; }
float divide(float a, float b) { return a/b; }

int
main()
{
	struct MatrixHead mats[2] =  { 
		matrix_allocate(2, 3),
	 	matrix_allocate(2, 3),
	};
	for(int i=0; i<2; i++) {
		matrix_stdin(mats + i);
		matrix_stdout(mats + i);
	}
	float (*op_func)(float, float) = NULL;
	while(!op_func)
	switch(getchar())
	{
		case '+': op_func = add; break;	
		case '-': op_func = sub; break;	
		case '*': op_func = dot; break;	
		case '/': op_func = divide; break;
	}
	struct MatrixHead sum = matrix_op(mats[0], mats[1], op_func);
	matrix_stdout(&sum);
	matrix_free(&sum);
	matrix_free(&mats[0]);
	matrix_free(&mats[1]);
	return 0;
}
