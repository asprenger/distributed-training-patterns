import os
import socket
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create some np arrays on each process
value = np.array(rank, 'd')

process_id = '%s@%s' % (os.getpid(), socket.gethostname())

print(process_id, 'Rank', rank, 'value=', value)

# initialize some buffers that will receive the result
value_sum = np.array(0.0, 'd')
value_max = np.array(0.0, 'd')

# perform the reductions:
comm.Allreduce(value, value_sum, op=MPI.SUM)
comm.Allreduce(value, value_max, op=MPI.MAX)

print('Rank', rank, 'value_sum=', value_sum)
print('Rank', rank, 'value_max=', value_max)