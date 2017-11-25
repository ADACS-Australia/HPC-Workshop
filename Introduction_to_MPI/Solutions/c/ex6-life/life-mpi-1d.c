/*****************************************************************************
 *
 *  A simple implementation of John Conway's "Game of life"
 *  using MPI with a one-dimensional domain decomposition
 *  (NDIMS=1) in the x-direction.
 *
 *  The system is im x jm cells and runs for nsteps iterations
 *  Boundary conditions may be periodic or 'closed'.
 *
 *****************************************************************************/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include <mpi.h>
#define NDIMS 1

int main(int argc, char * argv[]) {

  const int imtot = 16;
  const int jmtot = 16;
  const int nsteps = 12;
  const int periodic = 1;

  int im, jm;
  int imp1, jmp1;
  int imp2, jmp2;

  int i, j, n;
  int i0;
  int live, lcount, ncount;

  int ** state_old;
  int ** state_new;

  /* MPI variables for communicator, and halo communication */

  MPI_Comm comm;
  int rank, size;
  int dims[NDIMS];
  int periods[NDIMS];
  int mycoords[NDIMS];
  int my_left, my_right;

  const int my_tagl = 9999;
  const int my_tagr = 9998;
  MPI_Request req[4];
  MPI_Status  status[4];

  /* Message buffers */

  int * sxl;  /* Send in x-direction to left  */
  int * sxr;  /* Send in x-direction to right */
  int * rxl;
  int * rxr;



  /* Initialise */

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  /* Check a regular 1-d decomposition is possible */

  if (imtot % size != 0) {
    printf("Number of points not exactly divisible by number of MPI tasks\n");
    MPI_Abort(MPI_COMM_WORLD, -1);
  }

  /* Create the one-dimensional Cartesian communicator */
  /* Set the local system size */

  periods[0] = periodic;
  dims[0]= 0;
  MPI_Dims_create(size, NDIMS, dims);
  MPI_Cart_create(MPI_COMM_WORLD, NDIMS, dims, periods, 1, &comm);

  MPI_Comm_rank(comm, &rank);
  MPI_Cart_shift(comm, 0, 1, &my_left, &my_right);
  MPI_Cart_coords(comm, rank, NDIMS, mycoords);

  im = imtot / dims[0];
  jm = jmtot;
  imp1 = im + 1;
  jmp1 = jm + 1;
  imp2 = jm + 2;
  jmp2 = jm + 2;

  /* Allocate a two-dimensional array for both old and new state */
  /* We use calloc() to provide default initialisation to zero. */
  /* The 'real' system will be indexed 1 .. im, 1 .. jm */

  state_old = calloc(imp2, sizeof(int *));
  state_new = calloc(imp2, sizeof(int *));
  assert(state_old);
  assert(state_new);

  for (i = 0; i < imp2; i++) {
    state_old[i] = calloc(jmp2, sizeof(int));
    state_new[i] = calloc(jmp2, sizeof(int));
    assert(state_old[i]);
    assert(state_new[i]);
  }

  /* Allocate the message buffers; for simplicity these are all of
   * extent jmp2 */

  sxl = calloc(jmp2, sizeof(int));
  sxr = calloc(jmp2, sizeof(int));
  rxl = calloc(jmp2, sizeof(int));
  rxr = calloc(jmp2, sizeof(int));
  assert(sxl);
  assert(sxr);
  assert(rxl);
  assert(rxr);

  /*  Initialize state, for example live cells marked 'X' ...
   *
   *         i=i0
   *
   *  j-2    X
   *  j-1   X X
   *  j    XX XX
   */

  /* Every rank must test to see if the relevant points are local...
   * so the local x-coordinate for indexing the array should be
   * offset by the starting position in the global system.
   */

  i0 = imtot/2 - mycoords[0]*im;
  j  = jmtot/2;

  i = i0 - 2;
  if (i >= 1 && i <= im) state_old[i][j] = 1;

  i = i0 - 1;
  if (i >= 1 && i <= im) {
    state_old[i][j-1] = 1;
    state_old[i][j  ] = 1;
  }

  i = i0;
  if (i >= 1 && i <= im) state_old[i][j-2] = 1;

  i = i0 + 1;
  if (i >= 1 && i <= im) {
    state_old[i][j-1] = 1;
    state_old[i][j  ] = 1;
  }

  i = i0 + 2;
  if (i >= 1 && i <= im) state_old[i][j] =1;


  /* Time step loop (counting from 1...) */

  for (n = 1; n <= nsteps; n++) {

    /* Pack the x-direction buffers, exchange, and unpack */

    for (j = 0; j <= jmp1; j++) {
      sxl[j] = state_old[1][j];
      sxr[j] = state_old[im][j];
    }

    MPI_Irecv(rxr, jmp2, MPI_INT, my_right, my_tagl, comm, req);
    MPI_Irecv(rxl, jmp2, MPI_INT, my_left, my_tagr, comm, req + 1);
    MPI_Issend(sxl, jmp2, MPI_INT, my_left, my_tagl, comm, req + 2);
    MPI_Issend(sxr, jmp2, MPI_INT, my_right, my_tagr, comm, req + 3);
    MPI_Waitall(4, req, status);

    for (j = 1; j <= jm; j++) {
      state_old[0][j]    = rxl[j];
      state_old[imp1][j] = rxr[j];
    }

    /* y-direction */

    for (i = 0; i <= imp1; i++) {
      state_old[i][0]    = state_old[i][jm];
      state_old[i][jmp1] = state_old[i][1];
    }

    /* Update, and keep a count of the number of live cells */

    lcount = 0;

    for (i = 1; i <= im; i++) {
      for (j = 1; j <= jm; j++) {

	state_new[i][j] = 0;
	if (state_old[i][j]) lcount += 1;

	live = state_old[i-1][j-1] + state_old[i][j-1] + state_old[i+1][j-1]
	     + state_old[i-1][j  ]                     + state_old[i+1][j  ] 
	     + state_old[i-1][j+1] + state_old[i][j+1] + state_old[i+1][j+1];

	if (state_old[i][j]) {
	  if (live == 2 || live == 3) {
	    /* remains alive */
	    state_new[i][j] = 1;
	  }
	  else {
	    /* dies */
	    state_new[i][j] = 0;
	  }
	}
	else {
	  /* currently dead */
	  if (live == 3) {
	    /* new cell */
	    state_new[i][j] = 1;
	  }
	}
      }
    }

    /* output */
    /*
    for (j = 1; j <= jm; j++) {
      for (i = 1; i <= im; i++) {
	printf("%1d ", state_old[i][j]);
      }
      printf("\n");
    }
    */

    MPI_Reduce(&lcount, &ncount, 1, MPI_INT, MPI_SUM, 0, comm);
    if (rank == 0) {
      printf("Step, count %2d %2d\n", n, ncount);
    }

    /* update time levels */

    for (i = 0; i < imp2; i++) {
      for (j = 0; j < jmp2; j++) {
	state_old[i][j] = state_new[i][j];
      }
    }

    /* Next time step */
  }

  /* Release resources and finish */

  free(rxr);
  free(rxl);
  free(sxr);
  free(sxl);

  for (i = 0; i < imp2; i++) {
    free(state_new[i]);
    free(state_old[i]);
  }

  free(state_new);
  free(state_old);

  MPI_Comm_free(&comm);
  MPI_Finalize();

  return 0;
}
