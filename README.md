# Installations

## Install OpenMPI from source

Install OpenMPI to `/usr/local`:

	wget https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-3.1.2.tar.gz
	tar xzf openmpi-3.1.2.tar.gz
	cd openmpi-3.1.2
	make all
	sudo make install

Executing `mpirun` requires setting `LD_LIBRARY_PATH`:

	export LD_LIBRARY_PATH=/usr/local/lib

## Install mpi4py

MPI for Python provides MPI bindings for Python. Check out the docs: [MPI for Python](https://mpi4py.readthedocs.io/en/stable/).

Install module:

	pip install mpi4py

## Install NCCL

    tar -xvf  nccl_2.2.12-1+cuda9.0_x86_64.txz
    sudo mkdir /usr/local/nccl-2.2.12
    sudo cp -r nccl_2.2.12-1+cuda9.0_x86_64/* /usr/local/nccl-2.2.12

Create a file `/etc/ld.so.conf.d/nccl.conf` with content:

    /usr/local/nccl-2.2.12/lib

Run `ldconfig` to update `LD_LIBRARY_PATH`:

    sudo ldconfig 

Create symbolic link for NCCL header file:

    sudo ln -s /usr/local/nccl-2.2.12/include/nccl.h /usr/include/nccl.h

## Install Horovod

Here is the link to the [Horovod docs](https://github.com/uber/horovod/tree/master/docs)

For installation on machines with GPUs read this: [Horovod GPU page](https://github.com/uber/horovod/blob/master/docs/gpus.md)

Install Horovod with NCCL support:

    HOROVOD_NCCL_HOME=/usr/local/nccl-2.2.12 HOROVOD_GPU_ALLREDUCE=NCCL pip install --no-cache-dir horovod


# OpenMPI examples

Create a file `myhosts` with text:

	127.0.0.1 slots=4

**Note:** you might need to add --prefix argument to mpirun like this:

	--prefix /usr/local

## Point to point

Send data from one process to another.

	mpirun -np 2 --hostfile myhosts --mca btl self,tcp python mpi_point_to_point.py

## Broadcasting

Broadcasting takes a variable and sends an exact copy of it to all processes.

	mpirun -np 4 --hostfile myhosts --mca btl self,tcp python mpi_broadcast.py
	> Rank:  0 , data received:  [0. 0.34888889 0.69777778 1.04666667 1.39555556 1.74444444 2.09333333 2.44222222 2.79111111 3.14 ]
	> Rank:  1 , data received:  [0. 0.34888889 0.69777778 1.04666667 1.39555556 1.74444444 2.09333333 2.44222222 2.79111111 3.14 ]
	> Rank:  2 , data received:  [0. 0.34888889 0.69777778 1.04666667 1.39555556 1.74444444 2.09333333 2.44222222 2.79111111 3.14 ]
	> Rank:  3 , data received:  [0. 0.34888889 0.69777778 1.04666667 1.39555556 1.74444444 2.09333333 2.44222222 2.79111111 3.14 ]
 	
## Scattering

Scatter takes an array and distributes contiguous sections of it to different processes. 

	mpirun -np 4 --hostfile myhosts --mca btl self,tcp python mpi_scatter.py
	> Rank:  0 , recvbuf received:  [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
	> Rank:  1 , recvbuf received:  [11. 12. 13. 14. 15. 16. 17. 18. 19. 20.]
	> Rank:  2 , recvbuf received:  [21. 22. 23. 24. 25. 26. 27. 28. 29. 30.]
	> Rank:  3 , recvbuf received:  [31. 32. 33. 34. 35. 36. 37. 38. 39. 40.]


## Gathering

The reverse of a scatter is a gather, which takes subsets of an array that are distributed across the processes, 
and gathers them back into the full array.

	mpirun -np 4 --hostfile myhosts --mca btl self,tcp python mpi_gather.py
	> Rank:  0 , sendbuf:  [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
	> Rank:  1 , sendbuf:  [11. 12. 13. 14. 15. 16. 17. 18. 19. 20.]
	> Rank:  2 , sendbuf:  [21. 22. 23. 24. 25. 26. 27. 28. 29. 30.]
	> Rank:  3 , sendbuf:  [31. 32. 33. 34. 35. 36. 37. 38. 39. 40.]
	> Rank:  0 , recvbuf received:  [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10. 11. 12. 13. 14. 15. 16. 17. 18. 19. 20. 21. 22. 23. 24. 25. 26. 27. 28. 29. 30. 31. 32. 33. 34. 35. 36. 37. 38. 39. 40.]


## Reduce

The reduce operation takes values in from an array on each process and reduces them to a single result on the root process.

	mpirun -np 4 --hostfile myhosts --mca btl self,tcp python mpi_reduce.py
	> Rank:  0  value =  0.0
	> Rank:  1  value =  1.0
	> Rank:  2  value =  2.0
	> Rank:  3  value =  3.0
	> Rank 0: value_sum = 6.0
	> Rank 0: value_max = 3.0

## Allreduce

The allreduce operation takes values in from an array on each process, reduces them to a single result and sends the result 
to each process. Note that the communication pattern is much more complex compared to the reduce operation.

	mpirun -np 4 --hostfile myhosts --mca btl self,tcp python mpi_allreduce.py
	> Rank  0 value= 0.0
	> Rank  1 value= 1.0
	> Rank  2 value= 2.0
	> Rank  3 value= 3.0
	> Rank 0 value_sum= 6.0
	> Rank 0 value_max= 3.0
	> Rank 1 value_sum= 6.0
	> Rank 2 value_sum= 6.0
	> Rank 2 value_max= 3.0
	> Rank 3 value_sum= 6.0
	> Rank 3 value_max= 3.0
	> Rank 1 value_max= 3.0
