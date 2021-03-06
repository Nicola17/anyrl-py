"""
Test for learning algorithm utilities.
"""

# pylint: disable=E1129

import unittest

from anyrl.algos.util import masked_mean
import numpy as np
import tensorflow as tf

class TestMask(unittest.TestCase):
    """
    Test the masked_mean() API.
    """
    def test_basic(self):
        """
        Test on a normal set of inputs.
        """
        mean = _masked_mean([0, 1, 0, 1, 1], [2.5, 7, 3, 0.8, 0.9])
        self.assertTrue(np.allclose(mean, np.mean([7, 0.8, 0.9])))

    def test_unusual_values(self):
        """
        Test masking unusual values like nan.
        """
        mean = _masked_mean([0, 1, 0, 1, 1, 0],
                            [np.inf, 7, np.nan, 0.8, 0.9, np.inf])
        self.assertTrue(np.allclose(mean, np.mean([7, 0.8, 0.9])))

def _masked_mean(mask, values):
    """
    Compute the masked mean using TensorFlow.
    """
    with tf.Graph().as_default():
        with tf.Session() as sess:
            mask_ph = tf.placeholder(tf.float32, shape=(None,))
            values_ph = tf.placeholder(tf.float32, shape=(None,))
            mean = masked_mean(mask_ph, values_ph)
            return sess.run(mean, feed_dict={mask_ph: np.array(mask),
                                             values_ph: np.array(values)})

if __name__ == '__main__':
    unittest.main()
