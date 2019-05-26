
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import scipy.signal

import scipy.optimize
import struct
from copy import copy, deepcopy
import string
# import math
import os
import time as time
import datetime
import os.path
import re
import sys
import pickle

# from scipy.optimize import leastsq

# ==== lib Greeeting & initial stuff =============================
# ===================================================================

version = '2014-02-18'
#version = ' ** nrfslib unstable ** '

print ''
print '================================='
print 'nrfslib loaded, version',version
print '================================='
print ''
# change some general settings of matplotlib
# these changes can be reset with plt.rcdefaults()
plt.rcdefaults()
plt.ion()

#plt.rcParams['font.sans-serif']      = ['Roman']
#plt.rcParams['font.family']          = 'sans-serif'
plt.rcParams['font.size']            = '14.0'
plt.rcParams['figure.figsize']       = '11.6929134, 8.26771654'    # A4
#plt.rcParams['figure.subplot.left']  = '0.1'
plt.rcParams['figure.subplot.right'] = '0.975'
plt.rcParams['savefig.dpi']          = '300'
#plt.rcParams['savefig.facecolor']    = 'lightgrey'
plt.rcParams['legend.fontsize']      = 'small'
plt.rcParams['legend.fancybox']      = 'True'
plt.rcParams['legend.numpoints']     = '1'
plt.rcParams['axes.grid']            = 'True'
plt.rcParams['grid.linestyle']       = ':'
#plt.rcParams['backend']              = 'TkAgg' werkt niet ???
plt.rcParams['mathtext.default']     = 'regular'
#plt.rcParams['path.simplify']        = 'False'

# change the default color cycle for the plot
# the matplotlib defualt cycles 8 colors
# this is changed to the 16 colors also used in grafx
# (standard web-color names are valid for matplotlib)
#from matplotlib.axes import set_default_color_cycle
nrfs_default_colors = ['red',
                      'green',
                      'blue',
                      'black',
                      'orange',
                      'purple',
                      'grey',
                      'cyan',
                      'magenta',
                      'brown',
                      'olive',
                      'maroon',
                      'lime',
                      'teal',
                      'navy']

# Changing the default color cycle is a bit difficult with different
# version of Matplotlib, anyway we try two methods and print and error
# message if we do not succeed

colors_oke = False
try:
    plt.rcParams['axes.color_cycle'] = nrfs_default_colors
    colors_oke = True
except:
    pass
try:
    set_default_color_cycle(nrfs_default_colors)
    colors_oke = True
except:
    pass
try:
    matplotlib.axes.set_default_color_cycle(nrfs_default_colors)
    colors_oke = True
except:
    pass

if not colors_oke :
    print ''
    print 'WARNING: something went wrong with the colors.'
    print '         please update Python(X,Y), matplotlib etc...'
    print ''
    nrfs_default_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# default markers cycle, used in add_marker
nrfs_default_markers = ['s','^','o','v','x','D','*','+','H',
                       '<','>','d','p','1','2','3','4','h']


# see also: http://www.python.org/dev/peps/pep-0234/ 'some folks...'
class bidirectional_cyclic_iterator(object):
    def __init__(self, collection):
        self.collection = copy(collection)
        self.length = len(collection)
        self.index = None

    def next(self):
        if self.index == None:
            self.index = 0
        else:
            self.index = (self.index + 1) % self.length
        return self.collection[self.index]

    def prev(self):
        if self.index == None:
            self.index = self.length - 1
        else:
            self.index = (self.index - 1) % self.length
        return self.collection[self.index]

    def current(self):
        if self.index == None:
            self.index = 0
        else:
            self.index = (self.index) % self.length
        return self.collection[self.index]

    def reset(self):
        self.index = None

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        return self.collection[i]

colors = bidirectional_cyclic_iterator(nrfs_default_colors)
markers = bidirectional_cyclic_iterator(nrfs_default_markers)


# ==== nrfslib Data Class ============================================
# ===================================================================

class nrfs_data(object):
    """
    The nrfs_data object is an object where the measurement signals of
    the BFG and Blatest datafiles (.buf, .dfx, .dat, .dmp, .st3) are
    stored.

    The preferred way to access the data is using label indices as shown here::

        meas = nrfs.load_dmp('./path/to/file.dmp')
        plt.plot(meas['F01'], meas['001S120'])

    A nrfs_data object is loaded with measurement data by use of one of the
    load_xxx functions

    Members:

        *chn* - dictionary with arrays with measurement data

        *file_name* - original file name

        *file_type* - type of original file ['buf'|'dfx'|'dmp'|'st3'|'nrfss']

        *file_date* - date as string as recorded in the data file

        *file_time* - time as string as recorded in the data file

        *dumpratio* - Blatest .dmp dumpratio

        *station* - Blatest station number

    """

    def __init__(self, inNpnt=0):
        """
        initialize the nrfs_data object
        """
        self.allocate(inNpnt)
        self.file_name = ''
        self.file_type = ''
        self.file_date = ''
        self.file_time = ''
        self.dumpratio = 1
        self.station   = 0

    def allocate(self,inNpnt):
        """
        allocate (only for internal use)
        """
        self.chn = {}
        self.Npnt = inNpnt;
        self.Nchn = 0;

    def shrink_to(self,inNpnt):
        """
        resize (only for internal use)
        """
        print '[shrink_to] doet het nog niet'
        pass

    def add_pnt(self,inPntStep):
        """
        add points (only for internal use)
        """
        print '[add_pnt] doet het nog niet'
        pass

    # functions to make nrfs_data act as a dictionary
    def __getitem__(self,label):
        '''
        for emulating container type
        '''
        return self.chn[label]

    def __delitem__(self,label):
        '''
        for emulating container type
        '''
        del self.chn[label]

    def __setitem__(self,label, value):
        '''
        for emulating container type
        '''
        # sanity check is value an array of correct size.....
        if not type(value) == np.ndarray:
            raise ValueError, 'Only 1D numpy array of correct length ' +\
                              'can be added to a nrfs_data object'
        if not value.shape == (self.Npnt,):
            raise ValueError, 'Only 1D numpy array of correct length ' +\
                              'can be added to a nrfs_data object'
        if (not label in self.chn.keys()):
            #print 'creation of channel \'%s\'' % label
            self.chn[label] = value
            self.Nchn = len(self.chn)
        else:
            self.chn[label] = value

    def __iter__(self):
        '''
        for emulating container type, define iterator
        '''
        return self.chn.__iter__()

    def iteritems(self):
        '''
        m.iteritems() -> an iterator over the (label, data) items of m
        '''
        return self.chn.iteritems()

    def keys(self):
        '''
        for emulating container type
        '''
        return self.chn.keys()

    def values(self):
        '''
        for emulating container type
        '''
        return self.chn.values()

    def info(self):
        """
        print some information of this nrfs_data object
        """
        print 'Npnt        : ', self.Npnt
        print 'Nchn        : ', self.Nchn
        print 'file_name   : ', self.file_name
        print 'file_type   : ', self.file_type
        print 'file_date   : ', self.file_date
        print 'file_time   : ', self.file_time
        print 'dumpratio   : ', self.dumpratio
        print 'station     : ', self.station

    def masked_copy(self,inMask):
        """
        Returns a new nrfs_data object with masked applied

        Arguments:
            *inMask* - np.ndarray of Booleans
        """

        # create a new data object
        wd = nrfs_data()
        wd.allocate(np.sum(inMask))
        wd.file_name = 'masked copy of %s' % self.file_name
        wd.file_type = self.file_type
        wd.file_date = self.file_date
        wd.file_time = self.file_time
        wd.dumpratio = self.dumpratio
        wd.station   = self.station

        # copy the stuff
        for ch in self:
            wd[ch] = copy(self[ch][inMask])

        # return the newly created nrfs_data object
        return wd

    def copy(self):
        """
        Returns a copy of the nrfs_data object.
        """
        return deepcopy(self)

    def save_xls(self,inName,inOptions=''):
        """
        save the data of the nrfs_data object into an .xls file
        """

        # version 0.7.2 or higher required
        from xlwt import Workbook,easyxf

        def write_column(innrfsData,inWS,inName,inColumnNo):
            # 'borders: bottom medium;',
            inWS.write(0,inColumnNo,inName,
                easyxf('borders: bottom medium; '+
                       'pattern: pattern solid, fore_colour light_yellow;'))
            row = 1
            for val in innrfsData[inName]:
                # hmm, xlwt.Workbook.write, kent geen numpy.int64, vieze hack..
                if type(val) == np.int64:
                    val = int(val)
                inWS.write(row,inColumnNo,val)
                row += 1

        # worksheet_name = self.file_name
        # if worksheet_name == '': worksheet_name = 'nrfs_data'
        worksheet_name = 'nrfs_data'
        wb = Workbook('cp1252')
        ws = wb.add_sheet(worksheet_name)

        # write columns
        col = 0
        # for ch in np.sort(self.keys()): // gives errors, therefore...:
        k = copy(self.keys())
        k.sort()
        for ch in k:
            write_column(self,ws,ch,col)
            col += 1

        wb.save(inName+'.xls')

    def save_txt(self, inName, inSeperator=''):
        """
        save the data of the nrfs_data object into an .txt file
        """

        # first column record, then other data (and record again..)
        txt_columns = []
        txt_columns.append({'format' : '%d',
                            'label'  : 'record',
                            'width'  : 10})
        for ch in self:
            col_width = max(16,len(ch)+1)
            if   self[ch].dtype == np.dtype('int32'):
                col_format = '%d'
            elif self[ch].dtype == np.dtype('int64'):
                col_format = '%d'
            elif self[ch].dtype == np.dtype('float64'):
                col_format = '%15.4e'
            elif self[ch].dtype == np.dtype('bool'):
                col_format = '%d'
            else:
                raise ValueError, 'Unknown type'
            txt_columns.append({'format' : col_format,
                                'label'  : ch,
                                'width'  : col_width})

        # open file
        f = open(inName,'w')

        # write header
        for col in txt_columns:
            f.write(string.rjust(col['label'],col['width']))
            f.write(inSeperator)
        f.write('\n')

        # write_data
        for i in range(self.Npnt):
            for col in txt_columns:
                f.write(string.rjust(col['format'] %
                                     self[col['label']][i],
                                     col['width']))
                f.write(inSeperator)
            f.write('\n')

        # close file
        f.close()

    def save_nrfss(self, inName):
        """
        Save data in nrfsS format.

        For now is saves only the float channels
        """

        # some 'constants', block identifiers
        BT_nrfsS_IDENTIFIER  =  0
        BT_CHN_COUNT        = 20
        BT_CHANNEL_LABEL    = 100
        BT_DATA_RECORDS     = 200

        # we don't want to save and empty file
        if self.Npnt <= 0:
            raise ValueError('Cannot save an empty nrfs_data object')

        # find the float channels
        f_chns = [ch for ch in self if self[ch].dtype == np.float
                                    and not ch == 'unixtime']

        # check if some of the special channels are available
        has_scantime = 'scantime' in self and self['scantime'].dtype == np.int64
        has_unixtime = 'unixtime' in self and self['unixtime'].dtype == np.float
        has_status   = 'status'   in self and self['status'].dtype   == np.int64
        has_counter  = 'counter'  in self and self['counter'].dtype  == np.int64

        # open file
        f = open(inName,'wb')

        f.write(struct.pack('ii', BT_nrfsS_IDENTIFIER, 4))
        f.write('nrfsS')

        f.write(struct.pack('iii', BT_CHN_COUNT, 4, len(f_chns)))

        for i, ch in enumerate(f_chns):
            f.write(struct.pack('iii', BT_CHANNEL_LABEL, len(ch)+4, i))
            f.write(ch)

        for i in range(self.Npnt):
            f.write(struct.pack('ii', BT_DATA_RECORDS, len(f_chns) * 4 + 40))
            for ch in f_chns:
                f.write(struct.pack('f', self[ch][i]))

            # store 'special' channels if available
            tmp = np.int64(0)
            if has_scantime: tmp = self['scantime'][i]
            f.write(struct.pack('q', tmp))

            tmp1 = np.int64(0)
            tmp2 = np.int64(0)
            if has_unixtime:
                tmp1 = np.int64(np.modf(self['unixtime'][i])[1])
                tmp2 = np.int64(np.modf(self['unixtime'][i])[0]* 1.0e9)
            f.write(struct.pack('q', tmp1))
            f.write(struct.pack('q', tmp2))

            tmp = np.int64(0)
            if has_status: tmp = self['status'][i]
            f.write(struct.pack('q', tmp))

            tmp = np.int64(0)
            if has_counter: tmp = self['counter'][i]
            f.write(struct.pack('q', tmp))

        # close file
        f.close()


# ==== nrfslib General Functions =====================================
# ===================================================================

def isFloat(s):
    """
    Returns a Boolean to indicate if *s* can be converted to a float
    """
    try: float(s)
    except (ValueError, TypeError): return False
    else: return True

def nans(shape, dtype=None, order='C'):
    """
    Return a matrix of given shape and type, filled with NaNs

    (based on code of np.zeros and np.ones)
    """
    a = np.ndarray.__new__(np.ndarray, shape, dtype, order=order)
    a.fill(np.NaN)
    return a


# ==== nrfslib Data Functions
# ===================================================================

def load_channels(inFile,inOptions=''):
    """
    Interprets a channel.set or bfgdefs.knl file. This function is
    mostly only called from the `load_[buf|dfx|dmp|dat|st3]` functions

    Arguments:
        *inFile*:
            path and filename

        *inOptions*:
            string that can contain the following options
                'v' - verbose, print debug info

    Returns:
        dictionary with the chno as key and as values a tuples with
        chno, callibrationfactor, offset, label
    """

    # check options
    bVerbose     = 'v' in inOptions
    if (bVerbose): print "[load_channels_set] file:",inFile

    # check if file exists
    if not os.path.isfile(inFile) :
        raise ValueError, 'channels file ' + inFile + ' does not exist'

    channels = {}
    fChn = open(inFile,'r')
    for line in fChn:
        if  (line[0]!='#' and line[0:5]!='Kannr') :
            # remove nrfss comments
            line = re.compile(r'\[.*?\]').sub('', line)
            parts = line.split();
            if (len(parts)>=3):
                if (parts[3][0:2]!='nc' and parts[3][0:2]!='NC'):
                    # probably a correct line, lets use it...
                    channels[int(parts[0])] = (int(parts[0]),
                                               float(parts[1]),
                                               float(parts[2]),
                                               parts[3])
    fChn.close()

    if bVerbose :
        for ch in channels.iteritems() :
            print '%4d  %10.4e  %10.4e  %-10s ' % ch[1]

    return channels

def load_dfx(inFile,inOptions=''):
    """
    load a BFG points file (.dfx),
    it assumes that the bfgdefs.knl file is 'sibbling'.

    Arguments:
        *inFile*:
            path and filename

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info
                * 'vv' - even more verbose, print more debug info

    Returns:
        a filled nrfs_data object
    """

    # check options
    bVerbose = 'v' in inOptions
    bVerboseVerbose = 'vv' in inOptions

    if (bVerbose): print "[load_dfx] file:",inFile

    # check if file exists and check if sibbling bfgdefs.knl exists
    (dirName, fileName) = os.path.split(inFile)
    chnFile = os.path.join(dirName,'bfgdefs.knl')

    if not os.path.isfile(inFile) :
        raise ValueError, 'data file '+inFile+' does not exist'
    if not os.path.isfile(chnFile):
        raise ValueError, 'channels file '+chnFile+' does not exist'

    # create new nrfs_data object
    wd = nrfs_data()

    # read channel definition
    cd = load_channels(chnFile,inOptions)

    # open the file and read header as one big chunck
    hs = 1024                        # headersize
    fd = open(inFile,'rb')
    fd.seek(0)
    s = fd.read(hs)

    # retrieve some info from the header
    Nchn           = int(struct.unpack('h',s[6:8])[0])
    wd.file_date   = s[18:26]
    wd.file_time   = s[10:18]
    wd.file_name   = inFile
    wd.file_type   = 'dfx'

    # make an estimate of the number of points based on the file size
    # (there can be non-data points data in the file)
    fs = os.path.getsize(inFile)      # file size
    ds = fs - hs                      # data size
    rs = Nchn * (4 + 2) + 10          # data record size

    Nest = ds/rs                      # estimate Npnt

    # create some temporary arrays
    # wd.allocate(Nchn * 4,Nest)
    # wd.allocate(Nest)
    tmp_data     = np.empty((Nest, Nchn*2))
    tmp_counter  = np.zeros((Nest,), dtype=np.int32)
    tmp_testtime = np.empty((Nest,))

    # local callibration factors and offsets
    lcf = np.ones((Nchn,))
    los = np.zeros((Nchn,))
    print cd
    print cd.values()
    for c in cd.values():
        print c
        if c[0]<Nchn : # bugfix, if there are more channels defined in
                       # bfgdefs.knl than there are in the .dfx file
            lcf[c[0]] = c[1]
            los[c[0]] = c[2]

    Npnt = 0

    while True :
        # read 1 int, it contains the record type, also EOF detection
        s = fd.read(2)
        if len(s) <2 : break ## EOF

        rec_type = int(struct.unpack('h',s[0:2])[0])
        if bVerboseVerbose:
            print 'Npnt : %d, rec_type: %d' % (Npnt,rec_type)

        if rec_type == 10 :
            # text type, print it
            s = fd.read(114)
            print '[load_dfx] text type: ',s[8:34]
            print '[load_dfx] text type: ',s[34:114]

        elif rec_type == 1:
            # callibration factors and offsets
            s = fd.read(Nchn*8)
            for i in range(0,Nchn) :
                lcf[i] = float(struct.unpack('f',s[ 8*i  : 8*i+4 ])[0])
                los[i] = float(struct.unpack('f',s[ 8*i+4: 8*i+8 ])[0])
            if (bVerbose):
                print "[load_dfx] Calibration factor/offset"
                print lcf
                print los

        elif rec_type == 0 :
            # RNG and AVG
            s = fd.read(rs-2)
            if len(s) == (rs-2):
                tmp_counter[Npnt]  = int(struct.unpack('i',s[0:4])[0])
                tmp_testtime[Npnt] = float(struct.unpack('f',s[4:8])[0])
                # AVG (short)
                tmp_data[Npnt,0:Nchn] = \
                    struct.unpack('%dh'%Nchn,s[8+4*Nchn:8+4*Nchn+2*Nchn])
                # RNG (long), no offset in RNG
                tmp_data[Npnt,Nchn:2*Nchn] = \
                    struct.unpack('%di'%Nchn,s[8:8+4*Nchn])
                if bVerboseVerbose:
                    print tmp_counter[Npnt], tmp_testtime[Npnt]
                # apply calfac and offset
                tmp_data[Npnt,0:Nchn] = tmp_data[Npnt,0:Nchn] * lcf + los
                tmp_data[Npnt,Nchn:2*Nchn] = tmp_data[Npnt,Nchn:2*Nchn] * lcf

                Npnt += 1
            else:
                print '[load_dfx] corrupt data at end of .dfx file'

        elif rec_type == 11 :
            if bVerbose:
                print 'record_type 11'
            s = fd.read(rs-2)
            if len(s) == (rs-2):
                tmp_counter[Npnt]  = int(struct.unpack('i',s[0:4])[0])
                tmp_testtime[Npnt] = float(struct.unpack('f',s[4:8])[0])
                # AVG (short)
                tmp_data[Npnt,0:Nchn] =  \
                    np.array(struct.unpack('%dh'%Nchn,s[8+2*Nchn:8+2*Nchn+2*Nchn]),dtype=np.float64)
                # RNG = MAX - MIN
                tmp_data[Npnt,Nchn:2*Nchn] = \
                    np.array(struct.unpack('%dh'%Nchn,s[8+4*Nchn:8+4*Nchn+2*Nchn]),dtype=np.float64) - \
                    np.array(struct.unpack('%dh'%Nchn,s[8+4*Nchn:8+4*Nchn+2*Nchn]),dtype=np.float64)
                # apply calfac and offset
                tmp_data[Npnt,0:Nchn] = tmp_data[Npnt,0:Nchn] * lcf + los
                tmp_data[Npnt,Nchn:2*Nchn] = tmp_data[Npnt,Nchn:2*Nchn] * lcf

                if bVerboseVerbose:
                    print wd.counter[Npnt],wd.testtime[Npnt]
                Npnt += 1
            else:
                print '[load_dfx] corrupt data at end of .dfx file'
        else :
            print '=== rec_type ====>', rec_type
            print '=== Npnt  =======>', Npnt
            raise ValueError, '[load_dfx] Unknown record type'

    fd.close()

    # copy tmp to wd
    wd.allocate(Npnt)
    wd['counter']  = tmp_counter[0:Npnt]
    wd['testtime'] = tmp_testtime[0:Npnt]
    wd['record']   = np.array(range(Npnt),dtype=np.int32)
    for c in cd.values():
        if c[0] < Nchn:
            wd['A_'+c[3]] = tmp_data.T[     c[0],0:Npnt]
            wd['R_'+c[3]] = tmp_data.T[Nchn+c[0],0:Npnt]

    # everything ok, print message and return nrfs_data object
    print ('%s, Nchn = %d, Npnt = %d' % (inFile,Nchn,Npnt))
    return wd


def load_buf(inFile,inOptions=''):
    """
    load a BFG buffer file (.buf),
    it assumes that the bfgdefs.knl file is 'sibbling'.

    Arguments:
        *inFile*:
            path and filename

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info

    Returns:
        a filled nrfs_data object
    """

    # check options
    bVerbose = 'v' in inOptions

    if (bVerbose): print "[load_buf] file:",inFile

    # check if file exists and check if sibbling bfgdefs.knl exists
    (dirName, fileName) = os.path.split(inFile)
    chnFile = os.path.join(dirName,'bfgdefs.knl')

    if not os.path.isfile(inFile) :
        raise ValueError, 'data file '+inFile+' does not exist'
    if not os.path.isfile(chnFile):
        raise ValueError, 'channels file '+chnFile+' does not exist'

    # create new nrfs_data object
    wd = nrfs_data()

    # read the channel definition
    cd = load_channels(chnFile,inOptions)

    # open the file, and read header in one big chunk
    hs = 1024                        # headersize
    fd = open(inFile,'rb')
    fd.seek(0)
    s = fd.read(hs)

    # retrieve some data from the header
    Nchn           = int(struct.unpack('h',s[6:8])[0])
    wd.file_date   = s[18:26]
    wd.file_time   = s[10:18]

    wd.file_name   = inFile
    wd.file_type   = 'buf'
    wd.counter     = int(struct.unpack('i',s[26+2*Nchn+8:26+2*Nchn+8+4])[0])
    wd.time        = float(struct.unpack('f',s[26+2*Nchn+12:26+2*Nchn+12+4])[0])

    # we skip the remaining of the header

    # make an estimate of the number of data points in the file
    fs = os.path.getsize(inFile)      # file size
    ds = fs - hs                      # data size
    rs = Nchn * (2+2) + 10            # data record size

    Nest = ds/rs                      # estimate Npnt

    # allocate some temporary arrays
    tmp_data     = np.empty((Nest, Nchn))
    tmp_counter  = np.zeros((Nest,), dtype=np.int32)
    tmp_testtime = np.empty((Nest,))

    # local callibration factors and offsets
    lcf = np.ones((Nchn,))
    los = np.zeros((Nchn,))
    for c in cd.iteritems():
        if c[0]<Nchn : # bugfix, if there are more channels defined in
                       # bfgdefs.knl than there are in the .buf file
            lcf[c[0]] = c[1][1]
            los[c[0]] = c[1][2]

    Npnt = 0

    # move to the start of the data in the file
    fd.seek(1024)
    testtime_offset = 0.0
    while True :

        s = fd.read(2)
        if len(s) <2 : break ## EOF

        rec_type = int(struct.unpack('h',s[0:2])[0])

        if rec_type == 0:
            s = fd.read(rs-2)
            tmp_counter[Npnt]  = int(struct.unpack('i',s[0:4])[0])
            # testtime, fix it in case of a jump
            testtime = float(struct.unpack('f',s[4:8])[0])
            if  Npnt>1:
                if testtime < tmp_testtime[Npnt-1]:
                    testtime_offset = 2.0 * tmp_testtime[Npnt-1] - \
                                      tmp_testtime[Npnt-2]      - \
                                      testtime
            tmp_testtime[Npnt] = testtime_offset + testtime
            # data points
            tmp_data[Npnt,0:Nchn] =  \
                np.array(struct.unpack('%dh'%Nchn,s[8:8+2*Nchn]),dtype=np.float64)
            # apply calfac and offset
            tmp_data[Npnt,0:Nchn] = tmp_data[Npnt,0:Nchn] * lcf + los
            Npnt += 1

        elif rec_type == 1:
            # callibration factors and offsets
            s = fd.read(Nchn*8)
            for i in range(0,Nchn) :
                lcf[i] = float(struct.unpack('f',s[ 8*i  : 8*i+4 ])[0])
                los[i] = float(struct.unpack('f',s[ 8*i+4: 8*i+8 ])[0])
            if (bVerbose):
                print "[load_buf] Calibration factor/offset"
                print lcf
                print los

        elif rec_type == 5:
            # time header
            # skip it, we do not need it
            fd.read(8)

        else :
            print '[load_buf] Unknown record type ('+ str(rec_type) +') in .buf file'
            #print '=== rec_type ====>', rec_type
            #print '=== Npnt  =======>', Npnt
            #raise ValueError, 'Unknown record type'

    # file sluiten
    fd.close()

    # copy tmp to wd
    wd.allocate(Npnt)
    wd['testtime'] = tmp_testtime[0:Npnt]
    wd['record']   = np.array(range(Npnt),dtype=np.int32)
    bBufferToggleWarning = False
    for c in cd.values():
        if c[0]< Nchn :
            wd[c[3]] = tmp_data.T[c[0],0:Npnt]
        else :
            bBufferToggleWarning = True
            print "Error in file: '%s' not in measurement" % (c[3])
    if bBufferToggleWarning :
        print '=========================================='
        print '= WARNING:                               ='
        print '= BufferToggle in BFG was probably "UIT" ='
        print '= for some channels                      ='
        print '=========================================='

    # everything ok, print message and return nrfs_data object
    print ('%s, Nchn = %d, Npnt = %d' % (inFile,Nchn,Npnt))
    return wd

def load_dmp(inFile,inOptions='',**kwargs):
    """
    load a Blatest buffer file (.dmp),
    it assumes that the channels.set file is 'sibbling'.

    Arguments:
        *inFile*:
            path and filename

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info
                * 'r'   - reduce, skip   9 of   10 points
                * 'rr'  - reduce, skip  99 of  100 points
                * 'rrr' - reduce, skip 999 of 1000 points

    Returns:
        a filled nrfs_data object
    """

    # check options
    bVerbose = 'v' in inOptions
    #Nstep = kwargs.pop('Nstep',1)
    Nstep = 1
    if 'r'   in inOptions: Nstep = 10
    if 'rr'  in inOptions: Nstep = 100
    if 'rrr' in inOptions: Nstep = 1000

    if (bVerbose): print "[load_dmp] file:",inFile

    # check if file exists and check if sibbling channels.set exists
    (dirName, fileName) = os.path.split(inFile)
    chnFile = os.path.join(dirName,'channels.set')
    if not os.path.isfile(inFile) :
        raise ValueError, 'data file '+inFile+' does not exist'
    if not os.path.isfile(chnFile):
        raise ValueError, 'channels file '+ chnFile+' does not exist'

    # create new nrfs_data object
    wd = nrfs_data()

    # read channel definition
    cd = load_channels(chnFile,inOptions)

    # open file and read header in one big chunk
    fs = os.path.getsize(inFile)
    hs = 50                            # headersize
    fd = open(inFile,'rb')
    fd.seek(0)
    s = fd.read(hs)

    # retrieve some info from the header
    Nchn           = int(struct.unpack('h',s[0:2])[0])
    wd.dumpratio   = int(struct.unpack('h',s[46:48])[0])
    ut             = int(struct.unpack('i',s[38:42])[0])
    wd.file_date   = datetime.datetime.fromtimestamp(ut).date().isoformat()
    wd.file_time   = datetime.datetime.fromtimestamp(ut).time().isoformat()
    wd.file_name   = inFile
    wd.file_type   = 'dmp'
    wd.cycle       = int(struct.unpack('h',s[20:22])[0])
    wd.record      = int(struct.unpack('h',s[22:24])[0])
    wd.cycle100per = int(struct.unpack('i',s[24:28])[0])
    wd.loadfactor  = float(struct.unpack('f',s[34:38])[0])

    # estimate number of data points
    ds = fs-50                        # datasize
    rs = Nchn*2+4                     # record size
    Npnt = ds/rs           # aantal berekende punten
    if ds%rs != 0 :
        raise ValueError, 'incorrect file size'

    # for reduce option
    Npnt = int(Npnt/Nstep)

    # allocate temporary arrays
    tmp_scantime = np.zeros((Npnt,))
    tmp_data     = np.empty((Npnt, Nchn))

    # local callibration factors and offsets
    lcf = np.ones((Nchn,))
    los = np.zeros((Nchn,))
    for c in cd.iteritems():
        if c[0]<Nchn : # bugfix, if there are more channels defined in
                       # bfgdefs.knl than there are in the .dmp file
            lcf[c[0]] = c[1][1]
            los[c[0]] = c[1][2]

    # read data in one big chunck
    s = fd.read(ds)
    for i in range(0,Npnt) :
        i2 = i * Nstep
        tmp_scantime[i] = int(struct.unpack('i',s[ rs*i2 : rs*i2+4 ])[0])
        #for j in range(0,Nchn) :
        #    wd.data[j,i] = los[j] + lcf[j] * \
        #        float(int(struct.unpack('h',s[ rs*i2+4+j*2 : rs*i2+4+j*2+2 ])[0]))
        tmp_data[i] = np.array(
            struct.unpack('%dh'%Nchn,s[ rs*i2+4:rs*i2+4+2*Nchn]))

    # apply calfac and offset
    tmp_data = tmp_data * lcf + los

    fd.close()

    # copy tmp to wd
    wd.allocate(Npnt)
    wd['scantime'] = tmp_scantime[0:Npnt]
    wd['record']   = np.array(range(Npnt),dtype=np.int32)
    for c in cd.values():
        if c[0] < Nchn:
            wd[c[3]] = tmp_data.T[c[0],0:Npnt]

    # everything ok, print message and return nrfs_data object
    print ('%s, Nchn = %d, Npnt = %d' % (inFile,Nchn,Npnt))
    return wd

def load_multiple_dmp(inFile,inOptions='',inStationList=None):
    """
    loads multiple .dmp files from different Blatest stations
    and return the joined nrfs_data object.

    it assumes that the channels.set file are 'sibbling'.

    Arguments:
        *inFile*:
            path and filename, the pasth should contain 'datax', where
            the x is replaced by 1,2,3... or if given the integers from
            `inStationList`

        *inStationList*:
            list(or np.ndarray) of integers, see `inFile`.

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info

    Returns:
        a filled nrfs_data object
    """
    if not 'datax' in inFile:
        raise ValueError, 'No \'datax\' in inFile'

    bWarn = True
    if inStationList==None:
       inStationList = [1,2,3,4,5,6,7,8,9]
       bWarn = False

    wd = [] # list for the nrfs_data objects
    for stat in inStationList:
        fn = string.replace(inFile,'datax','data'+str(stat))
        if not os.path.isfile(fn):
            if bWarn:
                raise ValueError, 'File \''+fn+'\' does not exist'
        else:
            wd.append(load_dmp(fn,inOptions))

    combined_data = join_nrfs_data(wd)

    #copy some data from the first nrfs_data object
    combined_data.cycle       = wd[0].cycle
    combined_data.record      = wd[0].record
    combined_data.cycle100per = wd[0].cycle100per
    combined_data.loadfactor  = wd[0].loadfactor

    return combined_data

def load_dat(inFile,inOptions=''):
    """
    load a Blatest points file (.dat),
    it assumes that the channels.set file is 'sibbling'.

    Arguments:
        *inFile*:
            path and filename

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info
    """

    # check options
    bVerbose = 'v' in inOptions

    if (bVerbose): print "[load_dmp] file:",inFile

    # check if file exists and check if sibbling channels.set exists
    (dirName, fileName) = os.path.split(inFile)
    chnFile = os.path.join(dirName,'channels.set')
    if not os.path.isfile(inFile) :
        raise ValueError, 'data file ' + inFile+' does not exist'
    if not os.path.isfile(chnFile):
        raise ValueError, 'channels file '+ chnFile+' does not exist'

    # create new nrfs_data object
    wd = nrfs_data()

    # read channel definition
    cd = load_channels(chnFile,inOptions)

    # info
    wd.file_name   = inFile
    wd.file_type   = 'dat'
    # file size
    fs = os.path.getsize(inFile)

    # open the data file
    dat_f = open(inFile,'rb')

    n_record = 0;
    raw_data = []
    for line in dat_f :
        parts = line.split()
        if n_record==0 :
            # first time => determine n_channels and allocate arrays
            Nchn = len(parts)-1
            Npnt = fs / ( 21 + Nchn * 7)
            # allocate arrays
            lcf = np.ones((Nchn,))
            los = np.zeros((Nchn,))
            tmp_unixtime = np.zeros((Npnt,),dtype=np.int32)
            tmp_data = np.empty((Npnt,Nchn))
            # local callibration factors and offsets
            for c in cd.iteritems():
                if c[0]<Nchn : # bugfix, if there are more channels defined in
                               # bfgdefs.knl than there are in the .buf file
                    lcf[c[0]] = c[1][1]
                    los[c[0]] = c[1][2]
        # data
        for i in range(0,Nchn):
            tmp_data[n_record,i] = los[i] + lcf[i] * int(parts[i+1])
        # convert .dat time stamp to unix time
        tmp_unixtime[n_record] = time.mktime((int(parts[0][6:8]),
                                              int(parts[0][3:5]),
                                              int(parts[0][0:2]),
                                              int(parts[0][12:14]),
                                              int(parts[0][15:17]),
                                              int(parts[0][18:20]),0,0,0))

        n_record += 1
    dat_f.close()

    dat_f.close()

    # copy tmp to wd
    wd.allocate(Npnt)
    wd['unixtime'] = tmp_unixtime[0:Npnt]
    wd['record']   = np.array(range(Npnt),dtype=np.int32)
    for c in cd.values():
        if c[0] < Nchn:
            wd[c[3]] = tmp_data.T[c[0],0:Npnt]

    # everything ok, print message and return nrfs_data object
    print ('%s, Nchn = %d, Npnt = %d' % (inFile,Nchn,Npnt))
    return wd

def load_multiple_dat(inFile,inOptions='',inStationList=None):
    """
    loads multiple .dat files from different Blatest stations
    and return the joined nrfs_data object.

    it assumes that the channels.set file is 'sibbling'.

    Arguments:
        *inFile*:
            path and filename, the pasth should contain 'datax', where
            the x is replaced by 1,2,3... or if given the integers from
            `inStationList`

        *inStationList*:
            list(or np.ndarray) of integers, see `inFile`.

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info
    """
    if not 'datax' in inFile:
        raise ValueError, 'No \'datax\' in inFile'

    bWarn = True
    if inStationList==None:
       inStationList = [1,2,3,4,5,6,7,8,9]
       bWarn = False

    wd = [] # list for the nrfs_data objects
    for stat in inStationList:
        fn = string.replace(inFile,'datax','data'+str(stat))
        if not os.path.isfile(fn):
            if bWarn:
                raise ValueError, 'File \''+fn+'\' does not exist'
        else:
            wd.append(load_dat(fn,inOptions))

    return join_nrfs_data(wd)

def load_st3(inFile,inLoadCase='',inStat=0,inOptions=''):
    """
    load a Blatest ST3 file (.st3),
    it assumes that the channels.set file is 'sibbling'.

    Mostly this function is not called directly but by
    `load_multiple_st3`.

    Arguments:
        *inFile*:
            path and filename

        *inLoadCase*:
            string, if given only specified loadcase is loaded, otherwise
            all loadcases are loaded

        *inStat*:
            station number, not necessary ???

        *inOptions*:
            string that can contain the following options
                * 'v' - verbose, print debug info
    """

    # check options
    bVerbose = 'v' in inOptions

    # some init
    if (bVerbose): print "[load_st3] file:",inFile
    inLoadCase = inLoadCase.lower()

    # check if file exists and check if sibbling channels.set exists
    (dirName, fileName) = os.path.split(inFile)
    chnFile = os.path.join(dirName,'channels.set')
    #print '===>',dirName, fileName, chnFile
    if not os.path.isfile(inFile) :
        raise ValueError, 'data file '+inFile+' does not exist'
    if not os.path.isfile(chnFile):
        raise ValueError, 'channels file '+ chnFile+' does not exist'

    # create new nrfs_data object
    wd = nrfs_data()

    # read channel definition
    cd = load_channels(chnFile,inOptions)

    # The .st3 file has no global header
    # To determine the number of channels, we read records until we reach
    # a 'PERI' or an 'ACTU' and then we determine the number of channels
    # from 'recordlen'

    # open the file
    hs = 64                        # headersize
    fs = os.path.getsize(inFile)      # file size

    fd = open(inFile,'rb')
    fd.seek(0)

    Nchn = 0
    while True :
        h = fd.read(hs)
        if len(h) <hs : break ## EOF
        rec_type = h[2:7]
        reclen = int(struct.unpack('h',h[36:38])[0])
        d = fd.read(reclen)
        if rec_type == 'PERI ' or rec_type == 'ACTU ':
            N = int(struct.unpack('h',d[0:2])[0])
            if N > Nchn : Nchn = N

    # set some info
    wd.file_name   = inFile
    wd.file_type   = 'st3'
    wd.station     = inStat

    # estimate number of data points on file size

    # worst case scenario : only 'STRT ' records
    # each record has an header of 64 bytes and 6*Nchn data

    Nest = fs/(64+6*Nchn)             # estimate Npnt

    # allocate arrays
    lcf             = np.ones((Nchn*2,))
    los             = np.zeros((Nchn*2,))
    tmp_data        = np.empty((Nchn*2,Nest))
    tmp_st3_record  = np.empty((Nest,),dtype=np.int32)
    tmp_st3_cycle   = np.empty((Nest,),dtype=np.int32)
    tmp_st3_rec_cyc = np.empty((Nest,),dtype=np.int32)
    tmp_st3_100per  = np.zeros((Nest,),dtype=np.int32)
    tmp_st3_count   = np.zeros((Nest,),dtype=np.int32)
    tmp_unixtime    = np.zeros((Nest,),dtype=np.int32)

    # local callibration factors and offsets
    for c in cd.iteritems():
        if c[0]<Nchn : # bugfix, if there are more channels defined in
                       # bfgdefs.knl than there are in the .st3 file
            lcf[c[0]       ]=c[1][1]
            lcf[c[0]+Nchn  ]=c[1][1]

            los[c[0]       ]=c[1][2]
            los[c[0]+Nchn  ]=c[1][2]

    # start reading records
    fd.seek(0)                       # reset file to start
    Npnt = 0

    # read header, also EOF detection
    while True :
        h = fd.read(hs)
        if len(h) <hs : break ## EOF

        rec_type = h[2:7]
        loadcase = h[8:16].replace('\00','').lower()
        reclen = int(struct.unpack('h',h[36:38])[0])
        wd.file_date = h[16:24]  # will be overwritten each time
        wd.file_time = h[28:36]

        d = fd.read(reclen)    # read data

        if rec_type == 'TEXT ' :
            # text type, print it
            # print '[load_st3] text type: ',d[0:60]
            pass

        elif rec_type == 'PERI ' and  \
            (inLoadCase == '' or inLoadCase == loadcase) :

            tmp_st3_record[Npnt] = int(struct.unpack('h',h[40:42])[0])
            tmp_st3_cycle[Npnt]  = int(struct.unpack('h',h[42:44])[0])
            tmp_st3_rec_cyc[Npnt]=  long(tmp_st3_record[Npnt]) * 100000L + \
                                    long(tmp_st3_cycle[Npnt])
            tmp_unixtime[Npnt]   = int(struct.unpack('i',h[50:54])[0])
            tmp_st3_100per[Npnt] = int(struct.unpack('i',h[54:58])[0])
            N = int(struct.unpack('h',d[0:2])[0])
            for i in range(0,N) :
                # count = int()
                cnt = int(struct.unpack('h',d[10+10*i : 12+10*i])[0])
                tmp_st3_count[Npnt] = cnt # will be overwritten
                # cnt *= 2  # because of definition RNG,
                            # sum of ranges instead of (max-min)
                # RNG (long), no offset in RNG
                tmp_data[i+Nchn  ,Npnt] = lcf[i] * \
                    float(int(struct.unpack('i',d[ 2+10*i :  6+10*i])[0])) / \
                    ( cnt * 2)
                # AVG (long)
                tmp_data[i       ,Npnt] = los[i] + lcf[i] * \
                    float(int(struct.unpack('i',d[ 6+10*i : 10+10*i])[0])) /cnt
            Npnt += 1

        else :
            #if (bVerbose): print '[load_st3] ignoring record type :',rec_type
            pass

    # some admin...
    wd.allocate(Npnt)
    wd['record']   = np.array(range(Npnt),dtype=np.int32)
    wd['st3_record'] = tmp_st3_record[0:Npnt]
    wd['st3_cycle']  = tmp_st3_cycle[0:Npnt]
    wd['st3_rec_cyc'] = tmp_st3_rec_cyc[0:Npnt]
    wd['st3_100per'] = tmp_st3_100per[0:Npnt]
    wd['st3_count'] = tmp_st3_count[0:Npnt]
    wd['unixtime'] = tmp_unixtime[0:Npnt]
    for c in cd.values():
        if c[0] < Nchn:
            wd['A_'+c[3]] = tmp_data[c[0]     ,0:Npnt]
            wd['R_'+c[3]] = tmp_data[c[0]+Nchn,0:Npnt]

    fd.close()

    # everything ok, print message and return nrfs_data object
    print ('%s, Nchn = %d, Npnt = %d, station = %d' % (inFile,Nchn,Npnt,wd.station))
    return wd


def load_multiple_st3(inDirectory,
                      inLoadCase='',
                      inLoadSequence='',
                      inStartRec=0,
                      inEndRec=99999,
                      inOptions=''):
    """
    loads a multiple .st3 (Blatest points) files.

    Arguments :
        *inDirectory*:
            path to the directory that contains the ``DATAx`` directories,
            where x can be 1 to 5, and these directory must contain Rxxxxx
            directories and these direcory must contain the xxxxxxx.st3 files.

        *options* :
            * 'v' - verbose, print debug info

    Returns:
        a nrfs_data object

    """
    # check options
    bVerbose = 'v' in inOptions

    st3_files = []
    print "load_multiple_st3"
    for dir, subdirs, files in os.walk(inDirectory):
        for file in files:
            filename = os.path.join(dir, file)
            # fix non unix slashes
            filename = filename.replace('\\','/')
            #check naam voor "...../DATAx/Ryyyyy/zzzzz.st3" formaat
            tmatch = re.search(r'^.*\/data(\d)\/R(\d{5})\/(.*)\.st3$',
                filename,re.IGNORECASE)
            if tmatch:
                stat_no = int(tmatch.group(1))
                rec_no = int(tmatch.group(2))
                loadsequence = tmatch.group(3)
                if ((stat_no >= 1 and stat_no <= 5) and
                    (rec_no >= inStartRec) and
                    (rec_no <= inEndRec) and
                    (inLoadSequence == '' or
                     inLoadSequence.lower() == loadsequence.lower())) :
                    # we have a correct file:
                    st3_files.append(
                        load_st3(filename,inLoadCase,stat_no,inOptions))

    # join and return the list of nrfs_data objects
    return join_st3_data(st3_files)

def join_st3_data(inList):
    """
    Joins multiple nrfs_data objects from seperate .st3 files, helper
    function for ``load_multiple_st3``.
    """

    # determine size of resulting nrfs_data object
    cum_st3_rec_cyc = set()
    cum_labels = set()
    for wd in inList:
        for st3_rec_cyc in wd['st3_rec_cyc']:
            cum_st3_rec_cyc.add(st3_rec_cyc)
        for chn in wd:
            cum_labels.add(chn)

    # create nrfs_data object to return
    rv = nrfs_data()
    rv.allocate(len(cum_st3_rec_cyc))
    rv['st3_rec_cyc'] = np.sort(np.array(list(cum_st3_rec_cyc)))

    # copy data from each nrfs_data into the return nrfs_data object
    special_channels = ['record',
                        'st3_record',
                        'st3_cycle',
                        'st3_rec_cyc',
                        'st3_100per',
                        'st3_count',
                        'unixtime']
    for wd in inList:
        for chn in wd:
            if not chn in rv:
                dtype = wd[chn].dtype
                if dtype==np.float64:
                    rv[chn] = nans((rv.Npnt,),dtype=dtype)
                else:
                    rv[chn] = np.zeros((rv.Npnt,),dtype=dtype)
            if chn not in special_channels or wd.station == 1:
                for i in range(0,wd.Npnt):
                    i2 = np.searchsorted(rv['st3_rec_cyc'],wd['st3_rec_cyc'][i])
                    rv[chn][i2] = wd[chn][i]
    rv['record']   = np.array(range(rv.Npnt),dtype=np.int32)
    return rv



def load_nrfss(inFile, **kwargs):
    """
    Loads the data from a nrfsS data file [.buffer|.rngavg|.points] into a
    nrfss_data object.

    Arguments:
        *inFile*:
            path and filename

    Keyword arguments:
        *skipChn*:
            skip channels with lables starting with 'chn', default True

        *skipNc*:
            skip channels with lables starting with 'nc', default True

        *start*:
            skip records before the *start* record

        *stop*:
            skip records after the *stop* record

        *step*:
            take every *step* record

    """
    # process kwargs
    skipChn = True
    skipNc  = True
    start   = None
    stop    = None
    step    = 1

    for key in kwargs:
        if key not in ['skipChn', 'skipNc', 'start', 'stop', 'step']:
            print 'Unknown kwarg :', key
        if key == 'skipChn':
            skipChn = kwargs[key]
        if key == 'skipNc':
            skipNc = kwargs[key]
        if key == 'start':
            start = kwargs[key]
        if key == 'stop':
            stop = kwargs[key]
        if key == 'step':
            step = kwargs[key]

    # some 'constants', block identifiers
    BT_nrfsS_IDENTIFIER  =  0
    BT_FILE_TYPE        = 10
    BT_CHN_COUNT        = 20
    BT_TESTNAME         = 30
    BT_UNIX_TIME_SEC    = 40
    BT_UNIX_TIME_NSEC   = 41
    BT_RECORD_NO        = 50
    BT_CYCLE_NO         = 51
    BT_100PER_CYCLE_NO  = 52

    BT_CHANNEL_LABEL    = 100
    BT_CHANNEL_UNIT     = 101

    BT_CHANNEL_CALFAC   = 110
    BT_CHANNEL_OFFSET   = 111

    BT_DATA_RECORDS     = 200


    # helper function, an generator which extracts blocks from binary data
    #def blocks_from_chunk(chunk):

    #    size = len(chunk)
    #    index = 0

    #    while index + 8 <= size:

    #        block_type = int(struct.unpack('i', chunk[index + 0 : index + 4],)[0])
    #        block_len  = int(struct.unpack('i', chunk[index + 4 : index + 8],)[0])
    #        index += 8

    #        if block_len >= 0 and index + block_len <= size:

    #            block = chunk[index : index + block_len]
    #            index += block_len
    #            yield block_type, block_len, block

    #        else:

    #            break

    # helper function, an generator which extracts blocks from binary data
    def blocks_from_file(filename):

        fs = os.path.getsize(inFile)
        fd = open(inFile,'rb')

        index = 0

        while index + 8 <= fs:

            chunk = fd.read(8)

            block_type = int(struct.unpack('i', chunk[0:4],)[0])
            block_len  = int(struct.unpack('i', chunk[4:8],)[0])
            index += 8

            if block_len >= 0 and index + block_len <= fs:

                block = fd.read(block_len)
                index += block_len
                yield block_type, block_len, block

            else:

                break

        fd.close()


    # create the nrfs_data object
    wd = nrfs_data()

    # read file as one big chunk
    fs = os.path.getsize(inFile)
    #fd = open(inFile,'rb')
    #chunk = fd.read(fs)
    #fd.close()

    # initialize data structures
    Nchn = 0
    Npnt = 0
    NpntRead = 0
    tmp_data     = None
    tmp_scantime = None
    tmp_unixtime = None
    tmp_status   = None
    tmp_counter  = None
    tmp_unit     = None
    tmp_label    = None
    tmp_calfac   = None
    tmp_offset   = None

    unixtime_sec  = long(0)
    unixtime_nsec = long(0)

    # iterate over the blocks in the chunk, and process the known blocks
    #for block_type, block_len, block in blocks_from_chunk(chunk):
    for block_type, block_len, block in blocks_from_file(inFile):

        if block_type == BT_nrfsS_IDENTIFIER:
            if block != 'nrfsS':
                print('wrong identifier, ignored')

        elif block_type == BT_FILE_TYPE:
            pass

        elif block_type == BT_CHN_COUNT:
            if Nchn == 0:
                Nchn = int(struct.unpack('i', block)[0])
                if Nchn > 0:
                    # allocate memory, with (over) estimated number of points
                    file_estimate = fs / (4 * Nchn + 40)
                    # correct for *start* and *stop*
                    if start and stop:
                        estimate = stop - start
                    elif start and not stop:
                        estimate = file_estimate - start
                    elif not start and stop:
                        estimate = stop
                    else:
                        estimate = file_estimate
                    # correct for *step*
                    estimate /= step

                    # set start and stop...
                    if not start:
                        start = 0
                    if not stop:
                        stop = sys.maxint

                    #print file_estimate, estimate

                    tmp_data     = np.empty((estimate, Nchn), dtype=np.float)
                    tmp_scantime = np.zeros((estimate,),      dtype=np.int64)
                    tmp_unixtime = np.zeros((estimate,),      dtype=np.float)
                    tmp_status   = np.zeros((estimate,),      dtype=np.int64)
                    tmp_counter  = np.zeros((estimate,),      dtype=np.int64)
                    tmp_unit     = np.zeros((Nchn,),      dtype='|S50')
                    tmp_label    = np.zeros((Nchn,),      dtype='|S50')
                    tmp_calfac   = np.zeros((Nchn,),      dtype=np.float)
                    tmp_offset   = np.zeros((Nchn,),      dtype=np.float)
            else:
                # in future we might reallocate stuff...
                print('more than one channel count, ignored at first')

        elif block_type == BT_DATA_RECORDS:

            if Nchn > 0:
                rs = Nchn * 4 + 40 # record size
                if block_len % rs == 0:
                    n = block_len / rs
                    for i in range(n):

                        # check if we need to store this record
                        if ( NpntRead >= start and
                             NpntRead <  stop  and
                             (NpntRead -start) % step == 0) :

                            # store the record...
                            tmp_data[Npnt] = np.array(
                                struct.unpack('%df' % Nchn,
                                    block[ rs * i : rs * i + 4 * Nchn]))

                            offset = rs * i + 4 * Nchn

                            tmp_scantime[Npnt] = long(
                                struct.unpack('q',
                                    block[ offset : offset + 8 ])[0])

                            sec = long(
                                struct.unpack('q',
                                    # block[ offset + 8 : offset + 16 ])[0]) - unixtime_sec
                                    block[ offset + 8 : offset + 16 ])[0])

                            nsec = long(
                                struct.unpack('q',
                                    # block[ offset + 16 : offset + 24 ])[0]) - unixtime_nsec
                                    block[ offset + 16 : offset + 24 ])[0])

                            tmp_unixtime[Npnt] = float(sec + nsec * 1.0e-9)

                            tmp_status[Npnt] = long(
                                struct.unpack('q',
                                    block[ offset + 24 : offset + 32 ])[0])

                            tmp_counter[Npnt] = long(
                                struct.unpack('q',
                                    block[ offset + 32 : offset + 40 ])[0])

                            Npnt += 1

                        NpntRead += 1

                else:
                    print('in correct blocksize for data records')
            else:
                print('no yet allocated')

        elif block_type == BT_CHANNEL_LABEL:
            if block_len >= 4:
                chn = int(struct.unpack('i', block[0:4])[0])
                if chn >= 0 and chn < Nchn:
                    tmp_label[chn] = block[4:block_len]

        elif block_type == BT_CHANNEL_UNIT:
            if block_len >= 4:
                chn = int(struct.unpack('i', block[0:4])[0])
                if chn >= 0 and chn < Nchn:
                    tmp_unit[chn] = block[4:block_len]

        elif block_type == BT_CHANNEL_CALFAC:
            chn = int(struct.unpack('i', block[0:4])[0])
            tmp_calfac[chn] = float(struct.unpack('f', block[4:12])[0])

        elif block_type == BT_CHANNEL_OFFSET:
            chn = int(struct.unpack('i', block[0:4])[0])
            tmp_offset[chn] = float(struct.unpack('f', block[4:12])[0])

        elif block_type == BT_UNIX_TIME_SEC:
            unixtime_sec = long(struct.unpack('q',block)[0])

        elif block_type == BT_UNIX_TIME_NSEC:
            unixtime_nsec = long(struct.unpack('q',block)[0])

        elif block_type == BT_RECORD_NO:
            pass

        elif block_type == BT_CYCLE_NO:
            pass

        elif block_type == BT_100PER_CYCLE_NO:
            pass

        else:
            print('unknown blocktype %d : ' % (block_type))


    # copy tmp to wd
    wd.allocate(Npnt)
    wd['scantime'] = tmp_scantime[0:Npnt]
    wd['unixtime'] = tmp_unixtime[0:Npnt]
    wd['status']   = tmp_status[0:Npnt]
    wd['counter']  = tmp_counter[0:Npnt]
    wd['record']   = np.array(range(Npnt),dtype=np.int64)
    wd.units = {}
    wd.calfac = {}
    wd.offset = {}
    for i in range(Nchn):
        label = tmp_label[i]
        skip = False
        if skipChn and (label[0:3].lower() == 'chn'    or
                        label[0:5].lower() == 'a_chn'  or
                        label[0:5].lower() == 'r_chn') : skip = True
        if skipNc and  (label[0:2].lower() == 'nc'     or
                        label[0:4].lower() == 'a_nc'   or
                        label[0:4].lower() == 'r_nc')  : skip = True
        if not skip:
            wd[label] = tmp_data.T[i,0:Npnt]
            # following might or might not be availble hence the try/except.
            try:
                wd.units[label] = tmp_unit[i]
            except:
                pass
            try:
                wd.calfac[label] = tmp_calfac[i]
            except:
                pass
            try:
                wd.offset[label] = tmp_offset[i]
            except:
                pass

    wd['testtime'] = wd['unixtime'] - wd['unixtime'][0]

    wd.unixtime = unixtime_sec
    wd.unixtime_nsec = unixtime_nsec

    wd.file_name   = inFile
    wd.file_type   = 'nrfss'

    # everything ok, print message and return nrfs_data object
    print ('%s, Nchn = %d, Npnt = %d' % (inFile,Nchn,Npnt))
    return wd



def load_xls(inFile,inOptions=''):
    """
    Loads the data from an .xls excel file into a nrfs_data object.

    The data should be in the first sheet, in a full rectangle data
    block, the first column should be the label.

    The format is the same as produced by nrfs_data.save_xls()

    Arguments:
        *inFile*:
            path and filename

        *inOptions*
            Not yet used
    """

    # version 0.7.1 or higher required
    from xlrd import open_workbook

    book = open_workbook(inFile)
    sheet = book.sheet_by_index(0)

    # create new nrfs_data object
    wd = nrfs_data()
    wd.allocate(sheet.nrows-1)

    for i in range(sheet.ncols):
        label = (str(sheet.cell(0,i).value)).strip()
        wd[label] = np.array(sheet.col_values(i,1,sheet.nrows))

    # some admin...
    wd.file_type = 'xls'
    return wd

# ==== nrfslib Plotting Functions
# ===================================================================

def plotcomment(inComment):
    """
    plots a *inComment* above current axis. This can be used instead
    of plt.title
    """
    plt.text(0.005, 1.005 , inComment,
             size='x-small', horizontalalignment='left',
             transform = plt.gca().transAxes)

def savefig(inName,w=11.6929134,h=8.26771654):
    """
    Modification of matplotlib.savefig, adds 'nrfs' logo to the saved figure.
    """
    plt.ioff()
    #old_w,old_h = plt.gcf().get_size_inches()
    #plt.gcf().set_size_inches(w,h)

    # Note: Don't change anything on the next four lines, they are replaced
    #       by the setup script to create the BTCG installer
    savefig_logo_text  = 'Knowledge Centre nrfs'
    savefig_logo_color = '#3366FF'
    savefig_logo_style = 'oblique'
    savefig_logo_size  = 'small'

    plt.text(0.995, 0.005 ,
             savefig_logo_text,
             style=savefig_logo_style,
             weight='bold',
             size=savefig_logo_size,
             color=savefig_logo_color,
             horizontalalignment='right',
             transform = plt.gca().transAxes)

    plt.savefig(inName)
    del(plt.gca().texts[-1])
    #plt.gcf().set_size_inches(old_w,old_h)
    plt.ion()

def savefig_for_ppt(fileName):
    """
    Save the figure for use in the nrfs powerpoint presentation template.
    Colors are changed, to blend in with the powerpoint style.
    """
    colormap = {'red'    :'yellow' , \
                'green'  :'lime'   , \
                'blue'   :'cyan'   , \
                'black'  :'white', \
                'purple' :'pink'   , \
                'grey'   : 'red'   , \
                'cyan'   : 'green' , \
                'k'      : 'white' }

    #get all items in the figure
    itemlist = [plt.gcf()]
    for item in itemlist:
        itemlist += item.get_children()
        #somehow some children are forgotten in .get_children()
        if isinstance(item, matplotlib.legend.Legend):
            itemlist.append(item.legendPatch)
        if isinstance(item, matplotlib.text.Annotation):
            itemlist.append(item.arrow_patch)

    oldcolors = {}  #dictionary to store the colors
    oldmec = {}     #dictionary to store marker edge colors
    oldmfc = {}     #marker face colors

    #adjust colors
    #iterate over all items in the figure
    for item in itemlist:
        #first try if this item has get_color and set_color as methods
        try:
            #store the old color
            oldcolors[item] = item.get_color()
            #it may be a line with markers, store their colors now because set_color may change them
            try:
                oldmec[item] = item.get_markeredgecolor()
                oldmfc[item] = item.get_markerfacecolor()
            except AttributeError: pass
            #change the color according colormap. if the color is not in colormap leave it unchanged
            item.set_color(colormap.get(item.get_color(), item.get_color()))
            #and try for markers
            item.set_markeredgecolor(colormap.get(item.get_markeredgecolor(), item.get_markeredgecolor()))
            item.set_markerfacecolor(colormap.get(item.get_markerfacecolor(), item.get_markerfacecolor()))
        except AttributeError: pass
        try:
            oldcolors[item] = item.get_edgecolor()
            item.set_edgecolor(colormap.get(item.get_edgecolor(), item.get_edgecolor()))
        except AttributeError: pass
        try:
            item.legendPatch.get_facecolor()
            item.legendPatch.set_facecolor((0,.15,.45))
        except AttributeError: pass
        try:
            item.patch.set_alpha(0.1)
            item.patch.set_lw = 2
        except AttributeError: pass
    #make the figpatch 100% transparant
    plt.gcf().patch.set_alpha(0.0)
    plt.draw()
    #save the figure
    #try-finally to make sure the settings are always returned to the original
    try: plt.savefig(fileName)
    except: raise
    finally:
        #reset the original colors for all items
        for item in itemlist:
            try:
                item.get_color()   #because some items have set_color but not get_color
                item.set_color(oldcolors[item])
                item.set_markeredgecolor(oldmec[item])
                item.set_markerfacecolor(oldmfc[item])
            except AttributeError: pass
            try:
                item.get_edgecolor()
                item.set_edgecolor(oldcolors[item])
            except AttributeError: pass
            try:
                #to be done: store the original facecolors. For now we assume it was white
                item.legendPatch.set_facecolor('white')
            except AttributeError: pass
            try:
                #to be done: store original alpha's and linewidth, for now assume 1.
                item.patch.set_alpha(1)
                item.patch.set_lw = 1
            except AttributeError: pass

def legend_label_colors(leg = None):
    """
    Gives the labels from a legend the same color as the associated lines.
    """
    if leg is None:
        leg = plt.gca().get_legend()

    for text,line in zip(leg.get_texts(), leg.get_lines()):
        plt.setp(text, color = line.get_color())

def add_markers(N=10, filled = True, ax = None):
    '''
    Adds (grafx like) markers lines of the current axis

    Arguments:
        *N*:
            number of markers on a line
            the spacing is based on data visible
            in the plot, adjusting the axis will
            change the number of markers shown

        *filled*:
            if True, filled markers are used
            if False, open markers are used

        *ax*
            the axes to add markers to, if None,
            the current axes is used

    '''
    if ax == None: ax = plt.gca()
    lines = ax.get_lines()
    bgcolor = ax.get_axis_bgcolor()
    ax.markerindex = 0
    for line in lines:
        x = line.get_xdata()
        y = line.get_ydata()
        c = line.get_color()
        xmin, xmax, ymin, ymax = ax.axis()
        mask = (x >= xmin) * (x <= xmax) * (y >= ymin) * (y <= ymax)
        numpoints = len(x[mask])
        line.set_marker(nrfs_default_markers[ax.markerindex])
        ax.markerindex += 1
        line.set_markeredgecolor(c)
        if filled:
            line.set_markerfacecolor(c)
        else:
            line.set_markerfacecolor('None')
        line.set_markevery(np.max((int(numpoints / N),1)))
        plt.draw()

def plots_from_excel_list(inData,inExcelFileName,inTargetDir,
                          testname='testname',inOptions='', inMask=None, extraComment=''):
    """
    Generates plots defined in a special formatted excel file.
    It also generates a MS-Word VBA script to import the generated
    plots into a word document.

    Arguments:
        *inData*:
            nrfs_data object

        *inExcelFileName* :
            path and file name of excel file with plot definitions

        *inTargetDir* :
            directory to store results

        *testname*
            name of the test (used also for VBA function name and plotcomment)

        *inOptions* :
            * 'v' - verbose, print debug info
            * 'c' - close, close figures after saving
            * 'm' - markers, add markers
            * 'e' - create .eps images instead of .png

        *inMask* :
            np.ndarray of Booleans to be used as masker for plots

        *extraComment* :
            optional extra comment for plotcomment
    """

    # version 0.7.1 or higher required
    from xlrd import open_workbook,XL_CELL_EMPTY,XL_CELL_TEXT,XL_CELL_NUMBER

    # check options
    bVerbose     = 'v' in inOptions
    bClose       = 'c' in inOptions
    bMarkers     = 'm' in inOptions
    bEPS         = 'e' in inOptions

    # set mask to True if not given
    if inMask==None:
        inMask = np.ones(inData.Npnt,dtype=bool)

    if (bVerbose): print "[plots_from_excel_list] file:",inExcelFileName
    if (bClose): plt.ioff()

    # create directory if it does not exists
    if inTargetDir != '' :
        if not os.path.isdir(inTargetDir):
            os.makedirs(inTargetDir)

    # open .xls and relevant sheets
    wb = open_workbook(inExcelFileName)
    sh_signals = wb.sheet_by_name('signals')
    sh_plots = wb.sheet_by_name('plots')

    # from the first sheet find out what signals are in what plot
    # these define the columns used in the excel file
    col_comment    = 0
    col_y_sig      = 4
    col_group_no   = 5
    col_alt_x1     = 6
    col_alt_x2     = 7

    plot_signals = {}
    for i in range(0,sh_signals.nrows):
        if (sh_signals.cell(i, col_comment ).ctype == XL_CELL_EMPTY and
            sh_signals.cell(i, col_y_sig   ).ctype == XL_CELL_TEXT  and
            sh_signals.cell(i, col_group_no).ctype == XL_CELL_NUMBER):

            # we have a label and a plot_no
            y_sig  = (str(sh_signals.cell(i, col_y_sig   ).value)).strip()
            group  =  int(sh_signals.cell(i, col_group_no).value)
            alt_x1 = (str(sh_signals.cell(i, col_alt_x1  ).value)).strip()
            alt_x2 = (str(sh_signals.cell(i, col_alt_x2  ).value)).strip()
            if not (group in plot_signals.keys()):
                plot_signals[group] = []
            plot_signals[group].append((y_sig,alt_x1,alt_x2))

    # print the signals for each plot
    if (bVerbose):
        for k,v in plot_signals.items():
            print k,':',v

    # open the file for MS-Word VBA macro script
    macro = open(os.path.join(inTargetDir,testname+'.bas'),'w')
    macro.write('Sub '+testname+'()\n')
    macro.write('\n')

    # from the second sheet generate the plots

    # these define the columns used in the excel file
    col_comment    = 0
    col_group_no   = 1
    col_filename   = 2
    col_remark     = 3
    col_caption    = 4
    col_y_label    = 5
    col_y_prefix   = 6
    col_y_min      = 7
    col_y_max      = 8
    col_y_zero     = 9
    col_x1_sig     = 10
    col_x1_label   = 11
    col_x1_min     = 12
    col_x1_max     = 13
    col_legend1    = 14
    col_x2_sig     = 15
    col_x2_label   = 16
    col_x2_min     = 17
    col_x2_max     = 18
    col_legend2    = 19

    # loop over the rows in the excel sheet
    if bVerbose: print 'sh_plots.nrows: ',sh_plots.nrows
    for i in range(0,sh_plots.nrows):
        # (rough) check for a valid row
        if (sh_plots.cell(i, col_comment ).ctype == XL_CELL_EMPTY  and
            sh_plots.cell(i, col_group_no).ctype == XL_CELL_NUMBER and
            sh_plots.cell(i, col_filename).ctype == XL_CELL_TEXT   and
            sh_plots.cell(i, col_x1_sig  ).ctype == XL_CELL_TEXT):

            # we have a plot definition
            group     = int(sh_plots.cell(i, col_group_no).value)
            filename  = str(sh_plots.cell(i, col_filename).value)
            if bEPS:
                filename +='.eps'
            else:
                filename +='.png'
            if bVerbose: print 'plot :',filename

            # check for 2nd plot
            bDualPlot = (sh_plots.cell(i, col_x2_sig).ctype == XL_CELL_TEXT)

            # start the plot
            plt.figure()
            if bDualPlot: plt.axes((0.1,0.1,0.37,0.85))

            # y signal prefix ( '_A', '_R', ''
            y_prefix = (str(sh_plots.cell(i, col_y_prefix ).value)).strip()
            x_sig    = (str(sh_plots.cell(i, col_x1_sig   ).value)).strip()

            if group not in plot_signals.keys():
                raise ValueError, 'group number '+str(group)+' not in signals'

            for y_sig in plot_signals[group]:
                y = y_prefix + y_sig[0]
                x = x_sig
                if not (y_sig[1] == ''): x = y_sig[1] # alt x-axis 1
                if bVerbose: print 'plot: ',x,y
                if sh_plots.cell(i, col_y_zero ).value == 1:
                   plt.plot(inData.chn[x][inMask],
                            (inData.chn[y]-inData.chn[y][0])[inMask],
                            label=y)
                else:
                   plt.plot(inData.chn[x][inMask],
                            inData.chn[y][inMask],
                            label=y)

            # set limits
            if sh_plots.cell(i, col_x1_min ).ctype == XL_CELL_NUMBER:
                plt.xlim(xmin=float(sh_plots.cell(i, col_x1_min ).value))
            if sh_plots.cell(i, col_x1_max ).ctype == XL_CELL_NUMBER:
                plt.xlim(xmax=float(sh_plots.cell(i, col_x1_max ).value))
            if sh_plots.cell(i, col_y_min ).ctype == XL_CELL_NUMBER:
                plt.ylim(ymin=float(sh_plots.cell(i, col_y_min ).value))
            if sh_plots.cell(i, col_y_max ).ctype == XL_CELL_NUMBER:
                plt.ylim(ymax=float(sh_plots.cell(i, col_y_max ).value))

            if bMarkers: add_markers()

            # set axis labels
            plt.xlabel(str(sh_plots.cell(i, col_x1_label ).value))
            plt.ylabel(str(sh_plots.cell(i, col_y_label ).value))

            # set legend
            if sh_plots.cell(i, col_legend1 ).ctype == XL_CELL_NUMBER:
                plt.legend(loc=int(sh_plots.cell(i, col_legend1 ).value))
                legend_label_colors()

            # write plot comment
            comment = testname + ' | '
            if extraComment != '': comment += extraComment + ' | '
            comment += str(sh_plots.cell(i, col_remark ).value) + ' | '
            comment += filename
            plotcomment(comment)

            # if neccesary 2nd plot
            if bDualPlot:

                if bVerbose: print '2nd plot'
                #plt.subplot(122)
                plt.axes((0.6,0.1,0.37,0.85))

                # y signal prefix ( '_A', '_R', ''
                y_prefix = str(sh_plots.cell(i, col_y_prefix ).value)
                x_sig    = str(sh_plots.cell(i, col_x2_sig   ).value)

                for y_sig in plot_signals[group]:
                    y = y_prefix + y_sig[0]
                    x = x_sig
                    if not (y_sig[2] == ''): x = y_sig[2] # alt x-axis 2
                    if bVerbose: print 'plot: ',x,y
                    if sh_plots.cell(i, col_y_zero ).value == 1:
                        plt.plot(inData.chn[x][inMask],
                                 (inData.chn[y]-inData.chn[y][0])[inMask],
                                 label=y)
                    else:
                        plt.plot(inData.chn[x][inMask],
                                 inData.chn[y][inMask],
                                 label=y)

                # set limits
                if sh_plots.cell(i, col_x2_min ).ctype == XL_CELL_NUMBER:
                    plt.xlim(xmin=float(sh_plots.cell(i, col_x2_min ).value))
                if sh_plots.cell(i, col_x2_max ).ctype == XL_CELL_NUMBER:
                    plt.xlim(xmax=float(sh_plots.cell(i, col_x2_max ).value))
                if sh_plots.cell(i, col_y_min ).ctype == XL_CELL_NUMBER:
                    plt.ylim(ymin=float(sh_plots.cell(i, col_y_min ).value))
                if sh_plots.cell(i, col_y_max ).ctype == XL_CELL_NUMBER:
                    plt.ylim(ymax=float(sh_plots.cell(i, col_y_max ).value))

                if bMarkers: add_markers()

                # set axis labels
                plt.xlabel(str(sh_plots.cell(i, col_x2_label ).value))
                plt.ylabel(str(sh_plots.cell(i, col_y_label  ).value))

                # set legend
                if sh_plots.cell(i, col_legend2 ).ctype == XL_CELL_NUMBER:
                    plt.legend(loc=int(sh_plots.cell(i, col_legend2 ).value))
                    legend_label_colors()

            # save the figure
            savefig(os.path.join(inTargetDir,filename))

            if (bClose):
                plt.close()
                plt.ioff()

            # write VBA script
            abs_filename = os.path.abspath(os.path.join(inTargetDir,(filename)))
            macro.write('  Selection.InlineShapes.AddPicture _\n')
            macro.write('    FileName         := "'+abs_filename+'", _\n')
            macro.write('    LinkToFile       :=True, _\n')
            macro.write('    SaveWithDocument :=True \n')
            macro.write('  Selection.TypeParagraph\n')
            macro.write('  Selection.InsertCaption _\n')
            macro.write('    Label:="Figure", _\n')
            macro.write('    TitleAutoText:="InsertCaption1", _\n')
            macro.write('    Title:="", _\n')
            macro.write('    Position:=wdCaptionPositionBelow \n')
            macro.write('  Selection.TypeText Text:=" ' + \
                           str(sh_plots.cell(i, col_caption ).value) + \
                           '"\n')
            macro.write('  Selection.TypeParagraph\n')
            macro.write('\n')

    # close the macro script file
    macro.write('End Sub\n')
    macro.close()

    if (bClose): plt.ion()

def append_axes(rows = 1, cols=1, h = 1, hspace = 0.05, wspace = 0.1):
    '''
    fills the area empty space below any axes instances
    present in a figure with a grid of new axes instances

    Arguments:
        *rows* :
            number of rows

        *cols* :
            number of columns

        *h* :
            the height of the figure to be filled
            (fraction of figure height). If h is greater
            than the available height this is used.

        *hspace* :
            horizontal space between axes (fraction of figure)

        *wspace* :
            vertical space between axes (fraction of figure)

    Returns:
        list of axes instances, starting with top left

    '''
    #get the setting from rcParams
    rcleft = plt.rcParams['figure.subplot.left']
    rcright = plt.rcParams['figure.subplot.right']
    rcwidth = rcright - rcleft
    rctop = plt.rcParams['figure.subplot.top']
    rcbottom = plt.rcParams['figure.subplot.bottom']
    rcheight = rctop - rcbottom

    #get the bottom y coordinate of each axes in the current figure (gcf() creates a figure if none)
    axbottoms = [ax.get_position().get_points()[0][1] for ax in plt.gcf().get_axes()]

    #top of new axes is below present axes
    if axbottoms: top = np.min(axbottoms) - hspace
    else:         top = rctop

    bottom = np.max((top - h, rcbottom))
    if ( top - (rows - 1) * hspace ) <= bottom:
        raise ValueError, 'no space available below lowest axes'

    #create lists with coordinates and dimensions for new axes
    height = ((top - bottom) - (rows - 1) * hspace)/rows
    bottoms = [(bottom + i * (height + hspace)) for i in range(rows)]
    width = (rcwidth - (cols-1) * wspace)/cols
    lefts = [(rcleft + i * (width + wspace)) for i in range(cols)]

    #return a list of axes instances
    return [plt.axes([lefts[j],bottoms[i], width, height]) for i in range(rows-1,-1,-1) for j in range(cols) ]



# ==== nrfslib Calculation Functions =================================
# ===================================================================

class Parameter:
    """
    Helper class for the 'fit' function from the SciPy CookBook

    """
    def __init__(self, value):
        self.value = value

    def set(self, value):
        self.value = value

    def __call__(self):
        return self.value

def fit(function, parameters, y, x = None):
    """
    function from SciPy CookBook, 'Fitting Data',

    (from http://www.scipy.org/Cookbook/FittingData)

    Example::

        data_x = array([0,1,2,3,4])
        data_y = array([0,1,4,10,15])

        a = nrfs.Parameter(1)
        b = nrfs.Parameter(1)
        c = nrfs.Parameter(1)

        def f(x):
            return a() * x **2 + b() * x + c()

        nrfs.fit(f, [a,b,c], data_y, data_x)

        plot(data_x,data_y,'ro')
        fun_x = arange(0,4,0.1)
        plot(fun_x,f(fun_x))

    """
    def f(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return y - function(x)

    if x is None: x = np.arange(y.shape[0])
    p = [param() for param in parameters]
    sp.optimize.leastsq(f, p)


def smooth(x,window_len=11,window='hanning'):
    """
    Smooth the data using a window with requested size.
    (from http://www.scipy.org/Cookbook/SignalSmooth)

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    Arguments :

        *x* :
            the input signal (1D np.ndarray)

        *window_len* :
            the dimension of the smoothing window; should be an odd integer

        *window*:
            the type of window
            ['flat'|'hanning'|'hamming'|'bartlett'|'blackman']

            flat window will produce a moving average smoothing.

    Returns:
        the smoothed signal (1D np.ndarray)

    example::
        t=linspace(-2,2,0.1)
        x=sin(t)+randn(len(t))*0.1
        y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman,
    numpy.convolve, scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array
    instead of a string
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s=np.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

def nojump(x, max_pos_jump, max_neg_jump):
    """
    Removes 'jumps' from signals, use with caution! by subsequentially
    adapting the offset of a signal in case of a 'jump' to make a
    'continues' signal.

    Arguments:
        *x* :
            the input signal (1D np.ndarray)

        *max_pos_jump*, *max_neg_jump* :
            maximum absolute jumps in positive and negative direction

    Returns:
        The 'de-jumped' signal (1D np.ndarray)
    """
    # sanity check
    if x.ndim != 1:
        raise ValueError, "nojump only accepts 1 dimension arrays."

    offset = 0.0
    N = x.size
    retval = np.empty((N,))
    retval[0] = x[0]
    for i in range(1,N):
        if   x[i] > x[i-1] + max_pos_jump : offset -= (x[i]-x[i-1])
        elif x[i] < x[i-1] - max_neg_jump : offset -= (x[i]-x[i-1])
        retval[i] = x[i] + offset
    return retval

def skip_after_jump(x, max_pos_jump, max_neg_jump):
    """
    Removes all values after a jump by replacing these values with a NaN.

    Arguments:
        *x* :
            the input signal (1D np.ndarray)

        *max_pos_jump*, *max_neg_jump* :
            maximum absolute jumps in positive and negative direction

    Returns:
        The signal chopped at the first jump (1D np.ndarray)
    """
    # sanity check
    if x.ndim != 1:
        raise ValueError, "skip_after_jump only accepts 1 dimension arrays."

    N = x.size
    retval = x.copy()
    for i in range(1,N):
        if  retval[i] > retval[i-1] + max_pos_jump or \
            retval[i] < retval[i-1] - max_neg_jump    :
            retval[i:] = np.nan
            break
    return retval

def limits(x, lower_limit, upper_limit):
    """
    Removes values ouside given limits from signals, by replacing
    these values with a NaN.

    Arguments:
        *x* :
            the input signal (1D np.ndarray)

        *lower_limit*, *upper_limit* :
            lower and upper limit

    Returns:
        The limited signal (1D np.ndarray)

    """
    # sanity check
    if x.ndim != 1:
        raise ValueError, "valid_values only accepts 1 dimension arrays."


    retval = x.copy()
    retval[retval<lower_limit] = np.nan
    retval[retval>upper_limit] = np.nan
    return retval

def despike(x, max_deviation):
    """
    Removes spikes from signals, by replacing
    these values with a NaN.

    Arguments:
        *x* :
            the input signal (1D np.ndarray)

        *max_deviation* :
            Maximim allowable deviation (float)

    Returns:
        The despiked signal (1D np.ndarray)

    """
    # sanity check
    if x.ndim != 1:
        raise ValueError, "despike only accepts 1 dimension arrays."

    N = x.size
    last_valid_value = x[0]
    retval = np.empty((N,))
    retval[0] = x[0]
    for i in range(1,N):
        if (x[i] > last_valid_value + max_deviation or
            x[i] < last_valid_value - max_deviation ):
            retval[i] = np.nan
        else :
            retval[i] = x[i]
            last_valid_value = x[i]
    return retval


def lfilter_zi(b,a):
    """
    helper function for filtfilt
    (from http://www.scipy.org/Cookbook/FiltFilt)
    """
    #compute the zi state from the filter parameters. see [Gust96].

    #Based on:
    # [Gust96] Fredrik Gustafsson, Determining the initial states in forward-backward
    # filtering, IEEE Transactions on Signal Processing, pp. 988--992, April 1996,
    # Volume 44, Issue 4

    n=max(len(a),len(b))

    zin = (np.eye(n-1) - np.hstack( (-a[1:n,np.newaxis],
                                 np.vstack((np.eye(n-2), np.zeros(n-2))))))

    zid=  b[1:n] - a[1:n]*b[0]

    zi_matrix=np.linalg.inv(zin)*(np.matrix(zid).transpose())
    zi_return=[]

    # convert the result into a regular array (not a matrix)
    for i in range(len(zi_matrix)):
      zi_return.append(float(zi_matrix[i][0]))

    return np.array(zi_return)

def filtfilt(b,a,x):
    """
    zero phase delay filter
    (from http://www.scipy.org/Cookbook/FiltFilt)

    Arguments:
        *b*, *a*:
            IIR filter coefficients (lists or 1D np.arrays of the same size),
            these can be calculated with
        *x*:
            the input signal (1D np.ndarray)

    Returns:
        The filtered signal (1D np.ndarray)

    """
    # for now only accepting 1d arrays
    ntaps=max(len(a),len(b))
    edge=ntaps*3

    if x.ndim != 1:
        raise ValueError, "filtfilt is only accepting 1 dimension arrays."

    # x must be bigger than edge
    if x.size < edge:
        raise ValueError, "Input vector needs to be bigger than 3 * max(len(a),len(b)."

    if len(a) < ntaps:
        a = np.r_[a,np.zeros(len(b)-len(a))]

    if len(b) < ntaps:
        b = np.r_[b,np.zeros(len(a)-len(b))]

    zi=lfilter_zi(b,a)

    # Grow the signal to have edges for stabilizing
    # the filter with inverted replicas of the signal
    s=np.r_[2*x[0]-x[edge:1:-1],x,2*x[-1]-x[-1:-edge:-1]]
    # in the case of one go we only need one of the extrems
    # both are needed for filtfilt

    (y,zf)=sp.signal.lfilter(b,a,s,-1,zi*s[0])

    (y,zf)=sp.signal.lfilter(b,a,np.flipud(y),-1,zi*y[-1])

    return np.flipud(y[edge-1:-edge+1])


def lowpass(x, Fs, Ff, N=1):
    """
    Filters singnal 'x' with a 'N'-th order lowpass filter.

    It uses filtfilt and signal.iirfilter

    Arguments:
        *Fs* :
            sample frequency
        *Ff* :
            filter frequency
        *N* :
            filter order
    Returns:
        filtered signal
    """
    Wn = [(2.0 * Ff ) / Fs, (2.0 * Ff) / Fs]
    (b, a) = sp.signal.iirfilter(N, Wn, btype='lowpass')
    return filtfilt(b, a, x)

def argspeaks(x, threshold=0.0):
    """

    Detects peaks in a 1D numpy array and returns arrays with indices of the
    minima and maxima. To eliminate peaks caused by noise a noise threshold
    can be given.

    Arguments:

        *x* :
            the input signal (1D np.ndarray)

        *threshold* :
            threshold value for peaks caused by 'noise'

    example::

        # make a nice signal
        N = 200
        x = np.linspace(0.0, 1.0, N)
        y = ( 0.5 * x  +
              0.1 * np.sin(8.0 * np.pi * x) +
              1.0 * np.exp(-4.0 * x) * (np.random.random(len(x)) - 0.5) )
        y[0:N/10] = 0.0

        # detect (indices of) peaks
        mins, maxs = argspeaks(y, .1)

        print mins, maxs

        # plot signal and peaks
        plt.close('all')
        plt.plot(x, y, 'g-')
        plt.plot(x[mins], y[mins], 'bo')
        plt.plot(x[maxs], y[maxs], 'ro')

    """

    # sanity check on `x`
    if (not type(x) is np.ndarray) or len(x.shape) != 1 or len(x) < 2 :
        raise ValueError, 'a should be 1D numpy ndarray with length >= 2'

    # init some stuff
    N = len(x)
    local_max = local_min = 0
    max_indices = np.zeros(N, dtype=np.bool) # i.e. [False, False, .....]
    min_indices = np.zeros(N, dtype=np.bool)
    all_indices = np.arange(N, dtype=np.int32)

    # initialize direction, see [1]
    rising = x[1] > x[0]

    # let's loop
    for i in range(1, N):

        if x[i] > x[local_max]:
            local_max = i

        if x[i] < x[local_min]:
            local_min = i

        if rising:
            if x[i] < (x[local_max] - threshold):
                max_indices[local_max] = True
                local_min = i
                rising = False
        else:
            if x[i] > (x[local_min] + threshold):
                min_indices[local_min] = True
                local_max = i
                rising = True


    # [1] so far so good, however because of the lousy initialisation
    # we migth have a wrong (false positive) first peak, let's check it,
    # the first point (index 0) cannot be a peak and we have to check the
    # first peak in reverse
    min_indices[0] = False
    max_indices[0] = False
    mins = all_indices[min_indices]
    maxs = all_indices[max_indices]
    if len(mins>0):
        if not np.max(x[0:mins[0]]) > x[mins[0]] + threshold:
            min_indices[mins[0]] = False
    if len(maxs>0):
        if not np.min(x[0:maxs[0]]) < x[maxs[0]] - threshold:
            max_indices[maxs[0]] = False

    # ok, now we're really done
    mins = all_indices[min_indices]
    maxs = all_indices[max_indices]
    return mins, maxs


def append_nrfs_data(inList):
    """
    Appends multiple nrfs_data objects, and returns a new nrfs_data object
    """
    if (len(inList)<=1):
        raise ValueError, 'not enough objects given'

    Npnt = 0
    for part in inList:
        Npnt += part.Npnt

    wd = nrfs_data(Npnt)

    index = 0;
    for part in inList:
        for chn in part:
            if not chn in wd:
                dtype = part[chn].dtype
                if dtype==np.float64:
                    wd[chn] = nans((Npnt,),dtype=dtype)
                else:
                    wd[chn] = np.zeros((Npnt,),dtype=dtype)
            wd[chn][index:index + part.Npnt] = part[chn]
        index += part.Npnt

    return wd

def join_nrfs_data(inList):
    """
    Join multiple nrfs_data objects from multiple stations
    """
    if (len(inList)<=1):
        raise ValueError, 'not enough objects given'

    min_len = 99999999;
    for part in inList:
        min_len = min(min_len,part.Npnt)

    wd = nrfs_data(min_len)

    for part in inList:
        for chn in part:
            wd[chn] = deepcopy(part[chn][0:min_len])
    return wd

# ==== nrfslib Blade Specific Functions ==============================
# ===================================================================

#

# ==== nrfslib Geometrical Functions =================================
# ===================================================================


def geom_2D_dist(lp1,lp2):
    """
    Calculate distance between 2D points.

    Arguments:
        *lp1*, *lp2*:
            2D points or arrays of 2D points.
            (np.ndarrays where the last axis has length 2)

    Returns:
        array of distances (np.ndarray)
    """
    # check 2D
    if (lp1.shape[-1] != 2): raise ValueError, "lp1 contains no 2D points"
    if (lp2.shape[-1] != 2): raise ValueError, "lp2 contains no 2D points"
    # some trickery to make it work on points and arrays of points
    vects = lp2 - lp1
    a = len(vects.shape)
    squares = np.square(vects)
    dist =  np.sqrt(np.sum(squares, axis = a-1))
    return dist

def geom_2D_closest_point(lp1,lp2,lp3):
    """
    Determine if point p1 or p2 is closest to p3.

    Arguments:
        *lp1*, *lp2*, *lp3*:
            2D points or arrays of 2D points.
            (np.ndarrays where the last axis has length 2)

    Returns:
        array of 2D points (np.ndarray)
    """
    # check 2D
    if (lp1.shape[-1] != 2): raise ValueError, "lp1 contains no 2D points"
    if (lp2.shape[-1] != 2): raise ValueError, "lp2 contains no 2D points"
    if (lp3.shape[-1] != 2): raise ValueError, "lp3 contains no 2D points"
    # create arrays of distances
    d1 = geom_2D_dist(lp1,lp3)
    d2 = geom_2D_dist(lp2,lp3)
    # create list of indeces (False=0, True=1)
    bool_list = d2 > d1
    # A boolean converted to real results in: True->1.0, False 0.0
    # probably there should be a better method to do this
    b1 = np.transpose(np.array([bool_list + 0.0,bool_list + 0.0]))
    b2 = np.transpose(np.array([1.0 - bool_list,1.0 - bool_list]))
    return lp1 * b1 + lp2 * b2

def geom_2D_trilateration(lp1,l1,lp2,l2):
    """
    Calculate points at distance l1 from lp1, and l2 from lp2, if no
    such point is found NaN's are returned.

    Arguments:
        *lp1*, *lp2*:
            2D points or arrays of 2D points.
            (np.ndarrays where the last axis has length 2)
        *l1*, *l2*:
            floats of array of floats

    Returns:
        a tuple of two array with 2D points (np.ndarray)
    """
    # check 2D
    if (lp1.shape[-1] != 2): raise ValueError, "lp1 contains no 2D points"
    if (lp2.shape[-1] != 2): raise ValueError, "lp2 contains no 2D points"

    # distance between p1 and p2
    a = geom_2D_dist(lp1,lp2)

    # norm vector from p2 to p1
    px = (lp1[...,0]-lp2[...,0])/a;
    py = (lp1[...,1]-lp2[...,1])/a;

    # and a norm vector perpendicular to the previous one
    qx =  py;
    qy = -px;

    # we construct a line perdendicular to line p1-p2 and cross a possible
    # target point. We construct a point where this line and line p1-p2 cross.
    # a2 is the distance between this point and and p2
    # h is the distance between this point and the possible target point.
    # Now we apply two times pythagoras theorem, we have two equations and
    # two unknowns.

    a2 = (l2**2-l1**2+a**2) / (2*a);
    h =  np.sqrt((l2**2)-(a2**2));

    x1 = lp2[...,0] + a2 * px + h * qx
    y1 = lp2[...,1] + a2 * py + h * qy
    x2 = lp2[...,0] + a2 * px - h * qx
    y2 = lp2[...,1] + a2 * py - h * qy

    result1 =  np.transpose(np.array([x1,y1]))
    result2 =  np.transpose(np.array([x2,y2]))
    return result1,result2

def geom_2D_lab_to_rod_forces(lp1,lp2,lc,fx,fy):
    """
    Decompose lab forces (`fx`, `fy`) to forces `f1`, `f2`
    along the rods `r1`, `r2`.

    `r1` runs from `c(x,y)` to `p1(x,y)`,

    `r2` runs from `c(x,y)` to `p2(x,y)`.

    Arguments:
        *lp1*, *lp2*, *lc*:
            2D points or arrays of 2D points.
            (np.ndarrays where the last axis has length 2)
        *f1*, *f2*:
            floats of array of floats

    Returns:
        tuple of arrays
    """
    # check 2D
    if (lp1.shape[-1] != 2): raise ValueError, "lp1 contains no 2D points"
    if (lp2.shape[-1] != 2): raise ValueError, "lp2 contains no 2D points"
    if ( lc.shape[-1] != 2): raise ValueError, "lc  contains no 2D points"
    # convert parameters to arrays if the were not arrays
    if (len(lp1.shape)==1): lp1 = np.array([lp1])
    if (len(lp2.shape)==1): lp2 = np.array([lp2])
    if (len( lc.shape)==1):  lc = np.array([ lc])
    # 2D, write out completely
    v1x = lp1[:,0] - lc[:,0]
    v1y = lp1[:,1] - lc[:,1]
    v2x = lp2[:,0] - lc[:,0]
    v2y = lp2[:,1] - lc[:,1]
    # lengths of the rods (already known)
    l1 = np.sqrt(v1x**2 + v1y**2)
    l2 = np.sqrt(v2x**2 + v2y**2)
    # lab to rod matrix
    rl_11 = v1x / l1
    rl_12 = v2x / l2
    rl_21 = v1y / l1
    rl_22 = v2y / l2
    # determinant
    det = rl_11 * rl_22 - rl_12 * rl_21
    # inverse of 2x2 matrix => rod to lab
    lr_11 =   rl_22 / det
    lr_12 = - rl_12 / det
    lr_21 = - rl_21 / det
    lr_22 =   rl_11 / det
    #
    f1 = lr_11 * fx + lr_12 *fy
    f2 = lr_21 * fx + lr_22 *fy
    return f1,f2

def geom_2D_rod_to_lab_forces(lp1,lp2,lc,f1,f2):
    """
    decompose rod forces *f1*,*f2* to lab forces.
    The rod with *f1* runs from *c* to *p1*.
    The rod with *f2* runs from *c* to *p2*.

    Arguments:
        *f1*, *f2*:
            forces (float or list/array of floats)

        *lp1*, *lp2*, *lc*:
            centre and points which define the rods (directions).

    Returns:
        a tuple with nd.arrays of Fx and Fy

    """
    # check 2D
    if (lp1.shape[-1] != 2): raise ValueError, "lp1 contains no 2D points"
    if (lp2.shape[-1] != 2): raise ValueError, "lp2 contains no 2D points"
    if ( lc.shape[-1] != 2): raise ValueError, "lc  contains no 2D points"
    # convert parameters to arrays if the were not arrays
    if (len(lp1.shape)==1): lp1 = np.array([lp1])
    if (len(lp2.shape)==1): lp2 = np.array([lp2])
    if (len( lc.shape)==1):  lc = np.array([ lc])
    # 2D, write out completely
    v1x = lp1[:,0] - lc[:,0]
    v1y = lp1[:,1] - lc[:,1]
    v2x = lp2[:,0] - lc[:,0]
    v2y = lp2[:,1] - lc[:,1]
    # lengths of the rods (already known)
    l1 = np.sqrt(v1x**2 + v1y**2)
    l2 = np.sqrt(v2x**2 + v2y**2)
    # lab to rod matrix
    rl_11 = v1x / l1
    rl_12 = v2x / l2
    rl_21 = v1y / l1
    rl_22 = v2y / l2
    #
    fx = rl_11 * f1 + rl_12 *f2
    fy = rl_21 * f1 + rl_22 *f2
    return fx,fy

def geom_3D_dist(lp1,lp2):
    """
    Calculate distance beween 3D points.

    Arguments:
        *lp1*, *lp2*:
            np.ndarray of 3D points or a single 3D point

    Returns:
        distance (float or np.ndarray of float)

    """
    # check 3D
    if (lp1.shape[-1] != 3): raise ValueError, "lp1 contains no 3D points"
    if (lp2.shape[-1] != 3): raise ValueError, "lp2 contains no 3D points"
    # some trickery to make it work on points and arrays of points
    vects = lp2 - lp1
    a = len(vects.shape)
    squares = np.square(vects)
    dist =  np.sqrt(np.sum(squares, axis = a-1))
    return dist

def geom_3D_closest_point(lp1,lp2,lp3):
    """
    return a list with points from either lp1 or lp2 which is closest
    to point p3(x,y,z)

    lp1,lp2        - array's/lists/tuples of points(x,y,z)
    lp3            - reference point p3(x,y,z)
    (if there is a NaN in either lp1 or lp2 a NaN point is returned)
    """
    # check 3D
    if (lp1.shape[-1] != 3): raise ValueError, "lp1 contains no 3D points"
    if (lp2.shape[-1] != 3): raise ValueError, "lp2 contains no 3D points"
    if (lp3.shape[-1] != 3): raise ValueError, "lp3 contains no 3D points"
    # create arrays of distances
    d1 = geom_3D_dist(lp1,lp3)
    d2 = geom_3D_dist(lp2,lp3)
    # create list of indeces (False=0, True=1)
    bool_list = d2 > d1
    # A boolean converted to real results in: True->1.0, False 0.0
    # probably there should be a better method to do this
    b1 = np.transpose(np.array([bool_list + 0.0,bool_list + 0.0,bool_list + 0.0]))
    b2 = np.transpose(np.array([1.0 - bool_list,1.0 - bool_list,1.0 - bool_list]))
    return lp1 * b1 + lp2 * b2

def geom_3D_trilateration(p1,ld1,p2,ld2,p3,ld3):
    """
    find the 2 points on distances ld1,ld2,ld3 from points lp1,lp2 and lp3
    lp1,lp2,lp3    - array's/lists/tuples of points(x,y,z)
    ld1,ld2,ld3    - array's/lists/tuples of distances
    """

    # convert to numpy array's
    points = np.array( [ [ p1[0], p1[1], p1[2], 1.0 ],
                         [ p2[0], p2[1], p2[2], 1.0 ],
                         [ p3[0], p3[1], p3[2], 1.0 ] ] )
    d1 = np.array(ld1)
    d2 = np.array(ld2)
    d3 = np.array(ld3)

    # we gaan een nieuw assenstelsel maken zodat p1 in de oorsprong ligt, p2
    # op de x-as ligt en p3 in het xy-vlak

    # translatie zodat p1 in de oorsprong komt
    trans01 = np.array( [ [ 1.0         , 0.0         , 0.0         , 0.0 ],
                          [ 0.0         , 1.0         , 0.0         , 0.0 ],
                          [ 0.0         , 0.0         , 1.0         , 0.0 ],
                          [-points[0][0],-points[0][1],-points[0][2], 1.0 ] ] )
    points = np.dot(points,trans01)

    # rotatie om de z-as zodat de projectie van p2 op het xy-vlak
    # op de y-as komt te liggen (en daardoor p2 in het xz-vlak)
    phiz = np.arctan2(points[1][1],points[1][0])
    rot01 = np.array( [ [ np.cos(phiz),-np.sin(phiz), 0.0, 0.0 ],
                        [ np.sin(phiz), np.cos(phiz), 0.0, 0.0 ],
                        [ 0.0         , 0.0         , 1.0, 0.0 ],
                        [ 0.0         , 0.0         , 0.0, 1.0 ] ] )
    points = np.dot(points,rot01)

    # rotatie om de (nieuwe) y-as zodat p2 op de x-as komt te liggen
    phiy = - np.arctan2(points[1][2],points[1][0])
    rot02 = np.array( [ [ np.cos(phiy), 0.0, np.sin(phiy), 0.0 ],
                        [ 0.0         , 1.0, 0.0         , 0.0 ],
                        [-np.sin(phiy), 0.0, np.cos(phiy), 0.0 ],
                        [ 0.0         , 0.0, 0.0         , 1.0 ] ] )
    points = np.dot(points,rot02)

    # rotatie om de (nieuwe) x-as zodat p3 in het xy-vlak komt te liggen
    phix = np.arctan2(points[2][2],points[2][1])
    rot03 = np.array( [ [ 1.0, 0.0         , 0.0         , 0.0 ],
                        [ 0.0, np.cos(phix),-np.sin(phix), 0.0 ],
                        [ 0.0, np.sin(phix), np.cos(phix), 0.0 ],
                        [ 0.0, 0.0         , 0.0         , 1.0 ] ] )
    points = np.dot(points,rot03)

    # in het nieuwe stelsel bereken we x,y,z van de bol doorsnijdingen

    # we gebruiken de naamgeving volgens Wikipedia (trilateration)
    d = points[1][0] # x-coor p2
    i = points[2][0] # x-coor p3
    j = points[2][1] # y coor p3

    # sommetjes, als er geen oplossing is krijgen we NaN's in de array's
    x  = ( d1**2 -d2**2 + d**2 ) / ( 2.0 * d )
    y  = ( d1**2 -d3**2 + i**2 +j**2 ) / ( 2.0 * j ) - ( i * x ) / j
    z1 = + np.sqrt( d1**2 - x**2 - y**2 )
    z2 = - np.sqrt( d1**2 - x**2 - y**2 )

    # oplossingen in punten arrays stoppen
    N = len(x)
    result1 = np.transpose(np.array([x,y,z1,np.ones(N)]))
    result2 = np.transpose(np.array([x,y,z2,np.ones(N)]))

    # bereken de terug transformeer matrix
    back = np.linalg.inv(np.dot(trans01,np.dot(rot01,np.dot(rot02,rot03))))

    # terug transformeren, en alleen x,y,z terug geven
    result1 = np.dot(result1,back)[:,0:3]
    result2 = np.dot(result2,back)[:,0:3]
    return result1,result2

def geom_3D_displacements_from_wire_transducers(inMeasurement,
                                                inInstall_Dat,
                                                inTransduc_Set,
                                                inWireLabelList):
    """
    returns array of 3D displacements with respects to the
    install.dat point based on the length changes of the two or three
    wiretransducers, given the measurement and install info

    inMeasurement       - nrfs_data object with the measurement
    inInstall_Dat       - nrfs_data object with the install.dat measurement
    inTransduc_Set      - key_valuefile object of the transduc.set file
    inWireLabels        - list of (2 or 3) labels of wire transducers

    Note: in case of two involved wire transducers the returned points
          are in the plane defined by the instal.dat point and the two
          starting points of the wire transducers
    """
    if len(inWireLabelList) == 2 :
        return geom_3D_displacements_from_2_wire_transducers(
                    inMeasurement,
                    inInstall_Dat,
                    inTransduc_Set,
                    inWireLabelList[0],
                    inWireLabelList[1])

    if len(inWireLabelList) == 3 :
        return geom_3D_displacements_from_3_wire_transducers(
                    inMeasurement,
                    inInstall_Dat,
                    inTransduc_Set,
                    inWireLabelList[0],
                    inWireLabelList[1],
                    inWireLabelList[2])

    raise ValueError, "need 2 or 3 wire labels to calculate displacements"

def geom_3D_displacements_from_wire_transducers_plane(inMeasurement,
                                                      inInstall_Dat,
                                                      inTransduc_Set,
                                                      inWireLabelList,
                                                      plane_def_vec):
    """
    returns array of 3D displacements with respects to the
    install.dat point based on the length changes of the two or three
    wiretransducers, given the measurement and install info

    inMeasurement       - nrfs_data object with the measurement
    inInstall_Dat       - nrfs_data object with the install.dat measurement
    inTransduc_Set      - key_valuefile object of the transduc.set file
    inWireLabels        - list of (2 or 3) labels of wire transducers

    Note: in case of two involved wire transducers the returned points
          are in the plane defined by the instal.dat point and
          the plane perpendicular to vect plane_def_vec.
    """
    if len(inWireLabelList) == 2 :
        return geom_3D_displacements_from_2_wire_transducers_plane(
                    inMeasurement,
                    inInstall_Dat,
                    inTransduc_Set,
                    inWireLabelList[0],
                    inWireLabelList[1],
                    plane_def_vec)

    if len(inWireLabelList) == 3 :
        return geom_3D_displacements_from_3_wire_transducers(
                    inMeasurement,
                    inInstall_Dat,
                    inTransduc_Set,
                    inWireLabelList[0],
                    inWireLabelList[1],
                    inWireLabelList[2])

    raise ValueError, "need 2 or 3 wire labels to calculate displacements"


def geom_3D_displacements_from_3_wire_transducers(inMeasurement,
                                                  inInstall_Dat,
                                                  inTransduc_Set,
                                                  inWireLabel1,
                                                  inWireLabel2,
                                                  inWireLabel3):
    """
    returns array of 3D displacements with respects to the
    install.dat point based on the length changes of the three
    wiretransducers given the measurement and install info
    inMeasurement       - nrfs_data object with the measurement
    inInstall_Dat       - nrfs_data object with the install.dat measurement
    inTransduc_Set      - key_valuefile object of the transduc.set file
    inWireLabels        - labels of the involved wire transducers
    """

    install_pnt = np.array([0.0,0.0,0.0])

    wire1_pnt = np.array([inTransduc_Set.__dict__[inWireLabel1+'_X'],
                          inTransduc_Set.__dict__[inWireLabel1+'_Y'],
                          inTransduc_Set.__dict__[inWireLabel1+'_Z']])
    wire2_pnt = np.array([inTransduc_Set.__dict__[inWireLabel2+'_X'],
                          inTransduc_Set.__dict__[inWireLabel2+'_Y'],
                          inTransduc_Set.__dict__[inWireLabel2+'_Z']])
    wire3_pnt = np.array([inTransduc_Set.__dict__[inWireLabel3+'_X'],
                          inTransduc_Set.__dict__[inWireLabel3+'_Y'],
                          inTransduc_Set.__dict__[inWireLabel3+'_Z']])

    wire1_offset = geom_3D_dist(install_pnt,wire1_pnt) - \
                   inInstall_Dat[inWireLabel1][0]
    wire2_offset = geom_3D_dist(install_pnt,wire2_pnt) - \
                   inInstall_Dat[inWireLabel2][0]
    wire3_offset = geom_3D_dist(install_pnt,wire3_pnt) - \
                   inInstall_Dat[inWireLabel3][0]

    r1,r2 = geom_3D_trilateration(
                wire1_pnt,inMeasurement[inWireLabel1] + wire1_offset,
                wire2_pnt,inMeasurement[inWireLabel2] + wire2_offset,
                wire3_pnt,inMeasurement[inWireLabel3] + wire3_offset)

    return geom_3D_closest_point(r1,r2,install_pnt)


def geom_3D_displacements_from_2_wire_transducers(inMeasurement,
                                                  inInstall_Dat,
                                                  inTransduc_Set,
                                                  inWireLabel1,
                                                  inWireLabel2):
    """
    returns array of 3D displacements with respects to the
    install.dat point based on the length changes of the two
    wire transducers given the measurement and install info.

    Note: returned points are in the plane defined by the instal.dat point
    and the two starting points of the wire transducers.

    Parameters:
        *inMeasurement*:
            nrfs_data object with the measurement

        *inInstall_Dat*:
            nrfs_data object with the install.dat measurement

        *inTransduc_Set*:
            key_valuefile object of the transduc.set file

        *inWireLabels*:
            labels of the involved wire transducers

    """

    install_pnt = np.array([0.0,0.0,0.0])

    # pas op 4 getallen vanwege latere geometrische matrix manipulatie
    wire1_pnt = np.array([inTransduc_Set.__dict__[inWireLabel1+'_X'],
                          inTransduc_Set.__dict__[inWireLabel1+'_Y'],
                          inTransduc_Set.__dict__[inWireLabel1+'_Z'],0.0])
    wire2_pnt = np.array([inTransduc_Set.__dict__[inWireLabel2+'_X'],
                          inTransduc_Set.__dict__[inWireLabel2+'_Y'],
                          inTransduc_Set.__dict__[inWireLabel2+'_Z'],0.0])

    wire1_offset = geom_3D_dist(install_pnt,wire1_pnt[0:3]) - \
                   inInstall_Dat[inWireLabel1][0]
    wire2_offset = geom_3D_dist(install_pnt,wire2_pnt[0:3]) - \
                   inInstall_Dat[inWireLabel2][0]

    # we gaan een nieuw assenstelsel maken zodat install_pnt in de oorsprong
    # ligt, wire1_pnt op de x-as ligt en wire2_pnt in het xy-vlak

    # rotatie om de z-as zodat de projectie van wire1_pnt op het xy-vlak
    # op de y-as komt te liggen (en daardoor wire1_pnt in het xz-vlak)
    phiz = np.arctan2(wire1_pnt[1],wire1_pnt[0])
    rot01 = np.array( [ [ np.cos(phiz),-np.sin(phiz), 0.0, 0.0 ],
                        [ np.sin(phiz), np.cos(phiz), 0.0, 0.0 ],
                        [ 0.0         , 0.0         , 1.0, 0.0 ],
                        [ 0.0         , 0.0         , 0.0, 1.0 ] ] )
    wire1_pnt = np.dot(wire1_pnt,rot01)
    wire2_pnt = np.dot(wire2_pnt,rot01)

    # rotatie om de (nieuwe) y-as zodat wire1_pnt op de x-as komt te liggen
    phiy = - np.arctan2(wire1_pnt[2],wire1_pnt[0])
    rot02 = np.array( [ [ np.cos(phiy), 0.0, np.sin(phiy), 0.0 ],
                        [ 0.0         , 1.0, 0.0         , 0.0 ],
                        [-np.sin(phiy), 0.0, np.cos(phiy), 0.0 ],
                        [ 0.0         , 0.0, 0.0         , 1.0 ] ] )
    wire1_pnt = np.dot(wire1_pnt,rot02)
    wire2_pnt = np.dot(wire2_pnt,rot02)

    # rotatie om de (nieuwe) x-as zodat wire2_pnt in het xy-vlak komt te liggen
    phix = np.arctan2(wire2_pnt[2],wire2_pnt[1])
    rot03 = np.array( [ [ 1.0, 0.0         , 0.0         , 0.0 ],
                        [ 0.0, np.cos(phix),-np.sin(phix), 0.0 ],
                        [ 0.0, np.sin(phix), np.cos(phix), 0.0 ],
                        [ 0.0, 0.0         , 0.0         , 1.0 ] ] )
    wire1_pnt = np.dot(wire1_pnt,rot03)
    wire2_pnt = np.dot(wire2_pnt,rot03)

    # nu zit alles in een vlak waarvan we zeggen dat er niks in het
    # z-vlak gebeurt en daarom doen we een 2D_trilateration
    r1,r2 = geom_2D_trilateration(
                wire1_pnt[0:2],inMeasurement[inWireLabel1] + wire1_offset,
                wire2_pnt[0:2],inMeasurement[inWireLabel2] + wire2_offset)

    result_2D = geom_2D_closest_point(r1,r2,install_pnt[0:2])

    # we plakken er twee nullen aan vast
    result_3D = np.hstack((result_2D,np.zeros((len(result_2D),2))))

    # bereken de terug transformeer matrix
    back = np.linalg.inv(np.dot(rot01,np.dot(rot02,rot03)))

    # terug transformeren, en alleen x,y,z terug geven
    return np.dot(result_3D,back)[:,0:3]

def geom_3D_displacements_from_2_wire_transducers_plane(inMeasurement,
                                                        inInstall_Dat,
                                                        inTransduc_Set,
                                                        inWireLabel1,
                                                        inWireLabel2,
                                                        plane_def_vec):
    """
    returns array of 3D displacements with respects to the
    install.dat point based on the length changes of the two
    wire transducers given the measurement and install info.

    Note:
        returned points are in the plane defined by the instal.dat point
        and the two starting points of the wire transducers

    Pietje

    Parameters:
        *inMeasurement*:
            nrfs_data object with the measurement

        *inInstall_Dat*:
            nrfs_data object with the install.dat measurement

        *inTransduc_Set*:
            key_valuefile object of the transduc.set file

        *inWireLabels*:
            labels of the involved wire transducers

        *plane_def_vec*:
            vector perpendicular to result plane.

    Note:
        returned points are in the plane defined by the instal.dat point and
        the plane direction defined by plane_def_vec.

    """

    install_pnt = np.array([0.0,0.0,0.0])

    # pas op 4 getallen vanwege latere geometrische matrix manipulatie
    wire1_pnt = np.array([inTransduc_Set[inWireLabel1+'_X'],
                          inTransduc_Set[inWireLabel1+'_Y'],
                          inTransduc_Set[inWireLabel1+'_Z'],0.0])
    wire2_pnt = np.array([inTransduc_Set[inWireLabel2+'_X'],
                          inTransduc_Set[inWireLabel2+'_Y'],
                          inTransduc_Set[inWireLabel2+'_Z'],0.0])

    wire1_offset = geom_3D_dist(install_pnt,wire1_pnt[0:3]) - \
                   inInstall_Dat[inWireLabel1][0]
    wire2_offset = geom_3D_dist(install_pnt,wire2_pnt[0:3]) - \
                   inInstall_Dat[inWireLabel2][0]

    # sanity check
    if not plane_def_vec.shape == (3,):
        raise ValueError,'plane_def_vec should have shape (3,)'
    plane_def_vect = np.hstack((plane_def_vec, np.zeros((1,))))

    # rotatie om de y-as zodat plane_def_vect in het yz-vlak komt te liggen
    phiy = np.arctan2(plane_def_vect[0],plane_def_vect[2])
    rot01 = np.array( [ [ np.cos(phiy), 0.0, np.sin(phiy), 0.0 ],
                        [ 0.0         , 1.0, 0.0         , 0.0 ],
                        [-np.sin(phiy), 0.0, np.cos(phiy), 0.0 ],
                        [ 0.0         , 0.0, 0.0         , 1.0 ] ] )
    wire1_pnt      = np.dot(wire1_pnt     , rot01)
    wire2_pnt      = np.dot(wire2_pnt     , rot01)
    plane_def_vect = np.dot(plane_def_vect, rot01)

    # rotatie om de (nieuwe) x-as zodat plane_def_vect op de z-as komt te liggen
    phix = -np.arctan2(plane_def_vect[1],plane_def_vect[2])
    rot02 = np.array( [ [ 1.0, 0.0         , 0.0         , 0.0 ],
                        [ 0.0, np.cos(phix),-np.sin(phix), 0.0 ],
                        [ 0.0, np.sin(phix), np.cos(phix), 0.0 ],
                        [ 0.0, 0.0         , 0.0         , 1.0 ] ] )
    wire1_pnt      = np.dot(wire1_pnt     , rot02)
    wire2_pnt      = np.dot(wire2_pnt     , rot02)
    plane_def_vect = np.dot(plane_def_vect, rot02)

    # echte lengtes
    length_wire1 = inMeasurement[inWireLabel1] + wire1_offset
    length_wire2 = inMeasurement[inWireLabel2] + wire2_offset
    # geprojecteerde lengtes
    projected_length_wire1 = np.sqrt(length_wire1**2 - wire1_pnt[2]**2)
    projected_length_wire2 = np.sqrt(length_wire2**2 - wire2_pnt[2]**2)

    # nu zit alles in een vlak waarvan we zeggen dat er niks in het
    # z-vlak gebeurt en daarom doen we een 2D_trilateration
    r1,r2 = geom_2D_trilateration(
                wire1_pnt[0:2],projected_length_wire1,
                wire2_pnt[0:2],projected_length_wire2)

    result_2D = geom_2D_closest_point(r1,r2,install_pnt[0:2])

    # we plakken er twee nullen aan vast
    result_3D = np.hstack((result_2D,np.zeros((len(result_2D),2))))

    # bereken de terug transformeer matrix
    back = np.linalg.inv(np.dot(rot01,rot02))

    # terug transformeren, en alleen x,y,z terug geven
    return np.dot(result_3D,back)[:,0:3]


# ==== nrfslib bolt calculations  ====================================
# ===================================================================

def boltcalc1(s1, s2, s3, dia):
    """
    Calculations for a three straingauge measuring bolt.

    Parameters:

        *s1*, *s2*, *s3*:
            measured forces [kN] (1D np.ndarray)
        *dia*:
            bolt diameter [mm]

    Output:

        2D np.ndarray 'boltdat' with:

            - normal force [kN]
            - normal stress [kN/mm^2]
            - bending stress [kN/mm^2]
            - bending angle [radians]

    """

    rad = dia / 2.0                                            # [mm^2]
    avg_for = (s1 + s2 + s3) / 3                               # [kN]
    avg_str = avg_for / (np.pi * rad**2)                       # [kN/mm^2]
    bfact = (2 * s1 - s2 - s3) / (3 * np.pi * rad**3)          # [kN/mm^3]
    cfact = (s3 - s2) / (np.sqrt(3) * np.pi * rad**3)          # [kN/mm^3]
    ang = np.arctan2(cfact, bfact)                             # [radians]
    bend_str = rad * (bfact * np.cos(ang) +
                      cfact * np.sin(ang)   )                  # [kN/mm^2]

    # en geef de resultaten terug
    return np.array([avg_for, avg_str, bend_str, ang])

def boltcalc2(s1, s2, s3, momx, momy, dia, ori, loca,
              n_bolt, bc_dia, blade_ang):
    """
    Boltcalc calculates normal force, normal stress, bending stress,
    angle of bending vector, theoretical stress and bolt factor
    for a measuring bolts with three strain gauges.

    Parameters:

        *s1*, *s2*, *s3*:
            Three strain signals, calibrated in force [kN] (1D np.ndarray)
        *momx*, *momy*:
            Blade moments in lab x and y direction [kNmm] (1D np.ndarray)
        *dia*:
            Bolt diameter [mm]
        *ori*
            Bolt orientation angle [degrees]
        *loca*:
            Bolt loacation angle [degrees]
        *n_bolt*
            Number of bolts [-]
        *bc_dia*
            Diameter of bolt circle [mm]
        *blade_ang*:
            Blade mounting angle (pitch angle) [degrees]

    Output:

        2D np.ndarray 'boltdat' with:

            - average force [kN]
            - averages stress [N/mm^2]
            - bending stress [N/mm^2]
            - angle of bending moment [degrees]
            - theoretical stress [N/mm^2]
            - boltfactor (average stress/ theoretical stress) [-]

    """

    rad = dia / 2.0
    a_bolt = np.pi * dia**2 / 4                               # [mm^2]
    avg_for = (s1 + s2 + s3) / 3                              # [kN]
    avg_str = 1000 * avg_for / a_bolt                         # [N/mm^2]
    bfact = 1000 * (2 * s1 - s2 - s3)/(3 * np.pi * rad**3)    # [N/mm^3]
    cfact = 1000 * (s3 - s2) /(np.sqrt(3) * np.pi * rad**3)   # [N/mm^3]
    angloc = np.arctan2(cfact, bfact)                         # [radians]
    ang = angloc + np.radians(ori)                            # [radians]
    ang = ang % (2*np.pi)                                     # [degrees]
    bend_str = rad * (bfact * np.cos(angloc) +
                      cfact * np.sin(angloc)   )              # [N/mm^2]
    i_bolt = n_bolt * bc_dia**2 * a_bolt / 8                  # [mm^4]
    theor_stress = (1000 * bc_dia / 2 *
                    ( -momy * np.cos(np.radians(loca)) +
                       momx * np.sin(np.radians(loca))   ) / i_bolt) # [N/mm^2]
    boltfac = (avg_str - avg_str[0]) / theor_stress           # [-]
    boltfac[0] = 0   # sjoemelen, maar om toch...

    # en geef de resultaten terug
    return np.array([avg_for, avg_str, bend_str, ang, theor_stress, boltfac])


# ==== nrfslib keyword-value file  ===================================
# ===================================================================

class key_value_file(object):
    """
    reads keyvalue files like config.set, system.set and transduc.set
    """
    def __init__(self,inFile=None,inOptions=''):
        if inFile!=None:
            self.read_transduc_set(inFile,inOptions)
        return

    def read_key_value(self,inFile,inOptions=''):
        """
        deze functie zet de gelezen waardes in de global namespace
        """

        # options
        bVerbose = 'v' in inOptions

        f = open(inFile,'rb')
        for line in f:

            if (line[0]!='#') and True:   # later nog wat meer

                parts = line.split()
                if len(parts)>= 2 :
                    keyword = parts[0]
                    value = parts[1]
                    if isFloat(value):
                        self.__dict__[keyword] = float(value)
                    else:
                        self.__dict__[keyword] = value

                    if bVerbose: print keyword," = ",value

        f.close()


    def read_transduc_set(self,inFile,inOptions=''):
        """
        deze functie zet de gelezen waardes in de global namespace
        """

        # options
        bVerbose = 'v' in inOptions

        # first read the keywords/values
        self.read_key_value(inFile,inOptions)


        f = open(inFile,'rb')
        for line in f:

            if (line[0]!='#') and True:   # later nog wat meer

                parts = line.split()
                if (len(parts)==7) and (parts[0]=='transducer'):
                    label  = parts[1]
                    radius = parts[2]
                    X      = parts[3]
                    Y      = parts[4]
                    Z      = parts[5]
                    group  = parts[6]

                    if isFloat(radius) and \
                       isFloat(X)      and \
                       isFloat(Y)      and \
                       isFloat(Z)      and \
                       isFloat(group)  :

                        self.__dict__[label+'_X'] = float(X)
                        self.__dict__[label+'_Y'] = float(Y)
                        self.__dict__[label+'_Z'] = float(Z)
                        self.__dict__[label+'_group'] = float(group)
                        self.__dict__[label+'_radius'] = float(radius)

                        if bVerbose:  print label,float(radius),'(',float(X),float(Y),float(Z),')',float(group)

                    else :
                        print "error in line: '",line,"'"

        f.close()

    def info(self):
        """
        This functions displays the contents of the object
        """
        print '== key_value_file =='
        for i in self.__dict__.iteritems():
            print "%-20s"%i[0],i[1]

    # functions to make key_value_file act as a dictionary
    def __getitem__(self,label):
        '''
        for emulating container type
        '''
        return self.__dict__[label]

    def __setitem__(self,label, value):
        '''
        for emulating container type
        '''
        self.__dict__[label] = value

    def __iter__(self):
        '''
        for emulating container type, define iterator
        '''
        return self.__dict__.__iter__

    def iteritems(self):
        '''
        for emulating container type, define iterator
        m.iteritems() -> an iterator over the (label, data) items of m
        '''
        return self.__dict__.iteritems

    def keys(self):
        '''
        for emulating container type
        '''
        return self.__dict__.keys()

    def values(self):
        '''
        for emulating container type
        '''
        return self.__dict__.values()


# ==== nrfslib deprecated functions  =================================
# ===================================================================

def geom_2D_triangulation(lp1,l1,lp2,l2):
    """
    deprecated function, use geom_2D_trilateration instead
    """
    raise ValueError, 'deprecated function, use geom_2D_trilateration instead'

def geom_3D_triangulation(p1,ld1,p2,ld2,p3,ld3):
    """
    deprecated function, use geom_3D_trilateration instead
    """
    raise ValueError, 'deprecated function, use geom_3D_trilateration instead'

def error_message(inFunction,inMessage):
    """
    deprecated function
    """
    raise ValueError, '\n\nnrfslib Error in "'+inFunction+'" :\n\n  '+inMessage+'\n'

def warn(inFunction,inMessage):
    """
    deprecated function
    """
    raise ValueError, '\n\nnrfslib Warning in "'+inFunction+'" :\n\n  '+inMessage+'\n'

def load_buffer(inFile,inOptions='',**kwargs):
    """
    deprecated function
    """
    raise ValueError, "deprecated load_buffer function, use load_nrfss"

def load_rngavg(inFile,inOptions='',**kwargs):
    """
    deprecated function
    """
    raise ValueError, "deprecated load_rngavg function, use load_nrfss"


# ==== nrfslib experimental functions=================================
# ===================================================================


def glps(axis = None):
    """
    Experimental function to place text labels near the plots
    instead of using a legend.
    """

    if axis == None:
        axis = plt.gca()

    square_size = 32
    Nlines = len(axis.lines)

    # the 'point of presence' matrix
    POP = np.zeros((Nlines,square_size,square_size),dtype=np.int32)

    # the 'best place potential' matrices
    BPP1 = np.zeros((Nlines,square_size,square_size))
    BPP2 = np.zeros((Nlines,square_size,square_size))

    # the match and miss_match matrix
    match      = np.zeros((2*square_size-1,2*square_size-1))
    miss_match = np.zeros((2*square_size-1,2*square_size-1))
    for i in range(0,square_size):
        for j in range(0,square_size):
            dist = (square_size-1-i)+(square_size-1-j)
            val = 0
            if (dist<(square_size/3)):
                val = - (square_size/3) + dist
            miss_match[                i,                j] = val
            miss_match[                i,2*square_size-2-j] = val
            miss_match[2*square_size-2-i,                j] = val
            miss_match[2*square_size-2-i,2*square_size-2-j] = val
            val = 0
            if dist == 0 or dist == 1:
                val = - (square_size/3)
            if dist == 2 or dist == 3:
                val = (square_size/3)
            match[                i,                j] = val
            match[                i,2*square_size-2-j] = val
            match[2*square_size-2-i,                j] = val
            match[2*square_size-2-i,2*square_size-2-j] = val

    #plt.figure()
    #CS = plt.contourf(miss_match)
    #plt.colorbar()
    #plt.title('miss_match')
    #plt.figure()
    #CS = plt.contourf(match)
    #plt.colorbar()
    #plt.title('match')

    # transformation objects
    trData = axis.transData                # user -> pixel
    trAxesInv = axis.transAxes.inverted()  # pixel -> axes

    # storage for texts sizes
    theTextSizes = []

    for line_no in range(0,Nlines):
        line = axis.lines[line_no]
        xydata =  line.get_xydata()
        xy = trAxesInv.transform(trData.transform(xydata))
        xy_pop = np.array(xy*square_size,dtype=np.int32)

        for x_pop_pnt,y_pop_pnt in xy_pop:
            if ( x_pop_pnt >= 0           and
                 x_pop_pnt <  square_size and
                 y_pop_pnt >= 0           and
                 y_pop_pnt <  square_size     ) :
                # mark the presences at this location
                POP[line_no,x_pop_pnt,y_pop_pnt] = 1

        #plt.figure()
        #plt.contour(POP[line_no])
        #plt.title(line.get_label())

    for l1 in range(0,Nlines):
        for l2 in range(0,Nlines):
            for xpop in range(0,square_size):
                for ypop in range(0,square_size):
                    if POP[l2,xpop,ypop] == 1:
                        if (l1==l2):
                            BPP1[l1] += \
                            match[square_size-1-xpop:2*square_size-1-xpop,
                                  square_size-1-ypop:2*square_size-1-ypop] * \
                                  Nlines
                            pass
                        else:
                            BPP1[l1] += \
                            miss_match[square_size-1-xpop:2*square_size-1-xpop,
                                       square_size-1-ypop:2*square_size-1-ypop]
        #plt.figure()
        #CS = plt.contourf(BPP1[l1])
        #plt.colorbar()
        #plt.title(axis.lines[l1].get_label())

        theText = axis.text(0,0,axis.lines[l1].get_label(),
                            horizontalalignment='left',
                            verticalalignment='bottom',
                            transform = axis.transAxes)
        renderer = axis.figure._cachedRenderer
        text_size = theText.get_window_extent(renderer = renderer)# pixels
        text_size = trAxesInv.transform(text_size)[1] - \
                    trAxesInv.transform(text_size)[0]                  # axes
        text_size = np.array(text_size*square_size+1,dtype=np.int32)   # pop
        theTextSizes.append(text_size)
        del(axis.texts[-1])

    for l1 in range(0,Nlines):
        renderer = axis.figure._cachedRenderer
        text_size = theTextSizes[l1]

        for xpop in range(0,square_size):
            for ypop in range(0,square_size):
                if (xpop>=square_size-text_size[0] or
                    ypop>=square_size-text_size[1]     )  :
                    # disable the unpossible positions
                    # (those that will write outside the axis)
                    BPP2[l1,xpop,ypop] = np.nan
                else :
                    # create a mask with for the label size/position
                    m = np.zeros((square_size,square_size),dtype=np.int32)
                    m[xpop:xpop+text_size[0],ypop:ypop+text_size[1]] = \
                        np.ones(text_size)
                    BPP2[l1,xpop,ypop] += np.sum(BPP1[l1] * m)

        plt.figure()
        CS = plt.contourf(BPP2[l1])
        plt.colorbar()
        plt.title(axis.lines[l1].get_label())

        xmax = float(np.argmax(BPP2[l1]) / square_size) / square_size
        ymax = float(np.argmax(BPP2[l1]) % square_size) / square_size
        theText = axis.text(xmax,ymax,axis.lines[l1].get_label(),
                            horizontalalignment='left',
                            verticalalignment='bottom',
                            transform = axis.transAxes)

class DraggableAxes:
    """
    Make an Axes instance draggable and resizeable
    """
    def __init__(self, ax = None, connect = True):
        """
        Make axes draggable
        Parameters:
        ax      : the axes to make draggable. If None, the current axes is used
        connect : connect mouse events on initialisation, default is True.

        DraggableAxes can be connected and disconnected using the .connect() and
        .disconnect() methods.
        """
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        self.press = None
        if connect:
            self.connect()

    def connect(self):
        """
        connect to all the events we need
        """
        self.cidpress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        """
        check if mouse is over axes and store data
        """
        if event.inaxes != self.ax: return
        x0, y0, x1, y1 = self.ax.get_position().get_points().ravel()
        self.press = x0, x1, y0, y1, event.x, event.y

    def on_motion(self, event):
        """
        move the axes and redraw
        """
        #first check if the button was pressed over the axes
        if self.press is None: return
        x0, x1, y0, y1, xpress, ypress = self.press

        #because event locations are in pixels, get the figure size in pixels
        figxsize,figysize = self.ax.figure.get_size_inches() * \
                            self.ax.figure.get_dpi()
        #normalize event data and calculate movement
        dx = ( event.x - xpress ) / figxsize
        dy = ( event.y - ypress ) / figysize

        #if the click was in the outer 5 pixels of the axes, resize, otherwise
        #move. First check for moving the axes (click > 5 pixels from edge)
        if (x0 * figxsize + 5) < xpress < (x1 * figxsize - 5) and \
         (y0 * figysize + 5) < ypress < (y1 * figysize - 5):
            #shift the 4 corners of the axes with mouse movement
            x0, y0, x1, y1 = x0 + dx, y0 + dy, x1 + dx, y1 + dy
        else:
            #resize axes, move the corners on the edge of the click
            if xpress < (x0 * figxsize + 5):
                #check for minimum size of axes
                if (x1 - x0 - dx) < 0.05:
                    dx = x1 - x0 - 0.05
                x0 += dx
            elif xpress > (x1 * figxsize - 5):
                if (x1 - x0 + dx) < 0.05:
                    dx = 0.05 - (x1 - x0)
                x1 += dx
            if ypress < (y0 * figysize + 5):
                if (y1 - y0 - dy) < 0.05:
                    dy = y1 - y0 - 0.05
                y0 += dy
            elif ypress > (y1 * figysize - 5):
                if (y1 - y0 + dy) < 0.05:
                    dy = 0.05 - (y1 - y0)
                y1 += dy
        #set position uses (x,y, width, heigth)
        self.ax.set_position([x0, y0, x1 - x0, y1 - y0])
        self.ax.figure.canvas.draw()

    def on_release(self, event):
        """
        reset press data
        """
        self.press = None
        self.ax.figure.canvas.draw()

    def disconnect(self):
        """
        disconnect all the stored connection ids
        """
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)
        self.ax.figure.canvas.mpl_disconnect(self.cidrelease)
        self.ax.figure.canvas.mpl_disconnect(self.cidmotion)

def table(data,adjust_h = True, padding = 0.5, spacing = 0.5,  **kwargs):
    '''
    creates at table with data in the current axes. If no axes is present
    a new axes is created.

    Parameters:

        *data* - a list with table data containing a list of cell data for each
                 row, e.g. [['Channel', 'Max', 'Min'],['F01', 32.3,-0.1],['S01',22.43,21.23]]

                 Numbers are formatted as % .5g (5 digits). For other formats use
                 string formatting (e.g. '% .4f' %3.1)

                 The number of columns is based on the longest row

                 If the first item of a row list is the string 'hline', a horizontal line is
                 added in the table. The second item can be a dictionary to format the line.

        *adjust_h* - boolean, adjust the height of the axes to fit the data, default is True
        *padding* - padding to the border of the axes as a fraction of the font format
        *spacing* - spacing between lines as a fraction of font format
        *kwargs* - other keyword arguments are passed to all text instances

    Returns  :

        None
    '''
    #padding and spacing shall be floats
    padding = float(padding)
    spacing = float(spacing)
    #check if fontsize is specified directly of in a font dictionary, otherwise use rcParams
    fontdict = kwargs.get('fontdict', {})
    fontsize = kwargs.get('fontsize', fontdict.get('size', plt.rcParams['font.size']) )
    #get the dimensions of the current axes, gca() creates one if there is none
    fig = plt.gcf()
    figwidth, figheight = fig.get_size_inches()
    ax = plt.gca()
    axbox = ax.get_position().get_points()
    axw = axbox[1][0]-axbox[0][0]     # width as a fraction of figure
    axh = axbox[1][1]-axbox[0][1]     # height (fraction
    axheight = axh * figheight        # heigth in inches
    axwidth = axw * figwidth          # widht in inches

    #calculate the height needed for the table data
    if adjust_h:
        numrows = padding             #padding and spacing are also counted as rows
        for line in data:
            if line[0] == 'hline':
                numrows += spacing    #line has spacing above and below
            else:
                numrows += 1 + spacing
        numrows = numrows - spacing + padding  #subtract spacing for last line and add padding
        #calculate new height for axes and adjust
        axheight = numrows * float(fontsize)/72 #* 1.5
        axh = axheight / figheight
        ax.set_position([axbox[0][0],axbox[1][1] - axh , axw, axh])
    #rowheight as a fraction of the axes
    rowheight = float(fontsize)/72 / axheight

    #remove the ticklabels for the axes
    plt.xticks([])
    plt.yticks([])
    #start position for the first cell
    ypos = 1 - rowheight * (padding + 1)
    xpos = rowheight * padding * axheight / axwidth

    #find the number of columns
    numcols = max([len(line) for line in data])
    colwidth = (1 - rowheight * padding * axheight / axwidth) / numcols
    #write the table
    for line in data:
        if line[0] == 'hline':
            try:
                linekwargs = line[1]
                if not 'color' in linekwargs: linekwargs['color'] = 'black'
            except IndexError:
                linekwargs = {'color':'black'}
            ax.axhline(ypos + rowheight , xpos,1 - xpos, **linekwargs)
            ypos -= spacing * rowheight
        else:
            for item in line:
                if isinstance(item, (str,unicode)):
                    ax.text(xpos, ypos, item,va = 'baseline', ha = 'left', transform = ax.transAxes, **kwargs)
                    xpos += colwidth
                else:
                    ax.text(xpos, ypos, '% .5g' % item ,va = 'baseline', ha = 'left', transform = ax.transAxes, **kwargs)
                    xpos += colwidth
            ypos -= rowheight * (1 + spacing)
        xpos = rowheight * padding * axheight / axwidth
