#!/usr/bin/python

import os, sys
import buffer_data.wmclib as objbuff


class _data_buff(object):

    """**Data buffer class:**

    .. _dbuffer_cls:

    :platform: Unix, Windows
    :synopsis: buld-in plots based on pyTikZ

    :properties:
        Available plots:
            * Racime
            * Vertical bars plots

    **Chracteristics of the data buffer object**

        * Contain a buffer with channels data

    """

    def __init__(self, parent):

        self.parent = parent
        self.aux_def = "_#aux#_"
        pass

    def load_empty_dbuff(self, N):

        """
        .. _dbuffer_load_empty:

        **Synopsis:**
            * Load an empty data bufferr of channels of a length of N

        **Args:**
            * N: length of the channels

        **Optional parameters:**
            * None

        **Returns:**
            * A data buffer object

        **Usage**

            * Empty

        """

        if N < 1: self.parent.error("data_buffer N<0", ref = "_data_buff")

        dbuff = objbuff.wmc_data()
        dbuff.allocate(N)

        return dbuff
