from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create some np arrays on each process:
value = np.array(rank,'d')

print(' Rank: ',rank, ' value = ', value)

# initialize the np arrays that will store the results:
value_sum      = np.array(0.0,'d')
value_max      = np.array(0.0,'d')

# perform the reductions:
comm.Reduce(value, value_sum, op=MPI.SUM, root=0)
comm.Reduce(value, value_max, op=MPI.MAX, root=0)

if rank == 0:
    print(' Rank 0: value_sum =',value_sum)
    print(' Rank 0: value_max =',value_max)