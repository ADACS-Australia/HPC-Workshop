program ring

  use mpi
  implicit none

  integer :: ifail
  integer :: rank, size
  integer :: sum



  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  ! Work out neighbouring ranks
  ! ...

  ! Initialise the sum
  sum = 0

  ! Send messages
  ! ...

  ! Display the result on all ranks, along with the correct answer

  write (unit = *, fmt = '(a,i3,a,i4,a,i4)') &
       "Rank ", rank, " has sum of ranks ", sum, " Answer ", (size - 1)*size/2

  call mpi_finalize(ifail)


end program ring
