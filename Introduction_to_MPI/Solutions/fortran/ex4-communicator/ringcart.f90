program ringcart

  ! Pass a message around a ring in one dimension with the aid of a
  ! periodic Cartesian communicator.
  !
  ! We use synchronous non-blocking communications and mpi_waitall()
  ! to pass the message

  use mpi
  implicit none

  integer :: ifail
  integer :: rank, size
  integer :: sum

  ! 1-d Cartesian communicator
  integer :: comm
  integer :: my_left, my_right
  integer, parameter :: ndims = 1
  integer, dimension(ndims):: dims
  logical, dimension(ndims):: periods

  ! Message information

  integer :: sendbuf, recvbuf
  integer, parameter :: my_tag = 9999
  integer, dimension(2) :: req
  integer, dimension(MPI_STATUS_SIZE,2) :: status

  ! loop counter
  integer :: n


  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  ! Create periodic Cartesian communicator
  ! The 'reorder' parameter is set to .true., meaning MPI is allowed to
  ! reorder the ranks in the new communicator

  periods(:) = .true.

  call mpi_dims_create(size, ndims, dims, ifail)
  call mpi_cart_create(MPI_COMM_WORLD, ndims, dims, periods, .true., comm, ifail)

  ! check rank in new communicator
  ! and work out neighbouring ranks in 1-d: my_left - rank - my_right

  call mpi_comm_rank(comm, rank, ifail)
  call mpi_cart_shift(comm, 0, 1, my_left, my_right, ifail)

  ! Initialise the sum and the message for all ranks
  sum = 0
  sendbuf = rank

  do n = 1, size

     call mpi_irecv(recvbuf, 1, MPI_INTEGER, my_left, my_tag, comm, &
                    req(1), ifail)
     call mpi_issend(sendbuf, 1, MPI_INTEGER, my_right, my_tag, comm, &
                     req(2), ifail)
     call mpi_waitall(2, req, status, ifail)

     sum = sum + recvbuf
     sendbuf = recvbuf

  end do

  ! Display the result on all ranks, along with the correct answer

  write (unit = *, fmt = '(a,i3,a,i4,a,i4)') &
       "Rank ", rank, " has sum of ranks ", sum, " Answer ", (size - 1)*size/2

  call mpi_finalize(ifail)


end program ringcart
