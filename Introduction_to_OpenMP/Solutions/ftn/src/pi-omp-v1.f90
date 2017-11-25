! Calculating Pi with using method: 
!     integral 4.0/(1+x^2) dx = p	     
! 	   OpenMP Version 1	     
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
!$omp parallel private(x,tid) firstprivate(summation) shared(pi,nthreads,step)
	tid=omp_get_thread_num();
!$omp single
	nthreads=omp_get_num_threads();
!$omp end single
	do i =tid,num_steps-1,nthreads
		x=((i-1)+0.5) * step;
		summation=summation + (4.0/(1.0+(x*x)))
	end do
!$omp atomic update 
	pi=pi+(step*summation)

!$omp end parallel 
!call cpu_time(finish)
finish=omp_get_wtime()
	write(*,*) "Number of threads= ",nthreads
	write(*,*) "Estimated value of pi =",pi
	write(*,*) "Error =", abs(PI_ref - pi)
	write(*,*) "Compute time=", (finish-start)," seconds"
end


