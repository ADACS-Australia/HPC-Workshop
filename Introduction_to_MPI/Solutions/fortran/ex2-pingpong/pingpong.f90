program pingpong

  ! An MPI program to send a message back and forth between two ranks
  ! using a blocking send mpi_send(), and a blocking
  ! recieve mpi_recv().

  use mpi
  implicit none

  integer, parameter :: nexchange = 100
  integer :: ifail
  integer :: rank, size

  ! Message information (here type MPI_INTEGER)

  integer :: sender, recver
  integer :: sendbuffer, recvbuffer
  integer, dimension(MPI_STATUS_SIZE) :: status
  integer, parameter :: my_tag = 9999

  ! loop counter
  integer :: n


  call mpi_init(ifail)

  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  if (size /= 2) then
     write (unit = *, fmt = *) "Must use exactly two MPI tasks"
     call mpi_abort(MPI_COMM_WORLD, -1, ifail)
  end if

  ! The message is fixed
  sendbuffer = 1

  do n = 1, nexchange

     ! The sender and recver alternate between rank 0 and 1
     sender = mod(n, 2)
     recver = 1 - sender

     if (rank == sender) then
        call mpi_send(sendbuffer, 1, MPI_INTEGER, recver, my_tag, &
                       MPI_COMM_WORLD, ifail)
     else
        call mpi_recv(recvbuffer, 1, MPI_INTEGER, sender, my_tag, &
                      MPI_COMM_WORLD, status, ifail)
     end if

  end do

  call mpi_finalize(ifail)

end program pingpong
