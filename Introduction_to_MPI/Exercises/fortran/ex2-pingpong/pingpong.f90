program pingpong

  use mpi
  implicit none

  integer :: ifail
  integer :: rank, size


  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  if (size /= 2) then
     write (unit = *, fmt = *) "Must use exactly two MPI tasks"
     call mpi_abort(MPI_COMM_WORLD, -1, ifail)
  end if


  ! ...


  call mpi_finalize(ifail)

end program pingpong
