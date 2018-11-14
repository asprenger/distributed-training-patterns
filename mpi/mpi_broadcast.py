from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    # create a data array on process 0
    numData = 10  
    data = np.linspace(0.0, 3.14, numData)
else:
    numData = None

# broadcast numData and allocate array on other ranks:
numData = comm.bcast(numData, root=0)
if rank != 0:    
    data = np.empty(numData, dtype='d')  

comm.Bcast(data, root=0) # broadcast the array from rank 0 to all others

print('Rank: ',rank, ', data received: ',data)