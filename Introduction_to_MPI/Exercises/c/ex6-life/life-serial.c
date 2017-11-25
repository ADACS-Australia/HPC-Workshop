/*****************************************************************************
 *
 *  A simple implementation of John Conway's "Game of life"
 *  The system is im x jm cells and runs for nsteps iterations
 *  Boundary conditions may be periodic or 'closed'.
 *
 *****************************************************************************/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {

  const int im = 16;
  const int jm = 16;
  const int imp1 = im + 1;
  const int jmp1 = jm + 1;
  const int imp2 = im + 2;
  const int jmp2 = jm + 2;
  const int nsteps = 12;
  const int periodic = 1;

  int i, j, n;
  int live, ncount;

  int ** state_old;
  int ** state_new;

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

  /*  initialize state, for example live cells marked 'X' ...
   *
   *         i
   *
   *  j-2    X
   *  j-1   X X
   *  j    XX XX
   */

  i = im/2;
  j = jm/2;
  assert(i >= 3 && i <= im-2);
  assert(j >= 3);

  state_old[i-2][j  ] = 1;
  state_old[i-1][j  ] = 1;
  state_old[i-1][j-1] = 1;
  state_old[i  ][j-2] = 1;
  state_old[i+1][j  ] = 1;
  state_old[i+1][j-1] = 1;
  state_old[i+2][j  ] = 1;

  /* Time step loop (counting from 1...) */

  for (n = 1; n <= nsteps; n++) {

    if (periodic) {
      for (j = 1; j <= jm; j++) {
	state_old[0][j]    = state_old[im][j];
	state_old[imp1][j] = state_old[1][j];
      }
      for (i = 0; i <= imp1; i++) {
	state_old[i][0]    = state_old[i][jm];
	state_old[i][jmp1] = state_old[i][1];
      }
    }
    else {
      for (j = 1; j <= jm; j++) {
	state_old[0][j]    = 0;
	state_old[imp1][j] = 0;
      }
      for (i = 0; i <= imp1; i++) {
	state_old[i][0]    = 0;
	state_old[i][jmp1] = 0;
      }
    }

    /* Update, and keep a count of the number of live cells */

    ncount = 0;

    for (i = 1; i <= im; i++) {
      for (j = 1; j <= jm; j++) {

	state_new[i][j] = 0;
	if (state_old[i][j]) ncount += 1;

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

    for (j = 1; j <= jm; j++) {
      for (i = 1; i <= im; i++) {
	printf("%1d ", state_old[i][j]);
      }
      printf("\n");
    }

    printf("Step, count %2d %2d\n", n, ncount);


    /* update time levels */

    for (i = 0; i < imp2; i++) {
      for (j = 0; j < jmp2; j++) {
	state_old[i][j] = state_new[i][j];
      }
    }

    /* Next time step */
  }

  /* Finish */

  for (i = 0; i < imp2; i++) {
    free(state_old[i]);
    free(state_new[i]);
  }

  free(state_old);
  free(state_new);

  return 0;
}
