program point_function_comp

    use point_functions

    implicit none

    real :: &
        dx, &
        r

    real, allocatable, dimension(:) :: &
        x, &
        derivative

    integer :: &
        i, &
        nx, &
        deriv_flag, &
        npt

    real :: &
            start_time, &
            end_time

    ! procedure(), pointer :: deriv

    nx = 100000
    deriv_flag = 1
    dx = 10.0
    npt = 100000


    allocate(x(nx), derivative(nx))

    call random_number(x)

    !------------------------------------------------
    ! Flag 
    call cpu_time(start_time)

    do i = 1, npt

        if (deriv_flag == 1) then 
                
            call compute_derivative_n1(x, dx,derivative)
            
        endif 

    enddo

    call cpu_time(end_time)

    print*, 'Time for if statement: ', end_time-start_time

    !------------------------------------------------
    ! Pointer
    call cpu_time(start_time)

    deriv => compute_derivative_n1

    do i = 1, npt
    
        call deriv(x,dx,derivative)
    
    enddo
    
    call cpu_time(end_time)

    print*, 'Time for pointer: ', end_time-start_time

    !------------------------------------------------
    ! interface
    call cpu_time(start_time)

    call compute_derivative(x, dx, derivative)

    call cpu_time(end_time)

    print*, 'Time for interface: ', end_time - start_time

    
end program point_function_comp