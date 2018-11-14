from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    message = {'a': 10, 'b': 1.234, 'c': 'foobar'}
    print('Process 0: sending', message)
    comm.send(message, dest=1)
elif rank == 1:
    message = comm.recv(source=0)
    print('Process 1: received', message)