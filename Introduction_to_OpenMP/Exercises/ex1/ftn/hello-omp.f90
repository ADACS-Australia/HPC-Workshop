program hello90
        integer(kind=4):: id,nthreads,omp_get_thread_num,omp_get_num_threads
!$omp parallel private(id)
        id = omp_get_thread_num()
	write (*,*) 'Hello World from thread', id
!$omp barrier
	if ( id == 0 ) then
                nthreads = omp_get_num_threads()
	write (*,*) 'There are', nthreads, 'threads'
	end if
!$omp end parallel
	end program

