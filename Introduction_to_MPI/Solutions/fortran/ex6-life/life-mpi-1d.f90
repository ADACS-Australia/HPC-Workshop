program life

  ! Game of life program using MPI and a one-dimensional domain
  ! decomposition in the x-direction.

  ! The program checks that a decomposition is possible on the
  ! current number of MPI tasks as a first step.

  use mpi
  implicit none

  ! imtot and jmtot are the global system size in each direction
  ! im and jm are the local system size per MPI rank

  integer, parameter :: imtot = 16
  integer, parameter :: jmtot = 16
  integer, parameter :: nsteps = 12

  integer :: im, jm
  integer :: imp1, jmp1
  integer :: i, j
  integer :: n
  integer :: nc, np, tmp
  integer :: live, lcount, ncount

  ! System state

  logical, parameter :: periodic = .true.
  logical, allocatable, dimension(:, :, :) :: state

  ! send buffers for x-direction (left and right going) messages
  ! recv buffers for x-direction (lelft and right) messages

  logical, allocatable, dimension(:) :: sxl, sxr
  logical, allocatable, dimension(:) :: rxl, rxr

  ! MPI variables

  integer :: ifail
  integer :: rank, size

  integer :: comm
  integer :: my_left, my_right

  ! For 1-dimensional decomposition:

  integer, parameter :: ndims = 1
  integer, dimension(ndims) :: dims
  integer, dimension(ndims) :: mycoords
  logical, dimension(ndims) :: periods

  ! MPI messages
  integer, parameter :: my_tagl = 9999
  integer, parameter :: my_tagr = 9998
  integer, dimension(4) :: req
  integer, dimension(MPI_STATUS_SIZE, 4) :: status




  call mpi_init(ifail)
  call mpi_comm_rank(MPI_COMM_WORLD, rank, ifail)
  call mpi_comm_size(MPI_COMM_WORLD, size, ifail)

  ! If a decomposition is possible, use a Cartesian communicator,
  ! and work out relevant ranks in the new communicator

  if (mod(imtot, size) /= 0) then
     write (unit = *, fmt = *) &
     'Number of points not exactly divisible by number of MPI tasks'
     call mpi_abort(MPI_COMM_WORLD, -1, ifail)
  end if

  periods(:) = periodic

  call mpi_dims_create(size, ndims, dims, ifail)
  call mpi_cart_create(MPI_COMM_WORLD, ndims, dims, periods, .true., comm, ifail)

  call mpi_comm_rank(comm, rank, ifail)
  call mpi_cart_shift(comm, 0, 1, my_left, my_right, ifail)
  call mpi_cart_coords(comm, rank, ndims, mycoords, ifail)

  ! Commpute the number of points held locally on each rank
  ! Add one point at each end to hold the halo region
  ! Allocate message buffers for transfers in the x direction

  im = imtot/size
  jm = jmtot
  imp1 = im + 1
  jmp1 = jm + 1

  allocate(state(0:imp1, 0:jmp1, 2), stat = ifail)
  allocate(sxl(1:jm), stat = ifail)
  allocate(sxr(1:jm), stat = ifail)
  allocate(rxl(1:jm), stat = ifail)
  allocate(rxr(1:jm), stat = ifail)

  ! initial state

  nc = 1 ! pointer to current time level
  np = 2 ! pointer to forward time level

  state(:,:,:) = .false.

  ! Every rank must test to see if the relevant points are local...
  !    the points in the global system are:
  !    state(2, 6) state(3, 5:6) state(4, 4) state(5, 5:6) state(6,6)
  ! ...so subtract the starting x coordinate for this rank

  i = 2 - mycoords(1)*im
  if (i >= 1 .and. i <= im) state(i, 6, nc) = .true.

  i = 3 - mycoords(1)*im
  if (i >= 1 .and. i <= im) state(i, 5:6, nc) = .true.

  i = 4 - mycoords(1)*im
  if (i >= 1 .and. i <= im) state(i, 4, nc) = .true.

  i = 5 - mycoords(1)*im
  if (i >= 1 .and. i <= im) state(i, 5:6, nc) = .true.

  i = 6 - mycoords(1)*im
  if (i >= 1 .and. i <= im) state(i, 6, nc) = .true.

  do n = 1, nsteps

     ! halo regions

     ! x-direction

     sxl(1:jm) = state(1,  1:jm, nc)
     sxr(1:jm) = state(im, 1:jm, nc)

     call mpi_irecv(rxr, jm, MPI_LOGICAL, my_right, my_tagl, comm, req(1), ifail)
     call mpi_irecv(rxl, jm, MPI_LOGICAL, my_left, my_tagr, comm, req(2), ifail)

     call mpi_issend(sxl, jm, MPI_LOGICAL, my_left, my_tagl, comm, req(3), ifail)
     call mpi_issend(sxr, jm, MPI_LOGICAL, my_right, my_tagr, comm, req(4), ifail)
     call mpi_waitall(4, req, status, ifail)

     state(0,    1:jm, nc) = rxl(1:jm)
     state(imp1, 1:jm, nc) = rxr(1:jm)

     ! y-direction
     state(0:imp1, 0,    nc) = state(0:imp1, jm, nc)
     state(0:imp1, jmp1, nc) = state(0:imp1,  1, nc)

     ! update

     lcount = 0

     do j = 1, jm
        do i = 1, im
           if (state(i,j,nc)) lcount = lcount + 1
           state(i,j,np) = state(i,j,nc)
           ! count the neighbours (including self)
           live = count(state(i-1:i+1, j-1:j+1, nc))
           if (state(i,j,nc)) then
              ! currently alive
              if (live == 3 .or. live == 4) then
                 ! remains alive
              else
                 ! dies
                 state(i,j,np) = .false.
              end if
           else
              ! currently dead
              if (live == 3) then
                 ! new cell
                 state(i,j,np) = .true.
              end if
           end if
           ! next cell
        end do
     end do

     ! output

     call mpi_reduce(lcount, ncount, 1, MPI_INTEGER, MPI_SUM, 0, comm)

     if (rank == 0) then
        write (unit = *, fmt = '(a,i3,i3)') "Step, count: ", n, ncount 
     end if

     ! swap time level pointers
     tmp = nc
     nc = np
     np = tmp

  end do

  deallocate(rxr, rxl, sxr, sxl)
  deallocate(state)

  call mpi_finalize(ifail)

end program life
