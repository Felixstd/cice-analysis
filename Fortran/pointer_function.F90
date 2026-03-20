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
        deriv_flag

    real :: &
            start_time, &
            end_time

    ! procedure(), pointer :: deriv

    nx = 1000
    deriv_flag = 1
    dx = 10.0

    allocate(x(nx), derivative(nx))

    call random_number(x)

    call cpu_time(start_time)

    if (deriv_flag == 1) then 
        call compute_derivative_n1(x, dx,derivative)
    endif 

    call cpu_time(end_time)

    print*, 'Time for if statement: ', start_time-end_time

    call cpu_time(start_time)

    deriv => compute_derivative_n1
    
    call deriv(x,dx,derivative)
    
    call cpu_time(end_time)

    print*, 'Time for pointeR: ', start_time-end_time



    
end program point_function_comp