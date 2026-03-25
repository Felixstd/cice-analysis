module point_functions

    implicit none 

    public::compute_derivative_n1, compute_derivative_n2

    ! contains

    abstract interface
    subroutine deriv_interface(x, dx, derivative)

         real, allocatable, intent(in) :: &
            x(:)

        real, intent(in) :: &
            dx

        real, allocatable, intent(out) :: &
            derivative(:)

    end subroutine

    end interface

    procedure(deriv_interface), pointer :: deriv => null()


    interface compute_derivative
        module procedure compute_derivative_n1
        module procedure compute_derivative_n2
    end interface 

    contains

    subroutine compute_derivative_n1(x, dx, derivative)

         real, allocatable, intent(in) :: &
            x(:)

        real, intent(in) :: &
            dx

        real, allocatable, intent(out) :: &
            derivative(:)


        integer :: &
            n_x, &
            i

        n_x =  size(x)
        allocate(derivative(n_x))

        do i = 2, n_x

            derivative(i) = (x(i) - x(i-1))/dx
            
        enddo
    end subroutine compute_derivative_n1

    subroutine compute_derivative_n2(x, dx, derivative, n)

        real, allocatable, intent(in) :: &
            x(:)

        real, intent(in) :: &
            dx

        real, allocatable, intent(out) :: &
            derivative(:)


        integer :: &
            n  , &
            n_x, &
            i

        n_x =  size(x)

        do i = 2, n_x-1

            derivative(i) = (x(i+1) - x(i-1))/(2d0*dx)

        enddo


    end subroutine compute_derivative_n2

end module point_functions
        
