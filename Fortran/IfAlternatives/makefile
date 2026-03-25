FC = gfortran
FFLAGS = -O2 -Wall

my_program: pointer_funtion_mod.o pointer_function.o
	$(FC) $(FFLAGS) pointer_funtion_mod.o pointer_function.o -o my_program

pointer_funtion_mod.o: pointer_funtion_mod.F90
	$(FC) $(FFLAGS) -c pointer_funtion_mod.F90

pointer_function.o: pointer_function.F90 pointer_funtion_mod.o
	$(FC) $(FFLAGS) -c pointer_function.F90

clean:
	rm -f *.o *.mod my_program
