program collective

  use mpi
  implicit none

  integer :: ifail
  integer :: rank, size

  integer :: sum

  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  call mpi_allreduce(rank, sum, 1, MPI_INTEGER, MPI_SUM, MPI_COMM_WORLD, ifail)

  write (unit = *, fmt = '(a,i3,a,i4,a,i4)') &
       "Rank ", rank, " has sum of ranks ", sum, " Answer ", (size - 1)*size/2

  call mpi_finalize(ifail)

end program collective
