
import numpy as np
import tensorflow as tf
import horovod.tensorflow as hvd

hvd.init()
size = hvd.size()
rank = hvd.rank()

tensor = tf.Variable(np.array([1.0,1.0,1.0], dtype=np.float32) * rank, name = 'tensor')
assign_op = tf.assign(tensor, np.array([99.0, 99.0, 99.0]))

# An op which broadcasts all tensors on root rank to the same tensors
# on all other Horovod processes.
broadcast_op = hvd.broadcast_global_variables(0)

# The operation will not start until all processes are ready 
# to receive the tensor.

with tf.Session() as sess:

    sess.run(tf.global_variables_initializer())
    print("rank %d before broadcast: %s" % (rank, sess.run(tensor)))

    if rank == 0:
        sess.run(assign_op)

    sess.run(broadcast_op)
    print("rank %d after broadcast: %s" % (rank, sess.run(tensor)))
    # => [99. 99. 99.]
