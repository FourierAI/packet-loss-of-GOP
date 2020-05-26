#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     dfr_simulation.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2020-05-15
#
# @brief Skeleton code for the simulation of video streaming to investigate the
#        impact of packet losses on the quality of video streaming based on
#        decodable frame rate (DFR)
#


import argparse
import math
import sys
import numpy as np
import sgm_generate as sgm


def dfr_simulation(num_frames, loss_model, loss_probability, video_trace, fec,
                   trace):
    # initialize variables
    num_frames_decoded = 0
    num_frames_received = 0

    # main loop
    with open(video_trace, "r") as f:
        while (num_frames_received < num_frames):
            line = f.readline()
            if line[0] == '#':
                continue  # ignore comments

            # take frame number, type and size from the line
            f_info = line.split()
            f_number = int(f_info[0])  # str -> int
            f_type = f_info[2]
            f_size = int(f_info[3])  # str -> int
            num_pkts = math.ceil(f_size / (188 * 8))
            num_frames_received += 1

            # symbol loss sequences
            if loss_model == 'uniform':
                if trace is True:
                    print("{0:d}: generating symbol loss sequences based on uniform loss model...".format(
                        num_frames_received))

                # TODO: Implement.
                randomvalues = np.random.uniform(0, 1, (num_pkts, 188))

                symbols = np.int32(randomvalues <= loss_probability)

            elif loss_model == 'sgm':
                if trace is True:
                    print("{0:d}: generating symbol loss sequences based on SGM...".format(num_frames_received))

                # TODO: Implement.
                pl = loss_probability
                p = 0.03
                q = p * (1 - pl) / pl
                tr = np.array([[1 - p, q], [p, 1 - q]])
                symbols = []
                for i in range(num_pkts):
                    packet = sgm.sgm_generate(188, tr)
                    symbols.append(packet)
                symbols = np.array(symbols)
            else:
                print("{0:d}: loss model {1:s} is unsupported. existing...".format(loss_model, num_frames_received))
                sys.exit()

            # packet loss sequences
            frame_loss = False
            for i in range(num_pkts):

                # TODO: Extract the loss sequences corresponding to the current
                # packet
                packet = symbols[i, :]
                if fec is True:
                    # The bit can be corrected
                    t = 8
                    if trace is True:
                        print("{0:d}: applying FEC to symbol loss sequences...".format(num_frames_received))

                    # TODO: Implement
                    count = 0

                    for j, symbol in enumerate(packet):
                        if count >= t:
                            break
                        if symbol == 1:
                            packet[j] = 0
                            count += 1
                    symbols[i, :] = packet

            # TODO: set frame_loss to True if there is any symbol loss
            if 1 in symbols:
                frame_loss = True

            # frame decodability
            if frame_loss is False:
                if trace is True:
                    print("{0:d}: deciding decodability of the frame...".format(num_frames_received))

                # TODO: Decide whether the current frame is decodable; if so,
                # increase num_frames_decoded by 1.
                num_frames_decoded += 1

    return num_frames_decoded / num_frames_received  # DFR


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-N",
        "--num_frames",
        help="number of frames to simulate; default is 1000",
        default=1000,
        type=int)
    parser.add_argument(
        "-M",
        "--loss_model",
        help="loss model ('uniform' or 'sgm'; default is 'uniform'",
        default='uniform',
        type=str)
    parser.add_argument(
        "-P",
        "--loss_probability",
        help="overall loss probability; default is 0.1",
        default=0.1,
        type=float)
    parser.add_argument(
        "-V",
        "--video_trace",
        help="video trace file; default is 'terminator2_verbose'",
        default="terminator2_verbose",
        type=str)
    # forward error correction (FEC); default is False (i.e., not using FEC)
    parser.add_argument('--fec', dest='fec', action='store_true')
    parser.add_argument('--no-fec', dest='fec', action='store_false')
    parser.set_defaults(trace=False)
    # trace for debugging; default is False (i.e., no trace)
    parser.add_argument('--trace', dest='trace', action='store_true')
    parser.add_argument('--no-trace', dest='trace', action='store_false')
    parser.set_defaults(trace=False)
    args = parser.parse_args()

    # set variables using command-line arguments
    num_frames = args.num_frames
    loss_model = args.loss_model
    loss_probability = args.loss_probability
    video_trace = args.video_trace
    fec = args.fec
    trace = args.trace

    # call df_simulation()
    dfr = dfr_simulation(num_frames, loss_model, loss_probability, video_trace,
                         fec, trace)

    print("Decodable frame rate = {0:.4E} [s]\n".format(dfr))
