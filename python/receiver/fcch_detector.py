#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: FCCH Bursts Detector
# Author: Piotr Krysik
#
# Description: Detects positions of FCCH bursts. At the end of each 
# detected FCCH burst adds to the stream a tag with key "fcch" and value 
# which is a frequency offset estimate. The input sampling frequency 
# should be integer multiply of GSM GMKS symbol rate - 1625000/6 Hz.
##################################################

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import grgsm

class fcch_detector(gr.hier_block2):

    def __init__(self, OSR=4):
        gr.hier_block2.__init__(
            self, "FCCH bursts detector",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.OSR = OSR

        ##################################################
        # Variables
        ##################################################
        self.f_symb = f_symb = 1625000.0/6.0
        self.samp_rate = samp_rate = f_symb*OSR

        ##################################################
        # Blocks
        ##################################################
        self.gsm_fcch_burst_tagger_0 = grgsm.fcch_burst_tagger(OSR)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(0, 0, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(int((138)*samp_rate/f_symb), int((138)*samp_rate/f_symb), 0)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int((142)*samp_rate/f_symb), 1, int(1e6))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, int(OSR))
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.gsm_fcch_burst_tagger_0, 0), (self, 0))
        self.connect((self, 0), (self.gsm_fcch_burst_tagger_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.gsm_fcch_burst_tagger_0, 1))

    def get_OSR(self):
        return self.OSR

    def set_OSR(self, OSR):
        self.OSR = OSR
        self.set_samp_rate(self.f_symb*self.OSR)
        self.blocks_delay_0.set_dly(int(self.OSR))


