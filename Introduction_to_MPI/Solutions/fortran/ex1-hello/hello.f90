program hello

  ! An introductory MPI program using the default communicator
  ! MPI_COMM_WORLD to print a message to the screen on each rank.

  ! Access to MPI types and constants is via use of the module "mpi"
  ! While we must provide an error flag (here "ifail"), in practice
  ! we never have to check its value on return.

  ! Note that some programs may use the older idiom of
  !   include 'mpif.h'
  ! instead of "use mpi". Some compilers may still require the older
  ! form.

  use mpi
  implicit none

  integer :: ifail
  integer :: rank, size

  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  write (unit = *, fmt = *) "Hello from rank ", rank, " of ", size

  call mpi_finalize(ifail)

end program hello
