program assignment_comparison

    use assignments, only: direct, allocation, direct_do

    implicit none

    real, allocatable :: &
        x(:), &
        x_copy(:)

    integer :: &
        size_x, i

    
    size_x = int(10000)

    
    allocate(x(size_x), x_copy(size_x))

    call random_number(x)

    call direct(x, x_copy)

    call direct_do(x,x_copy)

    deallocate(x_copy)

    call allocation(x, x_copy)


end program assignment_comparison
    