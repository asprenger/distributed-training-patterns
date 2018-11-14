import numpy as np
import tensorflow as tf
import horovod.tensorflow as hvd

hvd.init()
size = hvd.size()
rank = hvd.rank()

tensor = tf.Variable(np.array([1,2,3], dtype=np.float32)+rank, name = 'tensor')

# An op that sums the tensor with the same tensor on
# all other Horovod processes.
summed = hvd.allreduce(tensor, average=False)

# An op that averages the tensor with the same tensor on
# all other Horovod processes.
averaged = hvd.allreduce(tensor, average=True)

# The reduction will not start until all processes are ready 
# to send and receive the tensor.

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print("sum:", sess.run(summed))
    # => [3. 5. 7.]
    print("average:", sess.run(averaged))
    # => [1.5 2.5 3.5]
