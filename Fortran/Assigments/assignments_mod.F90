module assignments 

    implicit none 

    public:: direct, allocation

    contains

    subroutine direct_do(x, x_copy)

        !- INPUTS -!
        real, allocatable, intent(inout) :: &
            x(:)

        real, allocatable, intent(inout) :: &
            x_copy(:)

        !- Local variable -!
        integer :: &
            nx, &
            i

        real :: &
            start_time, &
            end_time
        
        call cpu_time(start_time)
        
        nx = size(x)

        do i = 1, nx
            x_copy(i) = x(i)
        enddo

        call cpu_time(end_time)

        print*, 'Time for direct-do copy: ', end_time - start_time


    end subroutine direct_do

    subroutine direct(x, x_copy)

        !- INPUTS -!
        real, allocatable, intent(inout) :: &
            x(:)

        real, allocatable, intent(inout) :: &
            x_copy(:)

        !- Local variable -!
        integer :: &
            nx, &
            i

        real :: &
            start_time, &
            end_time
        
        call cpu_time(start_time)
        
        x_copy = x

        call cpu_time(end_time)

        print*, 'Time for direct copy: ', end_time - start_time


    end subroutine direct


    subroutine allocation(x, x_copy)

        real, allocatable, intent(inout) :: &
            x(:)

        real, allocatable, intent(out) :: &
            x_copy(:)

        real :: &
            start_time, &
            end_time
        
        call cpu_time(start_time)

        call move_alloc(x, x_copy)

        call cpu_time(end_time)

        print*, 'Time for moving allocation: ', end_time - start_time


    end subroutine allocation


end module assignments 

