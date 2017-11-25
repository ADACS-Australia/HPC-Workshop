program ring

  ! Accumulate the sum of the ranks by sending a message around a
  ! ring.

  ! We use a synchronous non-blocking send mpi_issend() and a non-
  ! blocking recieve mpi_irecv(), along with two wait statements.

  use mpi
  implicit none

  integer :: ifail
  integer :: rank, size
  integer :: my_prev, my_next
  integer :: sum

  ! Message information

  integer :: sendbuf, recvbuf
  integer :: req1, req2
  integer, parameter :: my_tag = 9999
  integer, dimension(MPI_STATUS_SIZE) :: status

  ! loop counter
  integer :: n

  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  ! Work out neighbouring ranks

  my_prev = rank - 1
  if (my_prev < 0) my_prev = my_prev + size
  my_next = mod(rank + 1, size)

  ! Initialise the sum and the message for all ranks
  sum = 0
  sendbuf = rank

  do n = 1, size

     call mpi_irecv(recvbuf, 1, MPI_INTEGER, my_prev, my_tag, MPI_COMM_WORLD, &
                    req1, ifail)
     call mpi_issend(sendbuf, 1, MPI_INTEGER, my_next, my_tag, MPI_COMM_WORLD, &
                     req2, ifail)

     ! When the receive has completed, we can use the contents of recvbuf
     call mpi_wait(req1, status, ifail)
     sum = sum + recvbuf

     ! When the send has completed, we can safely re-use the send buffer
     call mpi_wait(req2, status, ifail)
     sendbuf = recvbuf

  end do

  ! Display the result on all ranks, along with the correct answer

  write (unit = *, fmt = '(a,i3,a,i4,a,i4)') &
       "Rank ", rank, " has sum of ranks ", sum, " Answer ", (size - 1)*size/2

  call mpi_finalize(ifail)


end program ring
