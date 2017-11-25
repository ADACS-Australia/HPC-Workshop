program life

  ! A simple implementation of John Conway's "Game of life"
  ! The system is im x jm cells and runs for nsteps iterations
  ! Boundary conditions may be periodic or 'closed'.

  implicit none

  integer, parameter :: im = 16
  integer, parameter :: jm = 16
  integer, parameter :: imp1 = im+1
  integer, parameter :: jmp1 = jm+1
  integer, parameter :: nsteps = 12

  logical, parameter :: periodic = .true.
  integer            :: nc, np, n
  integer            :: tmp, live
  integer            :: ncount
  integer            :: i, j

  logical, dimension(0:imp1, 0:jmp1, 2) :: state

  ! Initialise system

  nc = 1 ! nc is a pointer to current time level
  np = 2 ! np is a pointer to forward time level

  state(:,:,:) = .false.

  ! initial state, for example live cells marked 'X' ...
  !
  !        i
  !
  ! j-2    X
  ! j-1   X X
  ! j    XX XX

  i = im/2
  j = jm/2
  state(i-2, j,     nc) = .true.
  state(i-1, j-1:j, nc) = .true.
  state(i,   j-2,   nc) = .true.
  state(i+1, j-1:j, nc) = .true.
  state(i+2, j,     nc) = .true.

  ! Iterate

  do n = 1, nsteps

     ! halo regions
     if (periodic) then
        state(0,      1:jm, nc) = state(im,   1:jm, nc)
        state(imp1,   1:jm, nc) = state(1,    1:jm, nc)
        state(0:imp1,    0, nc) = state(0:imp1, jm, nc)
        state(0:imp1, jmp1, nc) = state(0:imp1,  1, nc)
     else
        state(0,      1:jm, nc) = .false.
        state(imp1,   1:jm, nc) = .false.
        state(0:imp1,    0, nc) = .false.
        state(0:imp1, jmp1, nc) = .false.
     end if

     ! update, and keep a count of the number of live cells

     ncount = 0

     do j = 1, jm
        do i = 1, im
           if (state(i,j,nc)) ncount = ncount + 1
           state(i,j,np) = state(i,j,nc)
           ! count the neighbours (including self)
           live = count(state(i-1:i+1,j-1:j+1,nc))
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

     do j = 1, jm
        do i = 1, im
           live = 0
           if (state(i,j,nc)) live = 1
           write (*, fmt = '(1x,i1)', advance = 'no') live
        end do
      write (*,*)
     end do
     write (*, fmt = '(a,i3,i3)') "Step, count: ", n, ncount 
     write (*,*)

     ! swap time level pointers
     tmp = nc
     nc = np
     np = tmp

  end do

end program life
