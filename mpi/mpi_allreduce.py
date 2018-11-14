import os
import socket
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create some np arrays on each process
value = np.array(rank+1, 'd')

process_id = '%s@%s' % (os.getpid(), socket.gethostname())

print(process_id, 'Rank', rank, 'value=', value)

# initialize some buffers that will receive the result
value_min = np.array(0.0, 'd')
value_max = np.array(0.0, 'd')
value_sum = np.array(0.0, 'd')

# perform the reductions:
comm.Allreduce(value, value_min, op=MPI.MIN)
comm.Allreduce(value, value_max, op=MPI.MAX)
comm.Allreduce(value, value_sum, op=MPI.SUM)

print('Rank', rank, 'value_min=', value_min)
print('Rank', rank, 'value_max=', value_max)
print('Rank', rank, 'value_sum=', value_sum)