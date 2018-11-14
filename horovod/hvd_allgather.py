import numpy as np
import tensorflow as tf
import horovod.tensorflow as hvd

hvd.init()
size = hvd.size()
rank = hvd.rank()

tensor = tf.Variable(np.array([1.0,1.0,1.0], dtype=np.float32) * rank, name = 'tensor')

# An op that concatenates the tensor with the same tensor on
# all other Horovod processes.
allgather_op = hvd.allgather(tensor)

# The operation will not start until all processes are ready 
# to send and receive the tensor.

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(allgather_op))
    # => [0. 0. 0. 1. 1. 1.]
    