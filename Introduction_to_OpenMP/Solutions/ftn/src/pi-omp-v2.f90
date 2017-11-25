! Calculating Pi with using method: 
!     integral 4.0/(1+x^2) dx = p	     
! 	   OpenMP Version 2	     
program pi_omp_v1
implicit none
integer(kind=8) :: num_steps = 100000000000
integer(kind=8) i,tid,nthreads,omp_get_num_threads,omp_get_thread_num
real*8 :: PI_ref=3.1415926535897932,step,x,pi
real*8 :: summation=0.0
real*8   :: start,finish,omp_get_wtime
!call cpu_time(start)
step = 1/(1.0 * num_steps)
start=omp_get_wtime()
!$omp parallel do private(x) reduction(+:summation) shared(step)
	do i =1,num_steps
		x=((i-1)+0.5) * step;
		summation=summation + (4.0/(1.0+(x*x)))
	end do
!$omp end parallel do
	pi=step*summation

!call cpu_time(finish)
finish=omp_get_wtime()
	write(*,*) "Estimated value of pi =",pi
	write(*,*) "Error =", abs(PI_ref - pi)
	write(*,*) "Compute time=", (finish-start)," seconds"
end


