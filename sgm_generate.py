#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     sgm_generate.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2020-03-25
#
# @brief    A function for generating loss pattern based on simple Guilbert model.
#

import numpy as np
import sys


def sgm_generate(len, tr):
    """
    Generates a binary sequence of 0 (GOOD) and 1 (BAD) of length
    len from an SGM specified by a 2x2 transition probability matrix
    tr; tr[i, j] is the probability of transition from state i to
    state j.

    This function always starts the model in GOOD (0) state.

    Examples:

    import numpy as np

    tr = np.array([[0.95, 0.10],
                   [0.05, 0.90]])
    seq = sgm_generate(100, tr)
    """

    seq = np.zeros(len)

    # tr must be 2x2 matrix
    tr = np.asarray(tr)  # make sure seq is numpy 2D array
    if tr.shape != (2, 2):
        sys.exit("size of transition matrix is not 2x2")

    # create a random sequence for state changes
    statechange = np.random.rand(len)

    # Assume that we start in GOOD state (0).
    state = 0

    # main loop
    for i in range(len):
        if statechange[i] > tr[state, state]:
            # transition into the other state
            state ^= 1
        # add a binary value to output
        seq[i] = state

    return seq


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L",
        "--length",
        help="the length of the loss pattern to be generated; default is 10",
        default=10,
        type=int)
    parser.add_argument(
        "-T",
        "--transition",
        help="transition matrix in row-major order; default is \"0.95,0.10,0.05,0.90\"",
        default="0.95,0.10,0.05,0.90",
        type=str)
    args = parser.parse_args()
    len = args.length
    tr = np.reshape(np.fromstring(args.transition, sep=','), (2, 2))
    print(sgm_generate(len, tr))
