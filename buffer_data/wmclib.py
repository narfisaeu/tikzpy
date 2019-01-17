# ==== WMClib =======================================================
#
# ===================================================================
#
# (c) copyright 2018, Knowledge Centre WMC
#
# ===================================================================
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# =================================================================== 
#
# ==== Changes ======================================================
#
# ChangeLog is on the Wiki.
#
# ==== WMClib imports ===============================================
# ===================================================================

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import scipy.signal

import scipy.optimize
import struct
from copy import copy, deepcopy
import glob
import string
# import math
import os
import time as time
import datetime
import os.path
import re
import sys
import pickle
import subprocess
import wmclibdata
import io

# from scipy.optimize import leastsq

# ==== WMClib Greeting & initial stuff ====
# =========================================

version='20190104.11317'

print('WMClib %s'%version)
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
# python 2.7 defaults (I assume)
plt.rcParams['lines.linewidth'] = 1.0
if 'lines.dashed_pattern' in plt.rcParams:
    plt.rcParams['lines.dashed_pattern'] = [6, 6]
if 'lines.dashdot_pattern' in plt.rcParams:
    plt.rcParams['lines.dashdot_pattern'] = [3, 5, 1, 5]
if 'lines.dotted_pattern' in plt.rcParams:
    plt.rcParams['lines.dotted_pattern'] = [1, 3]
if 'lines.scale_dashes' in plt.rcParams:
    plt.rcParams['lines.scale_dashes'] = False
# change the default color cycle for the plot
# the matplotlib defualt cycles 8 colors
# this is changed to the 16 colors also used in grafx
# (standard web-color names are valid for matplotlib)
#from matplotlib.axes import set_default_color_cycle
wmc_default_colors = ['red',
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

view_from_top = 1
view_from_side = 2
view_from_tip = 3

allviews = [view_from_top, view_from_side, view_from_tip]

# Changing the default color cycle is a bit difficult with different
# version of Matplotlib, anyway we try two methods and print(and error
# message if we do not succeed

colors_oke = False
if 'axes.prop_cycle' in plt.rcParams:
    # python 3 (Anaconda
    try:
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=wmc_default_colors)
        colors_oke = True
    except:
        pass
        
if not colors_oke:   
    try:
        plt.rcParams['axes.color_cycle'] = wmc_default_colors
        colors_oke = True
    except:
        pass

if not colors_oke:       
    try:
        set_default_color_cycle(wmc_default_colors)
        colors_oke = True
    except:
        pass

if not colors_oke:       
    try:
        matplotlib.axes.set_default_color_cycle(wmc_default_colors)
        colors_oke = True
        print('color_cycle set using statement:')
        print("matplotlib.axes.set_default_color_cycle(wmc_default_colors)")
    except:
        pass

if not colors_oke :
    print('')
    print('WARNING: something went wrong with the colors.')
    print('         please update Python(X,Y), matplotlib etc...')
    print('')
    wmc_default_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

print('')

# default markers cycle, used in add_marker
wmc_default_markers = ['s','^','o','v','x','D','*','+','H',
                       '<','>','d','p','1','2','3','4','h']

class repaired_channel:
    '''
    :purpose: overruling channel settings
    '''
    def __init__(self, idcolumn='label', label='', calfac=1.0, offset=0.0
        , despike_maxdeviation=-1.0
        , smooth_window='', smooth_window_len=11):
        self.idcolumn = idcolumn
        ''' column in the definition with the id '''
        self.label = label
        ''' label of the channel '''
        self.calfac = calfac
        ''' calibration factor '''
        self.offset = offset
        ''' offset '''
        self.despike_maxdeviation = despike_maxdeviation
        ''' maximum deviation for despike '''
        self.smooth_window = smooth_window
        ''' smooth window, default value: no smoothing '''
        self.smooth_window_len = smooth_window_len
        ''' smooth window length'''
        
    def load(self, columns, values):
        self.idcolumn = columns[0]
        for icol, col in enumerate(columns):
            if col in ['label', 'smooth_window']:
                self.__dict__[col] = values[icol]
            elif col in ['channel', 'smooth_window_len']:
                self.__dict__[col] = int(values[icol])
            else:
                self.__dict__[col] = eval(values[icol])
        return True
        
    def change_values(self, meas):
        '''
        :purpose: change values for the current channel
            in a wmc_data object
        '''
        # first find the fields for this channel
        fields = []
        for ifld in meas.fields:
            fld = meas.fields[ifld]
            if fld.channelname == self.label:
                fields.append(fld)
        for fld in fields:
            label = fld.name
            if np.abs(self.calfac - 1.0) > 1e-5:
                print('change values in field "%s" by factor %g'%(label, 
                    self.calfac))
                meas[label] *= self.calfac
            
            if fld.fieldtype != fld.fieldtype_range:
                if not(np.abs(self.offset) == 0.0):
                    if self.offset > 0:
                        print('adding %g to values in field "%s"'%(self.offset,
                            label))
                    else:
                        print('subtracting %g from values in field "%s"'%(
                            np.abs(self.offset), label))
                    meas[label] -= self.offset
            
            if fld.is_channel_signal():
                if self.despike_maxdeviation > 0.0:
                    print('despiking field "%s" if deviation > %g'%(label
                        , self.despike_maxdeviation))
                    meas[label] = despike(meas[label]
                        , self.despike_maxdeviation)
                    
                if len(self.smooth_window.strip()) > 0:
                    print(
                        'smoothing field "%s" according to window "%s" with length %d'%(
                            label, self.smooth_window, self.smooth_window_len))
                    meas[label] = smooth(meas[label]
                        , window=self.smooth_window
                        , window_len=self.smooth_window_len)
    
    def label_changed(self):
        return len(self.label) > 0
        
    def calfac_changed(self):
        return np.abs(self.calfac - 1.0) > 1e-5
    
    def offset_changed(self):
        return np.abs(self.offset) > 0.0
        
    def must_despike(self):
        return self.despike_maxdeviation > 0.0
        
    def must_smooth(self):
        return len(self.smooth_window) > 0
        
    def __str__(self):
        if self.idcolumn == 'channel':
            s = '%7d %10s'%(self.channel, self.label)
        else:
            s = '%10s'%self.label
        
        return s
        

class repaired_channels:
    '''
    :purpose: file with definition for overruling channel settings
    '''
    
    def __init__(self, filename='channels.repair', separator='\t'):
        self.possibleidcolumns = ['channel', 'label']
        self.possibledatacolumns = ['label'
            , 'calfac', 'offset'
            , 'smooth_window', 'smooth_window_len', 'despike_maxdeviation']
        self.filename = filename
        self.folder = '.'
        self.separator = separator
        self.columns = []
        self.channels = {}
        self.label_changed = False
        self.offset_changed = False
        self.must_smooth = False
        self.must_despike = False
        self.calfac_changed = False
    
    def load(self, folder='.'):
        '''
        :purpose: load definition for overruling channel settings
        '''
        self.folder = folder
        flpth = os.path.join(self.folder, self.filename)
        self.columns = []
        self.channels = {}
        if os.path.exists(flpth):
            with open(flpth, 'r') as f:
                line = f.readline()
                while (len(line) > 0) and (
                    line.startswith('##') or (len(line.strip()) == 0)):
                    line = f.readline()
                if len(line) == 0:
                    print('no valid lines found')
                    return
                cols = line.strip().split(self.separator)
                for col in cols:
                    if not ((col in self.possibledatacolumns)
                        or (col in self.possibleidcolumns)):
                            raise(ValueError('column "%s" not valid'%(col)))
                if len(cols) == 0:
                    raise(ValueError('no columns in file "%s"'%(flpth)))
                self.columns = cols
                line = f.readline() # 1st line
                while len(line) > 0:
                    a = line.strip().split(self.separator)
                    if len(a) >= len(self.columns):
                        chnl = repaired_channel()
                        if chnl.load(self.columns, a):
                            self.channels[chnl.__dict__[cols[0]]] = chnl
                    line = f.readline()
                f.close()
        self._set_changed_columns()
                
    def change_values(self, meas):
        '''
        :purpose: change values in a wmc_data object
        '''
        keys = sorted(self.channels.keys())
        for key in keys:
            chnl = self.channels[key]
            chnl.change_values(meas)
    
    def labels_changed(self, meas_channels, verbose=False):
        '''
        :purpose: give a list of channel numbers that are changed
        '''
        ret = []
        if len(self.columns) < 2:
            if verbose:
                print('No columns changed: not enough columns')
            return ret
        # the id column should be the channel number
        if not (self.columns[0] == 'channel'):
            return ret
        # label should be one of the columns
        if not ('label' in self.columns):
            return ret
        keys = sorted(self.channels.keys())
        for key in keys:
            # channel definition in meas object
            measchannel = meas_channels.channels[key]
            # new definition
            chnl = self.channels[key]
            oldname = measchannel['label']
            newname = chnl.label
            if ((len(newname) > 0) and not (oldname == newname)):
                # label has actually changed
                ret.append(key)
        return ret
        
    def change_labels(self, meas, verbose=False):
        '''
        :purpose: Change the labels of channels and fields in wmc_data object
        
        :details: Assume the channel name is the last part of the field name
            E.g. field A_S01 for average
        
        :param meas: wmc_data object with data fields and channel definition
        '''
        channels_label_changed = self.labels_changed(
            meas.channels, verbose=verbose)
        # loop through keys if there is a label change
        if verbose and (len(channels_label_changed) > 0):
            print('Replacing channel names:')
            print('========================')
        for id in channels_label_changed:
            # channel definition in meas object
            measchannel = meas.channels.channels[id]
            # new definition
            chnl = self.channels[id]
            oldname = measchannel['label']
            newname = chnl.label
            if verbose:
                print('%s -> %s'%(oldname, chnl.label))
            # now change the name of the channel, and the datafields for that
            for ifld in meas.fields:
                fld =  meas.fields[ifld]
                fld.skip = False
                if fld.channelnumber == id:
                    # this is a field for the current channel, 
                    # so change the name
                    fld.channelname = newname
                    if fld.is_channel_signal():
                        fld.name = newname
                    else:
                        oldfldname = fld.name
                        # strip the original label
                        # assume the channel name is the latter part
                        fld.name = fld.name[:-len(oldname)]
                        fld.name += newname
                        if verbose:
                            print('Changed field: "%s" -> "%s"'%(
                                oldname, fld.name))
            measchannel['label'] = chnl.label

    def _set_changed_columns(self):
        '''
        :purpose: return dictionary of changes, where 
        '''
        self.label_changed = False
        self.offset_changed = False
        self.must_smooth = False
        self.must_despike = False
        self.calfac_changed = False
        for key in self.channels.keys():
            chnl = self.channels[key]
            # possibly change label
            if chnl.label_changed():
                self.label_changed = True
            if chnl.offset_changed():
                self.offset_changed = True
            if chnl.must_smooth():
                self.must_smooth = True
            if chnl.must_despike():
                self.must_despike = True
            if chnl.calfac_changed():
                self.calfac_changed = True
        
    def __str__(self):
        keys = sorted(self.channels.keys())
        if len(keys) == 0:
            return 'no repaired channels'
        s = 'repaired channels'
        s += '\n================='
        s += '\nid column: %s'%(self.columns[0])
        for key in keys:
            chnl = self.channels[key]
            s += '\n'
            if self.columns[0] == 'channel':
                if len(chnl.label) > 0:
                    s += 'channel %3d is named "%s"'%(key, chnl.label)
            else:
                s += key
            if chnl.calfac_changed():
                s += ' calibration factor: %g'%chnl.calfac
            if chnl.offset_changed():
                s += ' offset: %g'%chnl.offset
            if chnl.must_despike():
                s += ' despike if deviation > %g'%chnl.despike_maxdeviation
            if chnl.must_smooth():
                s += ' smoothed using window "%s" length %d'%(
                    chnl.smooth_window, chnl.smooth_window_len)
        return s
    
    
    
# see also: http://www.python.org/dev/peps/pep-0234/ 'some folks...'
class bidirectional_cyclic_iterator(object):
    def __init__(self, collection):
        self.collection = copy(collection)
        self.length = len(collection)
        self.index = None

    def next(self):
        if self.index is None:
            self.index = 0
        else: 
            self.index = (self.index + 1) % self.length
        return self.collection[self.index]

    def prev(self):
        if self.index is None:
            self.index = self.length - 1
        else: 
            self.index = (self.index - 1) % self.length
        return self.collection[self.index]
        
    def current(self):
        if self.index is None:
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

colors = bidirectional_cyclic_iterator(wmc_default_colors)
markers = bidirectional_cyclic_iterator(wmc_default_markers)


# ==== WMClib Data Class ============================================
# ===================================================================

class wmc_data(object):
    """
    The wmc_data object is an object where the measurement signals of
    WMCS (.buffer, .txt, .xls) are stored.
    
    The preferred way to access the data is using label indices as shown here::

        meas = wmc.load_wmcs('./path/to/file.buffer')
        plt.plot(meas['F01'], meas['001S120'])

    A wmc_data object is loaded with measurement data by use of one of the
    load_xxx functions
    
    """
    
    def __init__(self, inNpnt=0, file_name='', file_type=''):
        """
        initialize the wmc_data object
        """
        self.allocate(inNpnt)
        self.Nchn = 0
        ''' Number of channels '''
        self.file_name = file_name
        ''' original file name '''
        self.file_path = ''
        ''' path to original file name '''
        self.file_type = file_type
        ''' type of original file '''
        self.file_date = ''
        ''' date as string as recorded in the data file '''
        self.file_time = ''
        ''' time as string as recorded in the data file '''
        self.NpntInSource = -1
        ''' Number of data points in data source '''
        self.channels = wmcs_channels()
        ''' channel definition of data file '''
        dummyfld = wmc_data_field(name='dummy', number=0)
        self.fields4channeldef = [
            dummyfld.fieldtype_range, dummyfld.fieldtype_channel_signal]
        ''' fields, which are used to determine channel definition '''
        self.timecolumn = ''
        ''' name column with time signal '''
        self.prefixrange = 'R_'
        ''' prefix for a range field, default "R\_" '''
        self.prefixaverage = 'A_'
        ''' prefix for a average field, default "A\_" '''
        self.fields = {}
        ''' 
            dictionary with wmc_data_field objects 
            (key = field number in original file) 
        '''

    def allocate(self, inNpnt):
        """
        allocate (only for internal use)
        """
        self.chn = {}
        ''' dictionary with arrays with measurement data '''
        self.Npnt = inNpnt
        ''' Number of data points '''

    def shrink_to(self,inNpnt):
        """
        resize (only for internal use)
        """
        print('[shrink_to] doet het nog niet')
        pass

    def add_pnt(self,inPntStep):
        """
        add points (only for internal use)
        """
        print('[add_pnt] doet het nog niet')
        pass
    
    def add_data_field(self, fld
        , unit='', calfac=1.0, offset=0.0, verbose=False):
        """
        add field definition original file
        """
        if fld.fieldtype in self.fields4channeldef:
            fld.channelnumber = self.add_channel(name=fld.channelname
                , unit=unit, calfac=calfac, offset=offset)
        self.fields[fld.number] = fld
        if verbose:
            print('Add %s'%(fld.__str__()))
            print('%d channels'%(len(self.channels.channels)))
        
    def add_channel(self, name, id=-1, calfac=1.0, offset=0.0, unit=''):
        '''
        :purpose: add a channel
        '''
        if id == -1:
            id = len(self.channels.channels)
        else:
            if id in self.channels.channels:
                raise ValueError('%s. %s.'%(
                    'Try to add existing channel "%s" with id %d'%(name, id)
                    , 'It exists with name "%s"'%self.channels.channels[id]))
        self.channels.add(id=id, name=name
            , calfac=calfac, offset=offset, unit=unit)
        return id
        
    # functions to make wmc_data act as a dictionary
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
        
        # also delete attribute reference
        attr_label = label
        if str.isdigit(label[0]):
            attr_label = 's' + label
        if attr_label in self.__dict__:
            try:
                self.__delattr__(attr_label)
            except:
                pass
        
    def __setitem__(self, label, value):
        '''
        for emulating container type
        '''
        # sanity check is value an array of correct size.....
        if not type(value) == np.ndarray:
            raise(ValueError('Only 1D numpy array of correct length ' +\
                              'can be added to a wmc_data object'))
        if not value.shape == (self.Npnt,):
            raise(ValueError('Only 1D numpy array of correct length ' +\
                              'can be added to a wmc_data object'))
        # check label is string with length > 0
        if not (isinstance(label, str) and (len(label) > 0)):
            print(label)
            print(type(label))
            raise(ValueError('Invalid label "%s"'%label))

        if (not label in self.chn.keys()):
            self.chn[label] = value
            self.Nchn = len(self.chn)
        else:
            self.chn[label] = value
        
        # if possible make signals available as for instance: meas.F01
        attr_label = label
        if str.isdigit(label[0]):
            attr_label = 's' + label
        
        if attr_label in self.__dict__:
            self.__dict__[attr_label] = self.chn[label]
        else:
            try:
                self.__setattr__(attr_label, self.chn[label])
            except:
                pass
        
        
    
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
        
    def __repr__(self):
        s  = 'WMCLib wmc_data object ('
        if self.file_name:
            s += '%s, ' % self.file_name
        s += '%d channels, ' % (self.Nchn)
        s += '%d points)' % (self.Npnt)
        return s

    def info(self):
        """
        print some information of this wmc_data object
        """
        print('Npnt        : ', self.Npnt)
        print('Nchn        : ', self.Nchn)
        print('file_name   : ', self.file_name)
        print('file_type   : ', self.file_type)
        print('file_date   : ', self.file_date)
        print('file_time   : ', self.file_time)

    def masked_copy(self,inMask):
        """
        Returns a new wmc_data object with masked applied
        
        Arguments:
            *inMask* - np.ndarray of Booleans
        """
        
        # create a new data object
        wd = wmc_data()
        wd.allocate(np.sum(inMask))
        wd.file_name = 'masked copy of %s' % self.file_name
        wd.file_type = self.file_type
        wd.file_date = self.file_date
        wd.file_time = self.file_time
        
        # copy the stuff
        for ch in self:
            wd[ch] = copy(self[ch][inMask])
        
        # return the newly created wmc_data object
        return wd
        
    def copy(self):
        """
        Returns a copy of the wmc_data object.
        """
        return deepcopy(self)
    
    def add_minmax_from_rngavg(self):
        '''
        :purpose: add min and max per cycle from the range and average in 
            the measurement
        '''
        a_error_channels = []
        for id in self.channels.channels:
            chnl = self.channels.channels[id]
            channelname = chnl['label']
            # obtain the range and average fields
            average = None
            range = None
            for ifld in self.fields:
                fld = self.fields[ifld]
                if fld.channelname == channelname:
                    if fld.fieldtype == fld.fieldtype_average:
                        if fld.name in self.keys():
                            average = self[fld.name]
                    elif fld.fieldtype == fld.fieldtype_range:
                        if fld.name in self.keys():
                            range = self[fld.name]
            if (average is not None) and (range is not None):
                amplitude = 0.5 * range
                self['MIN_%s'%channelname] = average - amplitude
                self['MAX_%s'%channelname] = average + amplitude
                if min(np.abs(average + amplitude)) > 0:
                    self['RVAL_%s'%channelname] = (
                        (average - amplitude)/(average + amplitude))
                else:
                    a_error_channels.append(channelname)
                    self['RVAL_%s'%channelname] = np.zeros_like(average)
                    for i, x in enumerate(average):
                        if (x + amplitude[i]) == 0:
                            self['RVAL_%s'%channelname][i] = np.nan
                            
                        else:
                            self['RVAL_%s'%channelname][i] = (
                                (x - amplitude[i])/(x + amplitude[i]))
        ret = ''
        if len(a_error_channels) > 0:
            ret = 'WARNING: the maximum for %d channels contains zeros'%(
                len(a_error_channels))
            ret += '\n  R-value set to NaN for the following channels\n  '
            if len(a_error_channels) < 10:
                ret += ', '.join(a_error_channels)
            else:
                ret += ', '.join(a_error_channels[:10])
                ret += ', ...'
            print(ret)
        return ret
    
    def _channels(self, mapped_channels=None
        , write_unmapped=True, blacklist_channels=None, verbose=False):
        '''
        make a complete list of channels for export to xls or txt
        '''
        ret = []
        keys = sorted(self.keys())
        if mapped_channels is not None:
            for chnl in mapped_channels:
                if chnl.channel in keys:
                    ret.append(chnl)
                else:
                    print('channel "%s" not present, so not exported'%(
                        chnl.channel))
            
        if write_unmapped:
            for i, key in enumerate(keys):
                writechannel=True
                if blacklist_channels is not None:
                    if key in blacklist_channels:
                        writechannel=False
                if writechannel:
                    ret.append(mapped_channel(self, key))
                    
        if verbose:
            print('exported channels')
            for chnl in ret:
                print(chnl)
        
        return ret
            
    def save_xls(self, inName='', wsname='wmc_data', wb=None
        , headinglines=None, mapped_channels=None
        , channelnames=False, units=False, write_unmapped=True, blacklist_channels=None
        , verbose=False):
        """
        save the data of the wmc_data object into an excel workbook
        in a 'pretty' format
        
        :param inName: name of the workbook (file name = inName.xls
            if empty, no file is saved
        :param wsname: name of the work sheet
        :param wb: existing workbook if not None. Work sheet is added
        :param headinglines: e.g. [['samplename']]
            optionally start with custom heading lines
        :param mapped_channels: mapping of column names, possibly with scaling
        :param blacklist_channels: channels, which should not be written
        :param channelnames: if True 1st row contains original channel names
        :param units: if True last heading row contains units
        :param write_unmapped: if True, write unmapped channels
            , apart from channels in the blacklist
        
        """
        chnls = self._channels(mapped_channels=mapped_channels
            , write_unmapped=write_unmapped
            , blacklist_channels=blacklist_channels
            , verbose=verbose)
        # version 0.7.2 or higher required
        from xlwt import Workbook,easyxf
        
        if wb is None:
            wb = Workbook('cp1252')
        try:
            ws = wb.add_sheet(wsname)
        except:
            print('unable to add worksheet "%s"'%wsname)
            return wb
        
        def _val(val):
            if type(val) == np.int64:
                return int(val)
            else:
                return val
                
        xf = easyxf('borders: bottom medium; '+
            'pattern: pattern solid, fore_colour light_yellow;')
        irowoffset = 0
        # write header lines
        if headinglines is not None:
            for irow, hline in enumerate(headinglines):
                for icol, col in enumerate(hline):
                    ws.write(irow, icol, col)
            irowoffset = len(headinglines)
        toomanyrows = False
        for icol, pc in enumerate(chnls):
            # write data per column
            irow = irowoffset
            if channelnames:
                ws.write(irow, icol, pc.channel, xf)
                irow += 1
            ws.write(irow, icol, pc.columnname, xf)
            irow += 1
            if units:
                ws.write(irow, icol, pc.unit, xf)
                irow += 1
            for val in self[pc.channel]:
                if irow < 65536:
                    ws.write(irow, icol, float(_val(val)) * pc.scaling)
                else:
                    toomanyrows = True
                irow += 1
                
        if len(inName) > 0:
            # save work book and reset for next measurement
            wb.save(inName+'.xls')
            wb = None
        if toomanyrows:
            raise(ValueError(
                'writing data is aborted: too many rows for excel (max 65536)'))
            
        return wb
    
    def save_txt(self, inName, inSeperator=''
        , headinglines=None, mapped_channels=None
        , units=False, channelnames=False, write_unmapped=True
        , blacklist_channels=None
        , verbose=False, defaultfloatformat='%15.4e', channelformats=None):

        """
        save the data of the wmc_data object into an .txt file
        
        :param inName: name of the file
        :param headinglines: e.g. [['samplename']]
            optionally start with custom heading lines
        :param mapped_channels: mapping of column names, possibly with scaling
        :param blacklist_channels: channels, which should not be written
        :param units: if True 2nd row contains units
        :param channelnames: if True 1st row contains original channel names
        :param write_unmapped: if True, write unmapped channels
            , apart from channels in the blacklist
        :param defaultfloatformat: default format string for 
            floating number channels
        :param channelformats: dictionary of channels with custom format string
        
        """
        
        chnls = self._channels(mapped_channels=mapped_channels
            , write_unmapped=write_unmapped
            , blacklist_channels=blacklist_channels
            , verbose=verbose)
        # first column record, then other data (and record again..)
        if 'record' in self.keys():
            chnls.insert(0, mapped_channel(self, 'record'))
            if verbose:
                print('insert channel "record" in 1st column')
                
        for chnl in chnls:
            # enrich channel data with format and width
            ch = chnl.channel
            chnl.width = max(16,len(ch)+1)
            if (channelformats is not None) and (ch in channelformats):
                chnl.format = channelformats[ch]
            elif  self[ch].dtype == np.dtype('int32'):
                chnl.format = '%d'
            elif self[ch].dtype == np.dtype('int64'):
                chnl.format = '%d'
            elif self[ch].dtype == np.dtype('float64'):
                chnl.format = defaultfloatformat
            elif self[ch].dtype == np.dtype('bool'):
                chnl.format = '%d'
            else:
                raise(ValueError('Unknown type for column "%s"'%ch))
                    
        # open file
        with open(inName,'w') as f:
            if headinglines is not None:
                for line in headinglines:
                    for i, fld in enumerate(line):
                        f.write(fld.rjust(chnls[i].width))
                        if ((len(inSeperator) == 0) 
                            and (len(fld)>chnls[i].width)):
                            # write extra separator, if fields would be glued
                            f.write(' ')
                        f.write(inSeperator)
                    f.write('\n')

            if channelnames:
                for chnl in chnls:
                    s = '[%s]'%chnl.channel
                    f.write(s.rjust(chnl.width))
                    f.write(inSeperator)
                f.write('\n')

            # write header
            for chnl in chnls:
                s = chnl.columnname
                f.write(s.rjust(chnl.width))
                f.write(inSeperator)
            f.write('\n')
            
            # write units
            if units:
                for chnl in chnls:
                    s = '[%s]'%chnl.unit
                    f.write(s.rjust(chnl.width))
                    f.write(inSeperator)
                f.write('\n')
            
            # write_data
            for i in range(self.Npnt):
                for chnl in chnls:
                    s = chnl.format%(self[chnl.channel][i]*chnl.scaling)
                    f.write(s.rjust(chnl.width))
                    f.write(inSeperator)
                f.write('\n')
            
            # close file
            f.close()
        
    def save_wmcs(self, inName):
        """
        Save data in WMCS format.
        
        For now is saves only the float channels
        """
        
        # some 'constants', block identifiers
        BT_WMCS_IDENTIFIER  =  0
        BT_CHN_COUNT        = 20
        BT_CHANNEL_LABEL    = 100
        BT_DATA_RECORDS     = 200
        
        # we don't want to save and empty file
        if self.Npnt <= 0:
            raise(ValueError('Cannot save an empty wmc_data object'))
            
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
        
        f.write(struct.pack('ii', BT_WMCS_IDENTIFIER, 4))
        f.write('WMCS'.encode('ascii'))
        
        f.write(struct.pack('iii', BT_CHN_COUNT, 4, len(f_chns)))
        
        for i, ch in enumerate(f_chns):
            f.write(struct.pack('iii', BT_CHANNEL_LABEL, len(ch)+4, i))
            f.write(ch.encode('ascii'))
        
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
    
    def load(self, folder='', rep_channels=None
        , firstrecord=-1, step=1, lastrecord=-1, only_header=False
        , verbose=False):
        '''
        load the data in a text file into a wmc_data object
        
        following columns are added
            * record: counter in resulting wmc_data object
            * testtime: time in seconds, starting from the first record
            * lineinfile: counter of lines in original file (starts at 0)
        
        :param filepath: full name of the file
        :param rep_channels: repaired channels
        :param firstrecord: first record which should be read
        :param lastrecord: last line to be read
            if step != 1, there is a chance that this record is not present
        :param step: if not 1, then each nth line is read, 
        
        Loads the data from a text file
        '''
        if verbose:
            t0 = datetime.datetime.now()
        if len(folder) == 0:
            self.file_path = self.file_name
        else:
            self.file_path = os.path.join(folder, self.file_name)
        if not os.path.exists(self.file_path):
            raise ValueError('File "%s" not found'%self.file_path)
        # after this method the following data should be set
        #       file data: type, date
        #       number of records in source file
        #       channel data: column names, calibration factors, offsets, units
        self.load_header(verbose=verbose)
        if verbose:
            t = datetime.datetime.now() - t0
            print('Loading header took %.3f [s]'%t.total_seconds())
        first, last, step = self.set_Npnt(firstrecord, lastrecord, step, verbose)
        if only_header:
            if verbose:
                print('Only loaded header')
            self.finish_load()
            return
        self.allocate(self.Npnt)
        if (not (rep_channels is None)) and (
            len(rep_channels.labels_changed(self.channels)) > 0):
            print(rep_channels)
            rep_channels.change_labels(self, verbose=True)
        
        # initialize default columns
        self['record'] = np.arange(self.Npnt)
        self['recordinsource'] = np.zeros_like(self['record'])
        self['testtime'] = np.zeros(self.Npnt)
        for i in self.fields:
            fld = self.fields[i]
            if not fld.skip:
                self[fld.name] = np.zeros(self.Npnt)
        self.load_data(
            firstrecord=first, step=step, lastrecord=last, verbose=verbose)
            
        if not rep_channels is None:
            rep_channels.change_values(self)
        
        if verbose:
            t = datetime.datetime.now() - t0
            print('Loading took %.3f [s]'%t.total_seconds())
        
        self['record'] = np.arange(self.Npnt)
        if len(self.timecolumn) > 0:
            if self.Npnt > 0:
                self['testtime'] = \
                    self[self.timecolumn] - self[self.timecolumn][0]
                    
        print('%s, Nchn = %d, Npnt = %d' % (
            self.file_path,len(self.fields), self.Npnt))
        
    def stepsize4maxnumber(self, maxnumber):
        if self.Npnt < 2:
            return 1
        if self.Npnt <= maxnumber:
            return 1
        ret = int(np.log2(float(2*(self.Npnt-1)/maxnumber)))
        if ret <= 0:
            return 1
        return 2**ret

    def set_Npnt(self, firstrecord, lastrecord, step, verbose):
        '''
        :purpose: set number of points using number of points in source
            and the parameters firstrecord, lastrecord and step
        '''
        if self.NpntInSource < 0:
            raise ValueError('Number of points in source file invalid')
        self.Npnt = 0
        irec = 0
        Npnt = self.NpntInSource
        first = 0
        last = self.NpntInSource - 1
        if firstrecord >= 0:
            if firstrecord >= self.NpntInSource:
                raise ValueError(
                    'Given first record %d >= number of points (%d)'%(
                        firstrecord, self.NpntInSource))
            first = firstrecord
        if lastrecord >= 0:
            last = lastrecord
            if lastrecord < first:
                print('No data loaded: Given last record %d < first %d'%(
                    lastrecord, first))
            if lastrecord >= self.NpntInSource:
                print('Given last record %d >= number of points (%d). %s'%(
                        lastrecord, self.NpntInSource
                        , 'Number from source taken'))
                last = self.NpntInSource - 1
        if step < 0:
            raise ValueError('Invalid step %d'%step)
        self.Npnt = int((last-first)/step) + 1
        if verbose:
            print('%d records in file'%(self.NpntInSource))
            print('%d records in object'%(self.Npnt))
        return first, last, step

    def _field_from_label(self, ifield
            , name_in_source, fieldtype=-1, verbose=False):
        '''
        :purpose: define a field, using label, calibration factor, offset, unit
            and fieldtype, in many cases the field type can be extracted from
            the column name
        
        :usage: in specific (text) file formats the logic is different, then inherit
            this class and override this method
            
            the default is the wmcs logic
            * channel: fieldtype_channel_signal
            * A_channel: fieldtype_average
            * R_channel: fieldtype_range
            * MIN_channel: fieldtype_min
            * MAX_channel: fieldtype_max
        '''
        dummyfld = wmc_data_field(name='dummy', number=0)
        fieldtype=-1
        channelname = name_in_source
        if name_in_source == self.timecolumn:
            fieldtype = dummyfld.fieldtype_time
            channelname = ''
        elif name_in_source.startswith(self.prefixaverage):
            fieldtype = dummyfld.fieldtype_average
            # correct channel number is given for range fields
            channelname = name_in_source[len(self.prefixaverage):]
        elif name_in_source.startswith(self.prefixrange):
            fieldtype = dummyfld.fieldtype_range
            channelname = name_in_source[len(self.prefixrange):]

        return wmc_data_field(ifield, name=name_in_source, fieldtype=fieldtype
            , name_in_source=name_in_source, channelname=channelname
            , skip=False)            
        
    def _unit_from_label(self, label, verbose):
        '''
        :purpose: obtain unit from label
            by default it is taken from a separate array units
        '''
        return None
        
    def _channels_and_fields_from_labels(self
        , labels, calfacs, offsets, units
        , verbose=False):
        '''
        :purpose: obtain channel and field definition from list of label names
        
        :usage: can be used for wmcs, and most text formats
        '''
        for i, lbl in enumerate(labels):
            fld = self._field_from_label(ifield=i, name_in_source=lbl
                , fieldtype=-1, verbose=verbose)
            if fld.fieldtype == -1:
                # not set in _field_from_label
                fld.fieldtype = fld.fieldtype_channel_signal
            # unit, calibration factor and offset are channel properies
            # not field properties
            unit = self._unit_from_label(label=lbl, verbose=verbose)
            if unit is None:
                unit = units[i]
            self.add_data_field(fld
                , unit=unit, calfac=calfacs[i], offset=offsets[i]
                , verbose=verbose)
        self.channels.finalize()
        if verbose:
            print(self.channels)
    
    def load_header(self, verbose=False):
        '''
        :purpose: determine meta-data of the file
            file data: type, date
            number of records in source file
            channel data: column names, calibration factors, offsets, units
        
        :details: should be implemented in inherited class
        '''
        self.NpntInSource = -1
        raise ValueError(
            'Not implemented. Should be implemented in inherited class')
        
    def _count_records(self, verbose=False):
        '''
        :purpose: count records using reader. Assume you just read the header.
        '''
        self.NpntInSource = -1
        raise ValueError(
            'Not implemented. Should be implemented in inherited class')

    def load_data(self, firstrecord=-1, step=1, lastrecord=-1, verbose=False):
        raise ValueError(
            'Not implemented. Should be implemented in inherited class')
            
    def finish_load(self):
        pass

class mapped_channel:
    def __init__(self, meas, channel, columnname='', unit='', scaling=1):
        self.channel = channel
        if len(columnname) == 0:
            self.columnname = channel
        else:
            self.columnname = columnname
        if len(unit) == 0:
            # obtain unit from measurement, relies on lazy evaluation
            if ('units' in meas.__dict__) and (channel in meas.units):
                self.unit = meas.units[channel]
            else:
                self.unit = '-'
        else:
            self.unit = unit
        self.scaling = scaling
    
    def __str__(self):
        s = 'channel "%s", unit [%s]'%(self.channel, self.unit)
        if not (self.channel == self.columnname):
            s += ', column "%s"'%self.columnname
        if not (self.scaling == 1):
            s += ', scaling "%g"'%self.scaling
        
        return s

    
# ==== WMClib General Functions =====================================
# ===================================================================

def isFloat(s):
    """
    Returns a Boolean to indicate if *s* can be converted to a float
    """
    try: float(s)
    except (ValueError, TypeError): return False
    else: return True

def isInt(s):
    """
    Returns a Boolean to indicate if *s* can be converted to a float
    """
    try: int(s)
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

class wmcs_data_record:
    def __init__(self, block, Nchn, irec):
        self.irec = irec
        self.Nchn = Nchn
        
        recordsize = Nchn * 4 + 40
        offset = recordsize * irec
        newoffset = offset + 4 * Nchn
        self.data = np.array(
            struct.unpack('%df' % Nchn, block[ offset : newoffset]))
        
        # fixed fields
        offset = newoffset
        for i in range(5):
            offset = newoffset
            newoffset = offset + 8
            x = int(struct.unpack('q', block[ offset : newoffset ])[0])
            if i==0:
                self.scantime = x
            elif i==1:
                self.sec = x
            elif i==2:
                self.nsec = x
            elif i==3:
                self.status = x
            elif i==4:
                self.counter = x

class wmcs_data_block:
    # some 'constants', block identifiers
    BT_WMCS_IDENTIFIER  =  0
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

    BT_EOF  =  999
    
    def __init__(self, type=-1, length=0, block=None):
        if type >= 0:
            self.type = type
        else:
            self.type = self.BT_EOF
        self.length = length
        self.total_block_length = self.length + 8 # block type and block size
        self.block = block
    
    def get_integer(self):
        return int(struct.unpack('i', self.block)[0])

    def set_channel_string(self):
        self.channel = -1
        self.value = ''
        if self.length >= 4: 
            self.channel = int(struct.unpack('i', self.block[0:4])[0])
            self.value = self._blockbytes2string(self.block[4:self.length])
    
    def set_channel_float(self):
        self.channel = -1
        self.value = 0.0
        if self.length >= 4: 
            self.channel = int(struct.unpack('i', self.block[0:4])[0])
            self.value = float(struct.unpack('f', self.block[4:12])[0])

    def _blockbytes2string(self, s):
        if isinstance(s, str):
            return s
        return s.decode('cp437')
    
    def eof(self):
        return self.type == self.BT_EOF
        
    def isdatarecord(self, Nchn=-1, onlycount=True):
        ret = (self.type == self.BT_DATA_RECORDS)
        if ret and (Nchn >= 0):
            self.valid = True # initial state
            recordsize = Nchn * 4 + 40
            if not (self.length % recordsize == 0):
                self.valid=False
                print('incorrect block size')
                return ret
            if self.block is None:
                self.valid=False
                print('block is null')
                return ret
            self.nrec = int(self.length / recordsize)
            if not onlycount:
                self.records = []
                for i in range(self.nrec):
                    try:
                        self.records.append(
                            wmcs_data_record(self.block, Nchn, i))
                    except:
                        print(self)
                        print(sys.exc_info()[1])
                        print('Error parsing data record')
                        self.valid = False
        return ret

    def isidentifier(self):
        ret = (self.type == self.BT_WMCS_IDENTIFIER)
        if ret:
            self.value = self._blockbytes2string(self.block)
        return ret

    def isfiletype(self):
        ret = (self.type == self.BT_FILE_TYPE)
        if ret:
            self.value = self.get_integer()
        return ret
                
    def ischannelcount(self):
        ret = (self.type == self.BT_CHN_COUNT)
        if ret:
            self.value = self.get_integer()
        return ret
    
    def ischannellabel(self):
        ret = (self.type == self.BT_CHANNEL_LABEL)
        if ret:
            self.set_channel_string()
        return ret
    
    def ischannelunit(self):
        ret = (self.type == self.BT_CHANNEL_UNIT)
        if ret:
            self.set_channel_string()
        return ret
    
    def ischannelcalfac(self):
        ret = (self.type == self.BT_CHANNEL_CALFAC)
        if ret:
            self.set_channel_float()
        return ret

    def ischanneloffset(self):
        ret = (self.type == self.BT_CHANNEL_OFFSET)
        if ret:
            self.set_channel_float()
        return ret
    
    def isunixtimesec(self):
        ret = (self.type == self.BT_UNIX_TIME_SEC)
        if ret:
            self.value = int(struct.unpack('q',self.block)[0])
        return ret

    def isunixtimensec(self):
        ret = (self.type == self.BT_UNIX_TIME_NSEC)
        if ret:
            self.value = int(struct.unpack('q',self.block)[0])
        return ret
    
    def isrecordno(self):
        return self.type == self.BT_RECORD_NO
    
    def iscycleno(self):
        return self.type == self.BT_CYCLE_NO
    
    def is100percycleno(self):
        return self.type == self.BT_100PER_CYCLE_NO
        
    def __str__(self):
        s = 'Block (%3d): '%self.type
        if self.eof():
            s += 'End of file'
        elif self.isdatarecord():
            s += 'Data record'
        elif self.isidentifier():
            s += 'Identifier "%s"'%self.value
        elif self.isfiletype():
            s += 'File type %d'%self.value
        elif self.ischannelcount():
            s += 'Channel count %d'%self.value
        elif self.ischannellabel():
            s += 'Channel label (%d) "%s"'%(self.channel, self.value)
        elif self.ischannelunit():
            s += 'Channel unit (%d) "%s"'%(self.channel, self.value)
        elif self.ischannelcalfac():
            s += 'Channel calibration factor (%d) %g'%(self.channel, self.value)
        elif self.ischanneloffset():
            s += 'Channel offset (%d) %g'%(self.channel, self.value)
        elif self.isunixtimesec():
            s += 'Unix time sec %d'%self.value
        elif self.isunixtimensec():
            s += 'Unix time nsec %d'%self.value
        elif self.isrecordno():
            s += 'Record no'
        elif self.iscycleno():
            s += 'Cycle no'
        elif self.is100percycleno():
            s += '100 per cycle no'
        else:
            s  += 'Unknown block type'
        return s

# ==== WMClib Data Functions
# ===================================================================
class wmc_data_wmcs(wmc_data):
    
    # file types
    FT_BUFFER = 1 # buffer
    FT_POINTS = 2 # points
    FT_RNGAVG = 3 # range-average
    
    def __init__(self, file_name, skipChn=True, skipNc=True):
        wmc_data.__init__(self, file_name=file_name)
        self.skipChn = skipChn
        ''' skip channels starting with "chn" '''
        self.skipNc = skipNc
        ''' skip channels starting with "nc" '''
        self.file_size = 0
        ''' file size '''
        self.reader = None
        ''' file reader '''
        self.index = 0
        ''' file reader index '''
        self.Nchn_in_source = 0
        ''' number of channels in source '''
        self.currentblock = None
        ''' block read from file '''
        self.unixtime_sec = int(0)
        ''' unix time seconds '''
        self.unixtime_nsec = int(0)
        ''' unix time nano-seconds '''
        self.wmcs_file_type = -1
        ''' WMCS file type '''
        self.timecolumn = 'unixtime'
        self.onerecordperblock = True
        ''' contains one record per block '''
        
    def _next_block_from_file(self, skipbytes=0):
        # read the meta-data
        self.currentblock = wmcs_data_block()
        if skipbytes > 0:
            self.reader.seek(skipbytes, os.SEEK_CUR)
            self.index += skipbytes
            
        if self.index + 8 <= self.file_size:
            chunk = self.reader.read(8)
            block_type = int(struct.unpack('i', chunk[0:4],)[0])
            block_len  = int(struct.unpack('i', chunk[4:8],)[0])
            block = None
            
            self.index += 8 # block type and size
            
            if block_len < 0:
                raise ValueError('Block length < 0')
            if self.index + block_len <= self.file_size:
                block = self.reader.read(block_len)
                self.index += block_len
            else:
                print('File too short: Index %d, Length %d, Size %d'%(
                    self.index, block_len, self.file_size))
                
            self.currentblock = wmcs_data_block(block_type, block_len, block)
        
    def load_header(self, verbose=False):
        # read file as one big chunk
        self.file_size = os.path.getsize(self.file_path)
        ''' file size '''
        if verbose:
            print('Loading header')
        # initialize data structures
        units     = None
        labels    = None
        calfacs   = None
        offsets   = None
        
        self.unixtime_sec  = int(0)
        self.unixtime_nsec = int(0)
        filetype = -1
        # iterate over the blocks in the chunk, and process the known blocks
        #for block_type, block_len, block in blocks_from_chunk(chunk):
        self.reader = open(self.file_path,'rb')
        self.index = 0
        
        nxt = True
        while nxt:
            self._next_block_from_file()
            if verbose and not (
                self.currentblock.isdatarecord()
                or self.currentblock.ischannellabel()
                or self.currentblock.ischannelunit()
                or self.currentblock.ischannelcalfac()
                or self.currentblock.ischanneloffset()):
                print(self.currentblock)
            if self.currentblock.eof() or self.currentblock.isdatarecord():
                nxt = False
            elif self.currentblock.isidentifier():
                if not (self.currentblock.value == 'WMCS'):
                    print('wrong identifier "%s", ignored'%(
                        self.currentblock.value))
            elif self.currentblock.isfiletype():
                self.wmcs_file_type = self.currentblock.value
            elif self.currentblock.ischannelcount():
                if self.Nchn_in_source == 0:
                    self.Nchn_in_source = self.currentblock.value
                    if self.Nchn_in_source > 0:
                        calfacs   = np.zeros(self.Nchn_in_source)
                        offsets   = np.zeros(self.Nchn_in_source)
                        units     = []
                        labels    = []
                        for i in range(self.Nchn_in_source):
                            units.append('')
                            labels.append('')
                else:
                    # in future we might reallocate stuff...
                    print('more than one channel count, ignored at first')

            elif self.currentblock.ischannellabel():
                chn = self.currentblock.channel
                if chn >= 0 and chn < self.Nchn_in_source:
                    labels[chn] = self.currentblock.value
            elif self.currentblock.ischannelunit():
                chn = self.currentblock.channel
                if chn >= 0 and chn < self.Nchn_in_source:
                    units[chn] = self.currentblock.value
            elif self.currentblock.ischannelcalfac():
                chn = self.currentblock.channel
                if chn >= 0 and chn < self.Nchn_in_source:
                    calfacs[chn] = self.currentblock.value
            elif self.currentblock.ischanneloffset():
                chn = self.currentblock.channel
                if chn >= 0 and chn < self.Nchn_in_source:
                    offsets[chn] = self.currentblock.value
            elif self.currentblock.isunixtimesec():
                self.unixtime_sec = self.currentblock.value
            elif self.currentblock.isunixtimensec():
                self.unixtime_nsec = self.currentblock.value
            elif self.currentblock.isrecordno():
                pass
            elif self.currentblock.iscycleno():
                pass
            elif self.currentblock.is100percycleno():
                pass
            else:
                print(self.currentblock)
        self._channels_and_fields_from_labels(labels, calfacs, offsets, units
            , verbose=verbose)
        self._count_records(verbose=verbose)
        self.reader.close()
    
    def _field_from_label(self, ifield, name_in_source, fieldtype=-1
        , verbose=False):
        '''
        :purpose: define a field, using label, calibration factor, offset, unit
            and fieldtype, in many cases the field type can be extracted from
            the column name
        
        :usage: in specific (text) file formats the logic is different, then inherit
            this class and override this method
            
            the default is the wmcs logic
            * channel: fieldtype_channel_signal
            * A_channel: fieldtype_average
            * R_channel: fieldtype_range
            * MIN_channel: fieldtype_min
            * MAX_channel: fieldtype_max
        '''
        # default
        fld = wmc_data._field_from_label(self, ifield, name_in_source
            , fieldtype=fieldtype, verbose=verbose)
        # (optionally) skip irrelevant channels
        if self.skipNc and fld.channelname.lower().startswith('nc'):
            fld.skip = True
            if verbose:
                print('Skip field %d ("field name "%s", channel "%s")'%(
                    ifield, fld.name, fld.channelname))
        if self.skipChn and fld.channelname.lower().startswith('chn'):
            fld.skip = True
            if verbose:
                print('Skip field %d ("field name "%s", channel "%s")'%(
                    ifield, fld.name, fld.channelname))
        return fld            
        
    def _count_records(self, verbose=False):        
        # We are now at the first data block, now count the number of records
        n_blocks2check = 100
        if verbose:
            print('Index after first data block: %d'%self.index)
        nxt = self.currentblock.isdatarecord(Nchn=self.Nchn_in_source
            , onlycount=True)
        self.NpntInSource = 0
        i_block = 0
        while nxt:
            self.NpntInSource += self.currentblock.nrec
            i_block += 1
            if self.onerecordperblock:
                if self.currentblock.nrec == 1:
                    # could be a new-style file with 1 data record per block
                    # then the number of records can be determined very quickly
                    nr_remaining = self.file_size - self.index
                    x = nr_remaining % self.currentblock.total_block_length
                    if x == 0:
                        # exactly divided by total block length
                        # could be a new-style file with 1 data record per block
                        # From now on, assume that it is
                        nr_remaining = int(
                            nr_remaining /self.currentblock.total_block_length)
                        if verbose:
                            print('Estimated %d points in block %d'%(
                                self.NpntInSource+nr_remaining, i_block))
                        if i_block > n_blocks2check:
                            nxt = False
                            if verbose:
                                print('Using estimated number of points')
                            self.NpntInSource+=nr_remaining
                    else:
                        self.onerecordperblock = False
                        if verbose:
                            print('Block %d has 1 record, but remainder not zero'%( i_block))
                else:
                    self.onerecordperblock = False
                    if verbose:
                        print('Block %d has %d records'%(
                                i_block, self.currentblock.nrec))
            
            self._next_block_from_file()
            if not self.currentblock.isdatarecord(Nchn=self.Nchn_in_source
                , onlycount=True):
                nxt = False
    
    def finish_load(self):
        self.index = 0
        self.reader.close()
        self.Nchn_in_source = 0
        
    def add_record(self, rec, iindata, iinsource
        , channels, signals
        , firstrecord=-1, step=1, lastrecord=-1):
        ret = True
        if iinsource < firstrecord:
            ret = False
        if iinsource > lastrecord:
            ret = False
        if (not (lastrecord == iinsource)) and (
            not ((iinsource-firstrecord) % step == 0)):
            ret = False
        if ret:
            self['scantime'][iindata] = rec.scantime
            self['unixtime'][iindata] = float(rec.sec) \
                + float(rec.nsec) * 1.0e-9
            self['utime_sec'][iindata] = rec.sec
            self['utime_nsec'][iindata] = rec.nsec
            self['recordinsource'][iindata] = iinsource
            self['status'][iindata] = rec.status
            self['counter'][iindata] = rec.counter
            for i, chnl in enumerate(channels):
                signals[i][iindata] = rec.data[chnl]
        return ret
        
    def load_data(self, firstrecord=-1, step=1, lastrecord=-1, verbose=False):
        if verbose:
            print('Loading data')
        if self.NpntInSource == 0:
            print('No data found')
            return
        self.index = 0
        self.reader = open(self.file_path,'rb')
        nxt = True
        while nxt:
            self._next_block_from_file()
            if self.currentblock.isdatarecord():
                nxt = False
                # index is after the first data record
                
                if self.onerecordperblock and (firstrecord > 0):
                    # one record per block, so we can easily estimate
                    # skip firstrecord-1 records, because after that 
                    # block is filled with record[firstrecord]
                    # example:
                    #     firstrecord=1, currentblock contains record 0
                    #     nothing skipped, but only fill currentblock with next
                    self._next_block_from_file(skipbytes=(firstrecord-1)* \
                            self.currentblock.total_block_length)
                     
            if self.currentblock.eof():
                raise ValueError('No data found before end of file')
        if verbose:
            print('Allocating arrays')
        # pointer is at the first data block
        # now we can allocate numpy arrays
        # fixed fields
        self['unixtime'] = np.zeros(self.Npnt)
        a = np.array(range(self.Npnt),dtype=np.int64)
        self['record']   = np.zeros_like(a)
        self['recordinsource']  = np.zeros_like(self['record'])
        self['status']   = np.zeros_like(self['record'])
        self['counter']  = np.zeros_like(self['record'])
        self['scantime'] = np.zeros_like(self['record'])
        self['utime_sec'] = np.zeros_like(self['record'])
        self['utime_nsec'] = np.zeros_like(self['record'])

        channels = []
        signals = []
        labels = []
        for i in self.fields:
            fld = self.fields[i]
            if not fld.skip:
                channels.append(i)
                signals.append(np.zeros(self.Npnt))
                labels.append(fld.name)
        if verbose:
            print('%d signals found'%len(labels))
            print('Reading records from file')
        
        nxt =  True
        
        stepmessage = int(self.NpntInSource/10)
        if stepmessage < 1:
            stepmessage = 1
        iindata = 0
        if firstrecord > 0:
            iinsource = firstrecord
        else:
            iinsource = 0
        if self.onerecordperblock:
            stp = 1
        else:
            stp = step
        self.currentblock.isdatarecord(self.Nchn_in_source, onlycount=False)
        while nxt:
            if not self.currentblock.valid:
                print('Invalid block after %d records'%(iinsource))
            else:
                for rec in self.currentblock.records:
                    if verbose and (iinsource % stepmessage == 0):
                        print('Reading record %d of %d'%(
                            iinsource+1, self.NpntInSource))
                    if self.add_record(rec, iindata, iinsource
                        , channels, signals
                        , firstrecord=firstrecord, step=stp
                        , lastrecord=lastrecord):
                        iindata += 1
                        if iindata >= self.Npnt:
                            nxt = False
                    iinsource += 1
                
            if nxt:
                if (step > 1) and self.onerecordperblock:
                    self._next_block_from_file(skipbytes=(step-1) * \
                        self.currentblock.total_block_length)
                    iinsource += step-1
                else:
                    self._next_block_from_file()
                if not self.currentblock.isdatarecord(self.Nchn_in_source
                    , onlycount=False):
                    nxt = False
        self.reader.close()
        for i, lbl in enumerate(labels):
            self[lbl] = signals[i]
        dttm = self.unixtime_sec
        if self.Npnt > 0:
            dttmdata = self.utime_sec[0]
            if (dttmdata - dttm) > 3600 * 24 * 365 * 3: 
                # more than 3 years difference between 
                # file date and date of 1st record. We do not believe it.
                dttm = dttmdata
        if dttm > 0:
            x = datetime.datetime.fromtimestamp(dttm)
            self.file_date = x.strftime('%Y-%m-%d')
            self.file_time = x.strftime('%H:%M:%S')
        else:
            self.file_date = '0000-00-00'
            self.file_time = '00:00:00'
        
def load_wmcs(inFile, rep_channels=None, skipChn=True
    , skipNc=True, start=None, stop=None, step=1, verbose=False):
    """
    Loads the data from a WMCS data file [.buffer|.rngavg|.points] into a 
    wmcs_data object.
    
    :param inFile: path and filename
        
    :param rep_channels: repaired channels

    :param skipChn: 
        skip channels with labels starting with 'chn', default True

    :param skipNc:
        skip channels with lables starting with 'nc', default True

    :param start: skip records before the *start* record
            
    :param stop: skip records after the *stop* record
        
    :param step: take every *step* record
            
    """
    a = glob.glob(inFile)
    if len(a) == 0:
        print('WARNING: file "%s" does not exist'%inFile)
        return None
        
    ameas = []
    for x in a:
        folder, file_name = os.path.split(x)
        if start == None:
            firstrecord = -1
        else:
            firstrecord = start
        if stop == None:
            lastrecord = -1
        else:
            lastrecord = stop
        
        wd = wmc_data_wmcs(file_name=file_name, skipChn=skipChn, skipNc=skipNc)
        wd.load(folder=folder, rep_channels=rep_channels
            , firstrecord=firstrecord, lastrecord=lastrecord, step=step
            , verbose=verbose)
        if len(a) == 1:
            return wd
        ameas.append(wd)
    return append_wmc_data(ameas, verbose=verbose)

def load_xls(inFile,inOptions=''):
    """
    Loads the data from an .xls excel file into a wmc_data object.
    
    The data should be in the first sheet, in a full rectangle data
    block, the first column should be the label.
    
    The format is the same as produced by wmc_data.save_xls()
    
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
    
    # create new wmc_data object
    wd = wmc_data()
    wd.allocate(sheet.nrows-1)
    
    for i in range(sheet.ncols):
        label = (str(sheet.cell(0,i).value)).strip()
        wd[label] = np.array(sheet.col_values(i,1,sheet.nrows))
        
    # some admin...
    wd.file_type = 'xls'
    return wd

class wmc_data_text(wmc_data):
    def __init__(self, file_name='', Npnt=0, separator=','
        , timecolumn='testtime', timefactor=1.0
        , numberOfHeaderLines=-1
        , lineWithFields=None, columnnames=None
        , lineWithCalfacs=-1, calfacs=None
        , lineWithOffsets=-1, offsets=None
        , lineWithUnits=-1, units=None
        , prefixrange='R_', prefixaverage='A_'):
        wmc_data.__init__(self, file_name=file_name, inNpnt=Npnt)
        self.separator = separator
        ''' field separator '''
        self.timecolumn = timecolumn
        ''' name of the column that contains the time signal '''
        self.numberOfHeaderLines = numberOfHeaderLines
        ''' 
        number of header lines,
        if -1, 1st after largest line with header data
        (field names, calibration factors et cetera)
        '''
        self.timefactor = timefactor
        ''' factor, which makes seconds from the time signal '''
        self.lineWithFields = lineWithFields
        ''' if n >= 0, column names are taken from line n (count from 0)'''
        self.columnnames = columnnames
        ''' column names, if not taken from line '''
        self.lineWithCalfacs = lineWithCalfacs
        ''' if n >= 0, calibration factors are taken from line n (count from 0)'''
        self._calfacs = calfacs
        ''' calibration factors, if not read from line '''
        self.lineWithOffsets = lineWithOffsets
        ''' if n >= 0, offsets are taken from line n (count from 0)'''
        self._offsets = offsets
        ''' offsets, if not read from line '''
        self.lineWithUnits = lineWithUnits
        ''' if n >= 0, units are taken from line n (count from 0)'''
        self._units = units
        ''' units, if not read from line '''
        self.prefixrange = prefixrange
        ''' prefix for a range field 'R_' '''
        self.prefixaverage = prefixaverage
        ''' prefix for a average field, default 'A_' '''
        if self.separator == ' ':
            self.separator = None
        valid = True
        if lineWithFields is None:
            if self.numberOfHeaderLines == 0:
                # set to -1 if there are no header lines
                self.lineWithFields = -1
            else:
                self.lineWithFields = 0 # default in first line
        if (columnnames is not None) and (self.lineWithFields >= 0):
            print('Conflicting settings: %s are given and should be taken from line %d'%(
                'Column names', self.lineWithFields))
        if (units is not None) and (self.lineWithUnits >= 0):
            print('Conflicting settings: %s are given and should be taken from line %d'%(
                'Units', self.lineWithUnits))
        if (calfacs is not None) and (self.lineWithCalfacs >= 0):
            valid = False
            print('Conflicting settings: %s are given and should be taken from line %d'%(
                'Calibration factors', self.lineWithCalfacs))
        if (offsets is not None) and (self.lineWithOffsets >= 0):
            valid = False
            print('Conflicting settings: %s are given and should be taken from line %d'%(
                'Calibration factors', self.lineWithCalfacs))
        if (numberOfHeaderLines < 0): # not set
            if self.numberOfHeaderLines <= self.lineWithFields:
                self.numberOfHeaderLines = self.lineWithFields + 1
            if self.numberOfHeaderLines <= self.lineWithUnits:
                self.numberOfHeaderLines = self.lineWithUnits + 1
            if self.numberOfHeaderLines <= self.lineWithOffsets:
                self.numberOfHeaderLines = self.lineWithOffsets + 1
            if self.numberOfHeaderLines <= self.lineWithCalfacs:
                self.numberOfHeaderLines = self.lineWithCalfacs + 1
        if self.numberOfHeaderLines <= self.lineWithFields:
            valid = False
            print('Conflicting settings: Number of header lines (%d) <= line with %s (%d)'%(
                self.numberOfHeaderLines, 'column names', self.lineWithFields))
        if self.numberOfHeaderLines <= self.lineWithUnits:
            valid = False
            print('Conflicting settings: Number of header lines (%d) <= line with %s (%d)'%(
                self.numberOfHeaderLines, 'units', self.lineWithUnits))
        if self.numberOfHeaderLines <= self.lineWithOffsets:
            valid = False
            print('Conflicting settings: Number of header lines (%d) <= line with %s (%d)'%(
                self.numberOfHeaderLines, 'offsets', self.lineWithOffsets))
        if self.numberOfHeaderLines <= self.lineWithCalfacs:
            valid = False
            print('Conflicting settings: Number of header lines (%d) <= line with %s (%d)'%(
                self.numberOfHeaderLines, 'calibrationfactors', self.lineWithCalfacs))
        self.encoding = ''
        if not valid:
            raise ValueError('Error in text file definition')

    def load_header(self, verbose=False):
        '''
        :purpose: obtain labels, calibration factor, et cetera
            and number of first line with data
        '''
        # determine encoding
        with open(self.file_path, 'rb') as f:
            try:
                import chardet
                x = chardet.detect(f.read(5))
                if x['confidence'] > 0.9999:
                    print('Detected encoding "%s"'%(x['encoding']))
                else:
                    print('Detected encoding "%s" (Confidence %.1f %%)'%(
                        x['encoding'], 100. * x['confidence'] ))
                self.encoding = x['encoding']
            except:
                print('WARNING: Detecting of encoding failed')
            f.close()
        lines = []
        with io.open(self.file_path, 'r', encoding=self.encoding) as f:
            for i in range(self.numberOfHeaderLines):
                s = f.readline()
                if len(s) > 0:
                    if isinstance(s, str):
                        lines.append(s.strip())
                    else:
                        lines.append(s.strip().decode(self.encoding).encode("latin1"))
                else:
                    raise ValueError(
                        'File too short: %d header lines expected'%(
                            self.numberOfHeaderLines))
            self.get_column_info_from_header(lines, verbose=verbose)
            self._count_records(f, verbose=verbose)            
            f.close()

    def _count_records(self, f, verbose=False):        
        # read first data line, skip empty lines
        # each (non-empty) line is counted
        self.NpntInSource = 0
        s = f.readline()
        while len(s) > 0:
            if len(s.strip()) > 0:
                self.NpntInSource +=1 
            s = f.readline()
 
    def get_column_info_from_header(self, lines, verbose=False):
        '''
        :purpose: obtain labels, units, calibration factors and offsets from 
            header lines
            
        :usage: if e.g. unit is part of column name, overwrite this method
        '''
        
        # determine labels from file or from definition
        labels = []
        if self.lineWithFields >= 0:
            if verbose:
                print('Reading columns from header')
            a = lines[self.lineWithFields].strip().split(self.separator)
            for col in a:
                labels.append('%s'%col)
        else:
            if self.columnnames is None:
                raise(ValueError('No column names given'))
            for col in self.columnnames:
                labels.append(col)
        if len(labels) < 2:
            raise(ValueError('Number of columns (%d) too small: %s'%(
                len(labels), ','.join(labels))))
        if verbose:
            print('%d columns found: %s'%(len(labels), ','.join(labels)))
        
        # determine units from file or from definition
        units = []
        if self.lineWithUnits >= 0:
            if verbose:
                print('Reading units from header')
            a = lines[self.lineWithUnits].strip().split(self.separator)
            for col in a:
                units.append('%s'%col)
        else:
            if self._units is None:
                if verbose:
                    print('No units given, assume empty strings')
                
                for col in labels:
                    units.append('')
            else:
                if not (len(self._units) == len(labels)):
                    raise ValueError('%s %s'%(
                        'Number of given units in class definition'
                        , 'does not match number of columns'))
                for el in self._units:
                    units.append(el)
                    
        # determine calibration factors from file or from definition
        calfacs = []
        if self.lineWithCalfacs >= 0:
            if verbose:
                print('Reading calibration factors from header')
            a = lines[self.lineWithCalfacs].strip().split(self.separator)
            for col in a:
                calfacs.append(np.float(col))
        else:
            if self._calfacs is None:
                if verbose:
                    print('No calibration factors given, assume 1')
                calfacs = np.ones(len(labels))
            else:
                if not (len(self._calfacs) == len(labels)):
                    raise ValueError('%s %s'%(
                        'Number of given calibration factors in class definition'
                        , 'does not match number of columns'))
                for el in self._calfacs:
                    calfacs.append(el)
                
        # determine calibration factors from file or from definition
        offsets = []
        if self.lineWithOffsets >= 0:
            if verbose:
                print('Reading calibration factors from header')
            a = lines[self.lineWithOffsets].strip().split(self.separator)
            for col in a:
                offsets.append(np.float(col))
        else:
            if self._offsets is None:
                if verbose:
                    print('No offsets given, assume 0')
                offsets = np.zeros(len(labels))
            else:
                if not (len(self._offsets) == len(labels)):
                    raise ValueError('%s %s'%(
                        'Number of given offsets in class definition'
                        , 'does not match number of columns'))
                for el in self._offsets:
                    offsets.append(el)
        
        self._channels_and_fields_from_labels(labels, calfacs, offsets, units
            , verbose=verbose)

    def load_data(self, firstrecord=0, step=1, lastrecord=-1, verbose=False):
        with io.open(self.file_path, 'r', encoding=self.encoding) as f:
            for i in range(self.numberOfHeaderLines):
                s = f.readline()
                if len(s) == 0:
                    raise ValueError(
                        'File too short: %d header lines expected'%(
                            self.numberOfHeaderLines))
            irec = 0
            for i in range(firstrecord):
                s = f.readline()
                if len(s) == 0:
                    raise ValueError(
                        'File too short: at least %d record lines expected'%(
                            self.numberOfHeaderLines))
            for i in range(firstrecord, lastrecord+1):
                s = f.readline()
                if len(s) == 0:
                    raise ValueError(
                        'File too short: at least %d record lines expected'%(
                            self.numberOfHeaderLines))
                if (i%step == 0) or (i == lastrecord):
                    a = s.strip().split(self.separator)
                    msg = self.parseRecord(a, irec)
                    if len(msg) > 0:
                        print(msg)
                        raise ValueError('Error parsing line %d\n%s'%(
                            i+self.numberOfHeaderLines, s.strip()))
                    self['recordinsource'][irec] = i
                    irec += 1
            f.close()
            
    def parseRecord(self, a, irec):
        ret = ''
        for i in self.fields:
            fld = self.fields[i]
            try:
                self[fld.name][irec] = self.parseField(a[i], i, irec)
            except Exception as e:
                ret += e.__str__()
        return ret
                                                
    def parseField(self, s, ifield, irec):
        return np.float(s)
    
def load_txt(filepath, separator=','
    , timecolumn='testtime', timefactor=1.0
    , rep_channels=None, firstlineinfile=-1, step=1, lastlineinfile=-1
    , numberOfHeaderLines=-1
    , lineWithFields=0, columnnames=None
    , lineWithCalfacs=-1, calfacs=None
    , lineWithOffsets=-1, offsets=None
    , lineWithUnits=-1, units=None
    , prefixrange='R_', prefixaverage='A_'
    , verbose=False):
    '''
    load the data in a text file into a wmc_data object
    
    two columns are added
        * record: counter in resulting wmc_data object
        * lineinfile: counter of lines in original file (starts at 0)
    
    :param filepath: full name of the file
    :param separator: separator
    :param timecolumn: column, which contains the test time
    :param rep_channels: repaired channels
    :param firstlineinfile: first line which should be read
    :param lastlineinfile: last line to be read
        if step != 1, there is a chance that this record is not present
    :param step: if not 1, then each nth line is read, 
    :param columnnames: column names, if not taken from header
    
    Loads the data from a text file with column=channel
    '''
    
    wd = wmc_data_text(Npnt=0, separator=separator
        , timecolumn=timecolumn, timefactor=timefactor
        , numberOfHeaderLines=numberOfHeaderLines
        , lineWithFields=lineWithFields, columnnames=columnnames
        , lineWithCalfacs=lineWithCalfacs, calfacs=calfacs
        , lineWithOffsets=lineWithOffsets, offsets=offsets
        , lineWithUnits=lineWithUnits, units=units
        , prefixrange=prefixrange, prefixaverage=prefixaverage)
    wd.load(filepath
    , rep_channels=rep_channels, firstlineinfile=firstlineinfile
    , step=step, lastlineinfile=lastlineinfile
    , verbose=verbose)
    return wd

# ==== WMClib Plotting Functions
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
    Modification of matplotlib.savefig, adds 'WMC' logo to the saved figure.
    """
    plt.ioff()
    #old_w,old_h = plt.gcf().get_size_inches()
    #plt.gcf().set_size_inches(w,h)  
    
    plt.text(wmclibdata.savefig_logo_x, wmclibdata.savefig_logo_y,
             wmclibdata.savefig_logo_text,
             style=wmclibdata.savefig_logo_style, 
             weight='bold', 
             size=wmclibdata.savefig_logo_size,
             color=wmclibdata.savefig_logo_color, 
             horizontalalignment='right',
             transform = plt.gca().transAxes)
    filename, fileext = os.path.splitext(inName)
    if fileext.lower() == '.eps':
        try:
            flpdf = '%s.pdf'%filename
            plt.savefig(flpdf)
            exepath = ''
            if 'win' in sys.platform.lower():
                exepath = os.path.join(os.path.dirname(sys.executable)
                    , 'Lib', 'site-packages', 'xpdf', 'pdftops.exe')
                if not os.path.exists(exepath):
                    exepath = ''
            elif 'linux' in sys.platform.lower():
                exepath = '/usr/bin/pdftops'
            if len(exepath) > 0:
                subprocess.call([exepath, '-eps', flpdf, inName])
        except:
            print('Conversion of "%s" to eps failed, generate eps drectly'%(
                flpdf))
        if not os.path.exists(inName):
            plt.savefig(inName)
    else:
        plt.savefig(inName)
    del(plt.gca().texts[-1])
    #plt.gcf().set_size_inches(old_w,old_h)
    plt.ion()

def add_transparent_text(text='DRAFT', fontsize=100, rotation=45, alpha=0.4
    , ax=None):
    '''
    :purpose: Adds transparent text to a figure
    
    :param text: text to add
    :param fontsize: font size
    :param rotation: angle (degrees)
    :param alpha: transparency
    :param ax: axis object
    '''
    if ax is None:
        ax =plt.gca()
    txt = ax.text(0.5, 0.5, text
        , verticalalignment='center', horizontalalignment='center'
        , fontsize=fontsize #, color='blue'
        , rotation=rotation
        , transform=ax.transAxes)
    txt.set_alpha(alpha)
    return txt

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
    if ax is None: ax = plt.gca()
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
        line.set_marker(wmc_default_markers[ax.markerindex])
        ax.markerindex += 1
        line.set_markeredgecolor(c)
        if filled:
            line.set_markerfacecolor(c)
        else:
            line.set_markerfacecolor('None')
        line.set_markevery(np.max((int(numpoints / N),1)))
        plt.draw()

def add_arrow(meas, line, start_ind, xseries, yseries
    , direction='right', ndirection=15, size=20
    , ax=None, arrowstyle='->', color=None):
    """
    add an arrow to a line.

    meas:       measurement object
    line:       Line2D object
    start_ind:  start index in time series
    xseries:    label of time series for x-axis in measurement object
    yseries:    label of time series for y-axis in measurement object
    direction:  'left' or 'right'
    ndirection: number of datapoints to determine the direction
    size:       size of the arrow in fontsize points
    arrowstyle: style of the arrow
    color:      if None, line color is taken.
    """
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = line.get_color()
    xdata = meas[xseries]
    ydata = meas[yseries]
    if direction == 'right':
        end_ind = start_ind + ndirection
    else:
        end_ind = start_ind - ndirection
    ax.annotate('',
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle=arrowstyle, color=color),
        size=size)
        
def plots_from_excel_list(inData,inExcelFileName,inTargetDir, 
                          testname='testname',inOptions='', inMask=None, extraComment=''):
    """
    Generates plots defined in a special formatted excel file.
    It also generates a MS-Word VBA script to import the generated
    plots into a word document.
    
    Arguments:
        *inData*:
            wmc_data object
    
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
            * 't' - make legends transparant
            
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
    bTransparantLegend = 't' in inOptions
    
    # set mask to True if not given
    if inMask is None:
        inMask = np.ones(inData.Npnt,dtype=bool)

    if (bVerbose): print("[plots_from_excel_list] file:",inExcelFileName)
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
            print(k,':',v)

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
    if bVerbose: print('sh_plots.nrows: ',sh_plots.nrows)
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
            if bVerbose: print('plot :',filename)
            
            # check for 2nd plot
            bDualPlot = (sh_plots.cell(i, col_x2_sig).ctype == XL_CELL_TEXT)
            
            # start the plot
            plt.figure()
            if bDualPlot: plt.axes((0.1,0.1,0.37,0.85))
            
            # y signal prefix ( '_A', '_R', ''
            y_prefix = (str(sh_plots.cell(i, col_y_prefix ).value)).strip()
            x_sig    = (str(sh_plots.cell(i, col_x1_sig   ).value)).strip()
            
            if group not in plot_signals.keys():
                raise(ValueError('group number '+str(group)+' not in signals'))
                
            for y_sig in plot_signals[group]:
                y = y_prefix + y_sig[0]
                x = x_sig
                if not (y_sig[1] == ''): x = y_sig[1] # alt x-axis 1
                if bVerbose: print('plot: ',x,y)
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
                leg = plt.legend(loc=int(sh_plots.cell(i, col_legend1 ).value))
                legend_label_colors()
                if bTransparantLegend:
                    leg.get_frame().set_alpha(0.65)

            # write plot comment
            comment = testname + ' | '
            if extraComment != '': comment += extraComment + ' | '
            comment += str(sh_plots.cell(i, col_remark ).value) + ' | ' 
            comment += filename
            plotcomment(comment)

            # if neccesary 2nd plot
            if bDualPlot:
                
                if bVerbose: print('2nd plot')
                #plt.subplot(122)
                plt.axes((0.6,0.1,0.37,0.85))
                
                # y signal prefix ( '_A', '_R', ''
                y_prefix = str(sh_plots.cell(i, col_y_prefix ).value)
                x_sig    = str(sh_plots.cell(i, col_x2_sig   ).value)
                
                for y_sig in plot_signals[group]:
                    y = y_prefix + y_sig[0]
                    x = x_sig
                    if not (y_sig[2] == ''): x = y_sig[2] # alt x-axis 2
                    if bVerbose: print('plot: ',x,y)
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
                    leg = plt.legend(loc=int(sh_plots.cell(i, col_legend2 ).value))
                    legend_label_colors()
                    if bTransparantLegend:
                        leg.get_frame().set_alpha(0.65)

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
        raise(ValueError('no space available below lowest axes'))
    
    #create lists with coordinates and dimensions for new axes
    height = ((top - bottom) - (rows - 1) * hspace)/rows
    bottoms = [(bottom + i * (height + hspace)) for i in range(rows)]
    width = (rcwidth - (cols-1) * wspace)/cols
    lefts = [(rcleft + i * (width + wspace)) for i in range(cols)]
    
    #return a list of axes instances
    return [plt.axes([lefts[j],bottoms[i], width, height]) for i in range(rows-1,-1,-1) for j in range(cols) ]   



# ==== WMClib Calculation Functions =================================
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

        a = wmc.Parameter(1)
        b = wmc.Parameter(1)
        c = wmc.Parameter(1)

        def f(x):
            return a() * x **2 + b() * x + c()

        wmc.fit(f, [a,b,c], data_y, data_x)
    
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
        raise(ValueError("smooth only accepts 1 dimension arrays."))

    if x.size < window_len:
        raise(ValueError("Input vector needs to be bigger than window size."))

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise(ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"))

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
        raise(ValueError("nojump only accepts 1 dimension arrays."))
    
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
        raise(ValueError("skip_after_jump only accepts 1 dimension arrays."))

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
        raise(ValueError("valid_values only accepts 1 dimension arrays."))

    
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
        raise(ValueError("despike only accepts 1 dimension arrays."))
    
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
        raise(ValueError("filtfilt is only accepting 1 dimension arrays."))

    # x must be bigger than edge
    if x.size < edge:
        raise(ValueError("Input vector needs to be bigger than 3 * max(len(a),len(b)."))

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

        print(mins, maxs)

        # plot signal and peaks
        plt.close('all')
        plt.plot(x, y, 'g-')
        plt.plot(x[mins], y[mins], 'bo')
        plt.plot(x[maxs], y[maxs], 'ro')

    """
    
    # sanity check on `x`
    if (not type(x) is np.ndarray) or len(x.shape) != 1 or len(x) < 2 :
        raise(ValueError('a should be 1D numpy ndarray with length >= 2'))

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

def sort_wmc_data(inList, verbose=False):
    '''
    :purpose: sort a list of wmc_data objects
    '''
    orderbytime = True
    for meas in inList:
        if not ('unixtime' in meas.__dict__):
            # no WMCS file, so not ordered by time
            orderbytime = False
    
    asorted = []
    if verbose:
        if orderbytime:
            print('sort in order of field "unixtime"')
        else:
            print('sort in order of appearance')

    dct = {}
    
    for i, meas in enumerate(inList):
        if meas.Npnt > 0:
            if orderbytime:
                key = (meas.unixtime[0], meas.unixtime[-1])
            else:
                key = i
            dct[key] = meas
        else:
            print('File "%s" neglected: no points'%(
                os.path.split(meas.file_name)[1]))
    asorted = []
    for key in sorted(dct.keys()):
        asorted.append(dct[key])
    if verbose:
        print('appended in the following order')
        for meas in asorted:
            print(os.path.split(meas.file_name)[1])
    return asorted
    
def append_wmc_data(inList, verbose=False):
    """
    Appends multiple wmc_data objects, and returns a new wmc_data object
    """
    if (len(inList)<1) and verbose:
        print('No objects given (%d<1)'%(len(inList)))
        return wmc_data()
    
    asorted = sort_wmc_data(inList, verbose=verbose)
    Npnt = 0
    for part in asorted:
        Npnt += part.Npnt
    wd = wmc_data(Npnt)
    if Npnt == 0:
        print('No points found in %d files'%(len(inList)))
        return wd
    elif verbose:
        print('%d points found in %d files'%(Npnt, len(inList)))
        
    meas = asorted[0]
    pth, flnm = os.path.split(meas.file_name)
    wd.file_name = os.path.join(pth, 'appended_%s'%flnm)
    wd.channels = meas.channels
    wd.fields = meas.fields
    
    index = 0
    for icmp, part in enumerate(asorted[1:]):
        msg = part.channels.compare(asorted[icmp].channels)
        if len(msg) > 0:
            msg1 = 'WARNING: channels changed'
            files = []
            chnls = []
            addedorremoved = False
            for i in range(icmp, icmp+2):
                pth, flnm = os.path.split(asorted[i].file_name)
                files.append(flnm)
                chnls.append(asorted[i].channels)
            msg1 += ' from file "%s" to "%s"'%(files[0], files[1])
            print(msg1)
            print(msg)
            
    for part in asorted:
        for chn in part:
            if not chn in wd:
                dtype = part[chn].dtype
                if dtype==np.float64:
                    wd[chn] = nans((Npnt,),dtype=dtype)
                else:
                    wd[chn] = np.zeros((Npnt,),dtype=dtype)
            wd[chn][index:index + part.Npnt] = part[chn]
        index += part.Npnt
    if verbose:
        print('Change record number')
    wd['record'] = np.arange(Npnt)
    if 'unixtime' in wd:
        if verbose:
            print('Change test time')
        wd['testtime'] = wd['unixtime'] - wd['unixtime'][0]
    return wd

def join_wmc_data(inList):
    """
    Join multiple wmc_data objects from multiple stations
    
    Channels from different wmc_data objects are taken
    Minimum length is taken
    """
    if (len(inList)<1):
        raise(ValueError('no objects given'))

    min_len = 99999999;
    for part in inList:
        min_len = min(min_len,part.Npnt)
        
    wd = wmc_data(min_len)
    
    for part in inList:
        for chn in part:
            wd[chn] = deepcopy(part[chn][0:min_len])
    return wd

class equipment:
    def __init__(self, label, type, WMCnumber=-1):
        self.label = label
        self.type = type
        self.WMCnumber = WMCnumber
        
# ==== WMClib Ambient temperature function ==========================
# ===================================================================

def ambient_temp(location, *args, **kwargs):
    '''
    retrieve the readings from out 'wheater stations'.
    
    Arguments:
        *location*:
            'hal', 'minilab', 'lamineerruimte'
            
        second and optionally third argument can be:
            - a wmc_data object from a WMCS measurement file
            - one or two times expressed as datetime object or an
              list/tuple with the arguments for datetime or a 
              unixtime(float, int) value
    
    The result is returned as a wmc_data object which by convention is
    mostly called 'measT'.
    '''
    
    # local help function
    def try_make_date(arg):
        if isinstance(arg, datetime.datetime):
            return arg
        elif (isinstance(arg, float) or
            isinstance(arg, long) or
            isinstance(arg, int) ) :
            return datetime.datetime.fromtimestamp(arg)
        elif (isinstance(arg, list) or
              isinstance(arg, tuple)) :
            return datetime.datetime(*arg)
        else:
            raise(ValueError('Could not create date from' + repr(arg)))
    
    # figure out second and third argument
    meas = None
    single = False
    if len(args) >= 1 and isinstance(args[0], wmc_data):
        meas = args[0]
        if len(args) >= 2:
            extra_seconds = int(args[1])
        else:
            extra_seconds = 0
        start_date = datetime.datetime.fromtimestamp(meas['unixtime'][0]-extra_seconds)
        stop_date = datetime.datetime.fromtimestamp(meas['unixtime'][-1]+extra_seconds)
    else:
        if len(args) == 1:
            start_date = try_make_date(args[0])
            stop_date = start_date
            single = True
        elif len(args) == 2:
            start_date = try_make_date(args[0])
            stop_date = try_make_date(args[1])
        else:
            raise(ValueError('Too much or too less arguments'))
        
    data = wmclibdata.ambient_temp(location, start_date, stop_date)
    
    # store results in a wmc_data object
    measT = wmc_data(len(data[data.keys()[0]]))
    for label in data:
        measT[label] = data[label]
    # create unixtime channel
    measT['unixtime'] = np.zeros_like(measT.temperature)
    for i in range(measT.Npnt):
        measT['unixtime'][i] = measT['log_date'][i]
        
    # create testtime channel
    offset = 0.0
    if meas:
        offset = measT['unixtime'][0] - meas['unixtime'][0]
    measT['testtime'] = measT['unixtime'] - measT['unixtime'][0] + offset
    
    # check single, return only 1 point
    if single:
        mask = np.zeros(measT.Npnt, dtype=np.bool)
        mask[0] = True
        measT = measT.masked_copy(mask)
    
    return measT

# ==== WMClib Ambient temperature function ==========================
# ===================================================================

def get_factor_straingauge(gauge_factor, device='hbmd'):
    '''
    :purpose: obtain the calculation factor analogous the table gauge_factor
        in the coupon database
    
    :details: brute force. 
        If table changes in coupon database, change this table.
    '''
    tbl = {'hbm':{2.06:1.185149
                , 2.07: 1.179423
                , 2.08: 1.173753
                , 2.09: 1.168137
                , 2.1: 1.162574
                , 2.11: 1.157065
                , 2.12: 1.151607
                , 2.13: 1.1462
                , 2.14: 1.140844
                , 2.15: 0}
            , "hbmd":{2.06: 0.0202265
                , 2.07: 0.0201288
                , 2.08: 0.0200321
                , 2.09: 0.0199362
                , 2.1: 0.0198413
                , 2.11: 0.0197472
                , 2.12: 0.0196541
                , 2.13: 0.0195618
                , 2.14: 0.0194704}
            , "voorsluis":{2.06: 0.5925749
                , 2.07: 0.5897123
                , 2.08: 0.5868771
                , 2.09: 0.5840691
                , 2.1: 0.5812878
                , 2.11: 0.5785329
                , 2.12: 0.575804
                , 2.13: 0.5731007
                , 2.14: 0.5704226
                , 2.15: 0.5677695}
            }
    return tbl[device][gauge_factor]
    

# ==== WMClib Blade Specific Functions ==============================
# ===================================================================

#   

# ==== WMClib Geometrical Functions =================================
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
    if (lp1.shape[-1] != 2): raise(ValueError("lp1 contains no 2D points"))
    if (lp2.shape[-1] != 2): raise(ValueError("lp2 contains no 2D points"))
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
    if (lp1.shape[-1] != 2): raise(ValueError("lp1 contains no 2D points"))
    if (lp2.shape[-1] != 2): raise(ValueError("lp2 contains no 2D points"))
    if (lp3.shape[-1] != 2): raise(ValueError("lp3 contains no 2D points"))
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
    if (lp1.shape[-1] != 2): raise(ValueError("lp1 contains no 2D points"))
    if (lp2.shape[-1] != 2): raise(ValueError("lp2 contains no 2D points"))

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
    if (lp1.shape[-1] != 2): raise(ValueError("lp1 contains no 2D points"))
    if (lp2.shape[-1] != 2): raise(ValueError("lp2 contains no 2D points"))
    if ( lc.shape[-1] != 2): raise(ValueError("lc  contains no 2D points"))
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
    if (lp1.shape[-1] != 2): raise(ValueError("lp1 contains no 2D points"))
    if (lp2.shape[-1] != 2): raise(ValueError("lp2 contains no 2D points"))
    if ( lc.shape[-1] != 2): raise(ValueError("lc  contains no 2D points"))
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
    if (lp1.shape[-1] != 3): raise(ValueError("lp1 contains no 3D points"))
    if (lp2.shape[-1] != 3): raise(ValueError("lp2 contains no 3D points"))
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
    if (lp1.shape[-1] != 3): raise(ValueError("lp1 contains no 3D points"))
    if (lp2.shape[-1] != 3): raise(ValueError("lp2 contains no 3D points"))
    if (lp3.shape[-1] != 3): raise(ValueError("lp3 contains no 3D points"))
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

    inMeasurement       - wmc_data object with the measurement
    inInstall_Dat       - wmc_data object with the install.dat measurement
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
                    
    raise(ValueError("need 2 or 3 wire labels to calculate displacements" ))

def geom_3D_displacements_from_wire_transducers_plane(inMeasurement,
                                                      inInstall_Dat,
                                                      inTransduc_Set,
                                                      inWireLabelList,
                                                      plane_def_vec):
    """
    returns array of 3D displacements with respects to the
    install.dat point based on the length changes of the two or three
    wiretransducers, given the measurement and install info

    inMeasurement       - wmc_data object with the measurement
    inInstall_Dat       - wmc_data object with the install.dat measurement
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
                    
    raise(ValueError("need 2 or 3 wire labels to calculate displacements" ))


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
    inMeasurement       - wmc_data object with the measurement
    inInstall_Dat       - wmc_data object with the install.dat measurement
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
            wmc_data object with the measurement

        *inInstall_Dat*:
            wmc_data object with the install.dat measurement

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
            wmc_data object with the measurement

        *inInstall_Dat*:
            wmc_data object with the install.dat measurement

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
        raise(ValueError('plane_def_vec should have shape (3,)'))
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


# ==== WMClib bolt calculations  ====================================
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
    
class channel:
    '''
    :purpose: obtain data from channel name using WMC conventions
    '''
    
    def __init__(self, channelname):
        self.channel = channelname.strip()
        ''' channel id '''
        self.channeltype = None
        ''' type of the channel '''
        self.quantity = ''
        ''' measured quantity '''
        self.unit = ''
        ''' unit '''
        self.displayname = ''
        ''' displayname '''
        self.number = -1
        ''' number of the channel '''
        
        lenchannel = len(self.channel)
        if self.channel == 'record':
            self.unit = '-'
            self.quantity = self.channel
            self.displayname = self.channel
        elif self.channel in ['testtime']:
            self.unit = 's'
            self.quantity = 'Time'
            self.displayname = 'Test time'
        elif (lenchannel > 3) and (self.channel[:2] in ['RH'
            , 'CG', 'SL', 'SO', 'WE'
            , 'DT'
            , 'AX', 'AY'
            , 'LO'
            , 'BA'
            ]):
            try:
                self.number = int(self.channel[2:])
            except:
                return
            self.channeltype = self.channel[:2]
            if self.channeltype == 'RH':
                self.unit = '%'
                self.quantity = 'Relative humidity'
            elif self.channeltype in ['CG', 'SL', 'SO', 'WE'] :
                self.unit = 'mm'
                self.quantity = 'Extension'
            elif self.channeltype in ['DT'] :
                self.unit = 'mm'
                self.quantity = 'Displacement'
            elif self.channeltype in ['AX', 'AY'] :
                self.unit = u'\u00B0'
                self.quantity = 'Angle'
                self.axis = self.channeltype[1]
                ''' rotation axis '''
            elif self.channeltype in ['LO'] :
                self.unit = 'kN'
                self.quantity = 'Force'
            elif self.channeltype in ['BA'] :
                self.unit = 'mu'
                self.quantity = 'Bolt axial strain'
            self.displayname = '%s %d'%(self.quantity, self.number)
        elif (lenchannel > 2) and self.channel[0] in ['F', 'S', 'T']:
            # force, displacement, or temperature
            try:
                self.number = int(self.channel[1:])
            except:
                return None
            self.channeltype = self.channel[0]
            if self.channeltype == 'F':
                self.unit = 'kN'
                self.quantity = 'Force'
            elif self.channeltype == 'S':
                self.unit = 'mm'
                self.quantity = 'Displacement'
            elif self.channeltype == 'T':
                self.unit = u'\u00B0C'
                self.quantity = 'Temperature'
            self.displayname = '%s %d'%(self.quantity, self.number)
        elif (lenchannel==7) and (self.channel[3] in ['S', 'C', 'R']):
            try:
                self.number = int(self.channel[:3])
                self.angle = float(self.channel[4:])
            except:
                return None
            self.channeltype = 'SG'
            self.subtype = self.channel[3]
            self.unit = 'mu'
            self.quantity = 'Strain'
            self.displayname = '%s %d'%(self.quantity, self.number)
            if (not  (self.subtype == 'S')) or (np.abs(self.angle)> 0.5):
                self.displayname += ' %g \u00B0C'%(self.angle)
        elif (lenchannel==6) and (self.channel[:2] in ['BB']):
            try:
                self.number = int(self.channel[2:4])
                self.subnumber = float(self.channel[5])
            except:
                return None
            self.channeltype = self.channel[:2]
            self.subtype = self.channel[3]
            self.unit = 'mu'
            self.quantity = 'Strain'
            self.displayname = '%s %d'%(self.quantity, self.number)
        if len(self.displayname) == 0:
            self.displayname = self.quantity
    
    def mapped(self, meas):
        '''
        :purpose: create a mapped channel with unit and current displayname
        '''
        return mapped_channel(meas, self.channel
            , columnname=self.displayname
            , unit=self.unit)
        
    def __str__(self):
        s = '== channel "%s" (%s)'%(self.channel, self.displayname)
        s += '\n=  %s [%s]'%(self.quantity, self.unit)
        s += '\n=='
        return s

def load_from_sql(sql_columns, sql_from
    , sql_select = 'SELECT'
    , sql_args = None
    , columnmapping = None
    , date_columns = None
    , host = wmclibdata.sql_host
    , database = wmclibdata.sql_default_database
    , user     = wmclibdata.sql_user
    , password = wmclibdata.sql_password
    , port     = wmclibdata.sql_port):
    '''
    :purpose: wmc_data object from sql query
    
    :param list sql_columns: list of columns in SQL table (or stored procedure)
    :param str sql_from: part of the query after columns, usually starting
        with 'FROM'
    :param str sql_select: part of the query after columns, usually 'SELECT'
    :param list sql_args: list of arguments in query
    :param dict columnmapping: mapping of sql-columns to columns in 
        wmc_data object
    :param list date_columns: list of columns in wmc_data object 
        containing dates
    :param str host: IP-address of computer, where database is located
    :param str database: database name
    :param str user: user name for database connection
    :param str password: password for database connection
    :param str port: port number for database connection
    
    :remarks: database connection properties defined in wmclibdata
    
    example::
    
        import wmclib as wmc
        import datetime

        cols = ['log_date', 'temperature', 'humidity', 'pressure', 'dewpoint']
        sql_args = [datetime.datetime(2018,2,1)]
        sql_from = ' FROM hal WHERE log_date >= %s ORDER BY log_date ASC '
        measT = wmc.load_from_sql(sql_columns = cols
            , sql_args=sql_args
            , sql_from=sql_from)
        plt.plot(measT.unixtime, measT.temperature)
        plt.plot(measT.log_date, measT.temperature)

    
    '''
    import psycopg2
    
    datecols = []
    if date_columns is not None:
        datecols = date_columns
    colmapping = {}
    if columnmapping is not None:
        colmapping = columnmapping
    # local help function
    def try_make_date(arg):
        if isinstance(arg, datetime.datetime):
            return arg
        elif (isinstance(arg, float) or
            isinstance(arg, long) or
            isinstance(arg, int) ) :
            return datetime.datetime.fromtimestamp(arg)
        elif (isinstance(arg, list) or
              isinstance(arg, tuple)) :
            return datetime.datetime(*arg)
        else:
            raise(ValueError('Could not create date from' + repr(arg)))
    

    sql  = ' %s %s %s'%(sql_select, ', '.join(sql_columns), sql_from)
    conn = psycopg2.connect(
        host     = host,
        database = database,
        user     = user, 
        password = password,
        port     = port)
    cur = conn.cursor()

    # and retrieve the data, and make a nice (transposed) numpy array
    if sql_args is None:
        cur.execute(sql)
    else:
        cur.execute(sql, sql_args)
    db_data = np.asarray(cur.fetchall())
    cur.close()
    conn.close()
    
    # instantiate wmc_data object with right length
    nrec = len(db_data)
    meas = wmc_data(nrec)
    db_data = db_data.transpose()
    for i, col in enumerate(db_data):
        label = sql_columns[i]
        if label in colmapping:
            label = colmapping[label]
        if label in datecols:
            # convert to double
            meas[label] = np.zeros(nrec)
            for j in range(nrec):
                x = db_data[i][j]
                meas[label][j] = time.mktime(x.timetuple())
        else:
            meas[label] = db_data[i]
            
    # store results in a wmc_data object
    # create columns unixtime and testtime, if there is a column with dates
    if len(datecols) > 0:
        # create unixtime channel
        meas['unixtime'] = np.array(meas[datecols[0]])
            
        # create testtime channel
        meas['testtime'] = meas['unixtime'] - meas['unixtime'][0]
        
    return meas


# ==== WMClib experimental functions=================================
# ===================================================================


def glps(axis = None):
    """
    Experimental function to place text labels near the plots
    instead of using a legend.
    """
    
    if axis is None:
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

def strain_matrix_from_rosette(alpha=0.0, beta=45.0, gamma=45.0):
    '''
    :purpose: calculate matrix for transformation of rosette strains to
        x, y and xy direction
    
    :citation: 
        <http://www.efunda.com/formulae/solid_mechanics/mat_mechanics/strain_gage_rosette.cfm>
    
    .. math::
    
        \epsilon_{i} = \epsilon_{x} \\frac{1}{2} \\left( 1 + \cos 2 \\alpha_{i} \\right)
        + \epsilon_{y} \\frac{1}{2} \\left( 1 - \cos 2 \\alpha_{i} \\right)
        + \epsilon_{xy} \sin 2 \\alpha_{i}
        
    '''
    angles = np.array([alpha, alpha+beta, alpha+beta+gamma])
    angles *= 2.0 * np.pi / 180.
    
    c = np.cos(angles)
    s = np.sin(angles)
    return np.linalg.inv([[0.5*(1+c[0]), 0.5 * (1-c[0]), s[0]]
        , [0.5*(1+c[1]), 0.5 * (1-c[1]), s[1]]
        , [0.5*(1+c[2]), 0.5 * (1-c[2]), s[2]]])
        
def strain_from_rosette0(meas, sgname0, sgname45, sgname135):
    '''
    :purpose: obtain strains in main directions x, y, and xy for rosette with 
        x in direction of 'centre' strain gauge
        A: -45, B: 0, C: +45
        
    :details: for engineering strain (gamma) you have to multiply 
        the epsilon_xy by 2
    '''
    epsilon_x = meas[sgname0]
    epsilon_y = meas[sgname135]+meas[sgname45]-epsilon_x
    epsilon_xy = 0.5 *(meas[sgname45]-meas[sgname135])
    return epsilon_x, epsilon_y, epsilon_xy
    
def strain_from_rosette90(meas, sgname90, sgname45, sgname135):
    '''
    :purpose: obtain strains in main directions x, y, and xy for rosette with 
        y in direction of 'centre' strain gauge
        A: 45, B: 90, C: 135
        
    :details: for engineering strain (gamma) you have to multiply 
        the epsilon_xy by 2
    '''
    epsilon_y = meas[sgname90]
    epsilon_x = meas[sgname135]+meas[sgname45]-epsilon_y
    epsilon_xy = 0.5 *(meas[sgname45]-meas[sgname135])
    return epsilon_x, epsilon_y, epsilon_xy
    
def plateau_actuator(number, target, plamin, wmin, emin, fmin=0.0
    , plamax='min', wmax='min', emax='min'):
    '''
    :purpose: create actuator in a test with plateaus
        
    :param number: number of the actuator
    :param target: final target (force), a series can be defined by 
    :param plamin: acceptable deviation below plateau target
    :param plamax: acceptable deviation above plateau target (default = plamin)
    :param wmin: deviation where controller stops changing other actuators
        i.e. if measured signal for actuator F02 < function generator signal
        FG02 - wmin, the function generator signal for F01 is constant
    :param wmax: analogous to wmin, but if measured signal is too large
    :param emin: deviation where controller stops the test
        i.e. if measured signal for actuator F02 < function generator signal
        FG02 - wmin, the test stops
    :param fmin: minimum force for this actuator, in many cases it is not
        possible to obtain zero force
    :param emax: analogous to emin, but if measured signal is too large
    '''
    dct = {'number': number
        , 'target': target
        , 'plamin': plamin
        , 'wmin': wmin
        , 'emin': emin
        , 'fmin': np.abs(fmin)}
    if plamax == 'min':
        dct['plamax'] = float(plamin)
    else:
        dct['plamax'] = float(plamax)
            
    if wmax == 'min':
        dct['wmax'] = float(wmin)
    else:
        dct['wmax'] = float(wmax)
    if emax == 'min':
        dct['emax'] = float(emin)
    else:
        dct['emax'] = float(emax)
    return dct
        
class targetplateaus:
    '''
    :purpose: define the plateaus in a test
    
    example::
    
        # two actuators
        actuators = []
        targets = [16,5] # kN
        pla = 0.5 # kN
        w = 1 # kN
        e = 4 # kN
        for i, tgt in enumerate(targets):
            actuators.append(plateau_actuator(i+1, target=tgt
                , plamin=pla, wmin=w, emin=e)

        plateaus = wmc.targetplateaus(actuators, name='mytune')
        for i in range(3):
            plateaus.addplateau(factor=float(i+1)*0.2, plateautime=1.0)
        plateaus.addplateau(factor=0.8)
        plateaus.addplateau(factor=1.02, plateautime=1.0)
        plateaus.changeactuator(1, plamin=0.1)
        plateaus.write()
    '''
    
    status_invalid = -1
    status_noplateau = 0
    status_inplateau = 1
    status_entering_plateau = 2
    status_leaving_plateau = 3
    precision_fg_signal = 0.0001
    
    def __init__(self, actuators=None, name='tune', defaulttime=10.0):
        self.name = name
        ''' name of the set of plateaus '''
        self.defaulttime = float(defaulttime)
        ''' default time of a plateau '''
        self.plateaus = []
        ''' list of plateaus '''
        self.actuators = {}
        ''' dictionary of actuators '''
        self.keys = []
        self._actuators_from_array(actuators)
       
    def _actuators_from_array(self, actuators):
        if actuators is not None:
            self.actuators = self._actuators_array2dict(actuators)
            self.keys = sorted(self.actuators.keys())
        
    def _actuators_array2dict(self, actuators):
        dct = {}
        if actuators is not None:
            for act in actuators:
                dct[act['number']] = act
        return dct
        
    def addplateau(self, factor, plateautime='default'
        , addpla=False):
        '''
        :purpose: add plateau where all actuator signals are multiplied
            by the given factor
        
        :param factor: factor

        :param plateautime: time the plateau should last,
            if -1, take the default time

        :param addpla: add plamin for positive values and -plamax for negative

        '''
        targets = []
        for key in self.keys:
            act = self.actuators[key]
            tgt = act['target']
            val = factor*tgt
            if addpla:
                if val > 0.0:
                    val += act['plamin']
                elif val < 0.0:
                    val -= act['plamax']
                elif tgt > 0.0:
                    # factor is zero but target > 0.0
                    val += act['plamin']
                elif tgt < 0.0:
                    val -= act['plamax']
            # act['fmin'] is always positive or zero
            if np.abs(val) < act['fmin']:
                val = act['fmin']
                if tgt < 0.0:
                    val *= -1.
                if factor < 0.0:
                    val *= -1.
            targets.append(val)
        self.addplateautargets(targets, plateautime)
        
    def addplateautargets(self, targets, plateautime='default'):
        '''
        :purpose: add plateau with a list of target (forces)
        
        :param targets: values of the target signals,
                number of targets should match number of actuators
        :param plateautime: time the plateau should last,
            if -1, take the default time
        '''
        if len(targets) != len(self.keys):
            raise(ValueError(
                'Number of given targets (%d) should match %d actuators'%(
                len(targets), len(self.keys))))
        if plateautime == 'default':
            tm = self.defaulttime
        else:
            tm = float(plateautime)
        actuators = deepcopy(self.actuators)
        for i, key in enumerate(self.keys):
            actuators[key]['target'] = targets[i]
        self.plateaus.append({'time':tm, 'actuators':actuators})
        
    def changeactuator(self, actuator, step='last', target='default'
        , plamin='default', wmin='default', emin='default'
        , plamax='default', wmax='default', emax='default'):
        '''
        :purpose: change specific values for an actuator in one of the steps
        
        :param step: number of the step, if 'last', take the last step
        '''
        if step == 'last':
            istep = len(self.plateaus) - 1
        else:
            istep = int(step)
        if istep >= len(self.plateaus):
            raise(ValueError(
                'plateau number (%d) >= total number of plateaus (%d)'%(
                istep, len(self.plateaus))))
        if not (target == 'default'):
            self.plateaus[istep]['actuators'][actuator]['target'] = \
            float(target)
        if not (plamin == 'default'):
            self.plateaus[istep]['actuators'][actuator]['plamin'] = \
            float(plamin)
        if not (plamax == 'default'):
            self.plateaus[istep]['actuators'][actuator]['plamax'] = \
            float(plamax)
        if not (wmin == 'default'):
            self.plateaus[istep]['actuators'][actuator]['wmin'] = float(wmin)
        if not (wmax == 'default'):
            self.plateaus[istep]['actuators'][actuator]['wmax'] = float(wmax)
        if not (emin == 'default'):
            self.plateaus[istep]['actuators'][actuator]['emin'] = float(emin)
        if not (emax == 'default'):
            self.plateaus[istep]['actuators'][actuator]['emax'] = float(emax)
        
    def save(self, folder='.'):
        '''
        :purpose: 
        '''
        istep = len(self.plateaus) - 1

        pth = os.path.join(folder, '%s.plateau'%self.name)
        with open(pth, 'w') as f:
            f.write('#      time')
            for k in self.keys:
                f.write('       act%d'%k)
                for s in ['pla', 'w', 'e']:
                    for m in ['min', 'max']:
                        f.write(('%s%s%d'%(s,m,k)).rjust(11))
            for i, p in enumerate(self.plateaus):
                f.write('\n %10g'%(p['time']))
                for k in self.keys:
                    act = p['actuators'][k]
                    f.write(' %10g'%act['target'])
                    for s in ['pla', 'w', 'e']:
                        for m in ['min', 'max']:
                            colkey = '%s%s'%(s,m)
                            f.write(' %10g'%act[colkey])
            f.close()

    def load(self, path, factortarget=1.0):
        '''
        :purpose: read object targetplateaus from file
        
        :param path: file path
        :param factortarget: maximum target is determined and divided
            by this factor
        '''
        if not os.path.exists(path):
            print('File "%s" does not exist'%path)
            return
        print('Reading file "%s"'%path)
        with open(path, 'r') as f:
            # maximum signal up to now
            maxtotaltarget = 0.0
            n_act = -1
            s = f.readline() # header
            s = f.readline()
            while len(s) > 0:
                a = s.strip().split()
                tm = float(a[0])
                n_act = int((len(a) -1)/7)
                actuators = []
                # for determining step with largest target signal
                totaltarget = 0.0
                for i in range(n_act):
                    offset = 1 + i * 7
                    target = float(a[offset])
                    totaltarget += np.abs(target)
                    plamin = float(a[offset + 1])
                    plamax = float(a[offset + 2])
                    wmin = float(a[offset + 3])
                    wmax = float(a[offset + 4])
                    emin = float(a[offset + 5])
                    emax = float(a[offset + 6])
                    number = len(actuators) + 1
                    actuators.append(plateau_actuator(number=number
                        , target=target, plamin=plamin, wmin=wmin
                        , emin=emin, plamax=plamax, wmax=wmax, emax=emax))
                
                if len(self.keys) == 0:
                    maxtotaltarget = totaltarget
                    self._actuators_from_array(actuators)
                
                self.plateaus.append({'time':tm
                    , 'actuators':
                        deepcopy(self._actuators_array2dict(actuators))})
                if totaltarget > maxtotaltarget:
                    maxtotaltarget = totaltarget 
                    for act in actuators:
                        key = act['number']
                        self.actuators[key]['target'] = \
                            act['target']/factortarget
                s = f.readline()
            f.close()
    
    def generatetimeseries(self, plateau_speed=0.2):
        '''
        :purpose: generate time series of a test based on plateau file
        
        :param plateau_speed: 
        '''
        dct = {'time':[], 'actuators': {}}
        for key in self.keys:
            dct['actuators'][key] = {
                'target':[], 'targetmin':[], 'targetplus':[]}
        tm = 0.0 # current time
        for i, p in enumerate(self.plateaus):
            dsignal = 0.0 # maximum difference with next plateau
            for key in self.keys:
                tgt = p['actuators'][key]['target']
                if i < len(self.plateaus)-1:
                    tgtnext = self.plateaus[i+1]['actuators'][key]['target']
                    dsignal = np.max([np.abs(tgt-tgtnext), dsignal])
                tgtplus = tgt + p['actuators'][key]['plamax']
                tgtmin = tgt - p['actuators'][key]['plamin']
                for j in range(2):
                    dct['actuators'][key]['target'].append(tgt)
                    dct['actuators'][key]['targetplus'].append(tgtplus)
                    dct['actuators'][key]['targetmin'].append(tgtmin)
            
            dct['time'].append(tm)
            tm += p['time']
            dct['time'].append(tm)
            tm += (dsignal / plateau_speed)
        return dct
    
    def createfilters(self, meas, fg_channels, timeprecision=0.01):
        '''
        :purpose: create filters for plateaus on measured WMCS data
        
        :details: 
            fltrs = plateaus.createfilters(meas, 
                fg_channels={1:{'fg':'FG01', 'fb':'F01'}
                    1: {'fg':'FG01', 'fb':'F01'}})
            
            meas['signal'][fltrs[3]] gives signal during plateau 3
                
            function generator information can be obtained from 
                wmcs.conf and channels.set 
        '''
        a = []
        allTrue = []
        for i in range(meas.Npnt):
            allTrue.append(True)
        allTrue = np.array(allTrue)
        for i_p, p in enumerate(self.plateaus):
            x = np.ones_like(allTrue)
            for chnl in fg_channels:
                # initialize with False
                dct = p['actuators'][chnl]
                tgt = dct['target']
                tgtmin = tgt - dct['plamin']
                tgtmax = tgt + dct['plamax']
                fg = meas[fg_channels[chnl]['fg']]
                fb = meas[fg_channels[chnl]['fb']]
                # for this channel the fg-signal must equal the target
                # and the feedback signal must be close
                x = x \
                    & (np.abs(fg-tgt) < self.precision_fg_signal) \
                    & (fb <= tgtmax) & (fb >= tgtmin)
            a.append(x)
        imaxlast = -1 # end of last plateau
        dct = {}
        for i_p, x in enumerate(a):
            p = self.plateaus[i_p]
            # exclude all previously found plateaus
            x = x & (meas['record'] > imaxlast) 
            recs = meas['record'][x]
            nxt = True
            # try to find the first plateau, which is at least 99 % of the 
            for i, irec in enumerate(recs):
                if nxt:
                    if i == 0:
                        imin = irec
                    else:
                        if i == (len(recs)-1) or (irec - recs[i-1] > 1):
                            # hole detected or last record
                            if i == (len(recs)-1):
                                imax = recs[i]
                            else:
                                imax = recs[i-1]
                            t0 = meas['testtime'][imin]
                            t1 = meas['testtime'][imax]
                            if t1-t0 > (1-timeprecision) * p['time']:
                                print('plateau %d from %g to %g (%g seconds)'%(
                                    i_p, t0, t1, t1-t0))
                                dct[i_p] = (
                                    (meas['record'] >= imin) 
                                    & (meas['record'] <= imax)
                                    )
                                imaxlast = imax
                                nxt = False
                            imin = irec
        
        return dct

    def __str__(self):
        s = '== target plateaus =='
        s += '\n= name: "%s"'%self.name
        if len(self.keys) == 0:
            s += '\n= no actuators'
        else:
            for key in self.keys:
                act = self.actuators[key]
                s += '\n= actuator %3d target=%6g'%(key, act['target'])
            s += '\n= %d plateaus defined'%(len(self.plateaus))
        s += '\n====================='
        return s

class wmcs_configuration:
    '''
    :purpose: get information from file wmcs.conf
    '''
    mode_displacement = 0
    mode_force = 1
    chnls_int = [
        'device_max',
        'device_min',
        'fatigue_ampcon_channel_A',
        'fatigue_ampcon_channel_B',
        'fatigue_ampcon_channel_ampl',
        'fatigue_ampcon_channel_offs',
        'fatigue_ampcon',
        'fatigue_ampcon_mode',
        'fatigue_start_time',
        'fatigue_stop_target_mode',
        'fatigue_waveform',
        'feedback_channel',
        'fg_action',
        'init_method',
        'mode',
        'slow_cycle_channel_A',
        'slow_cycle_channel_B',
        'static_speed_direction'
        ]
    chnls_float= [
        'adjust_fatigue_amplitude',
        'adjust_fatigue_frequency',
        'adjust_fatigue_offset',
        'device_offset',
        'fatigue_ampcon_ampl_target',
        'fatigue_ampcon_fac',
        'fatigue_ampcon_maximum',
        'fatigue_ampcon_minimum',
        'fatigue_ampcon_offs_target',
        'fatigue_ampcon_offset_fac',
        'fatigue_frequency',
        'fatigue_max',
        'fatigue_min',
        'fatigue_stop_target',
        'move_speed',
        'move_target',
        'points_max_speed',
        'slow_cycle_limit',
        'slow_cycle_mode',
        'slow_cycle_speed',
        'static_speed'
        ]
        
    
    def __init__(self):
        self.__dict__ = {}
    
    def _parse_channel_line(self, a, section):
        a1 =  a[0].split('\\')
        if len(a1) == 3:
            if not ('channels' in self.__dict__[section]):
                self.__dict__[section]['channels'] = {}
            chnl = int(a1[1])
            if not (chnl in self.__dict__[section]['channels']):
                self.__dict__[section]['channels'][chnl] = {
                    self.mode_force:{}
                    , self.mode_displacement:{}}
            mode = -1
            key = a1[2]
            if key.endswith('_D'):
                key = key[:-2]
                mode = self.mode_displacement
            elif key.endswith('_F'):
                key = key[:-2]
                mode = self.mode_force
            else:
                pass
            if key in self.chnls_float:
                val = float(a[1])
            elif key in self.chnls_int:
                val = int(a[1])
            else:
                val = a[1]
            if mode < 0:
                self.__dict__[section]['channels'][chnl][key] = val
            else:
                self.__dict__[section]['channels'][chnl][mode][key] = val
        elif len(a1) == 2:
            if not ('channels' in self.__dict__[section]):
                self.__dict__[section]['channels'] = {}
            if a1[1] in ['size']:
                self.__dict__[section]['channels'][a1[1]] = int(a[1])
            else:
                self.__dict__[section]['channels'][a1[1]] = a[1]
        else:
            print('line "%s" in section "%s" not parsed: %d elements after split on "\\" unexpected'%(
                s,section, len(a)))
    
    def _parse_keyvalline(self, s, section):
        a = s.split('=')
        if len(a) == 2:
            if a[0].startswith('chn\\'):
                self._parse_channel_line(a, section)
            else:
                self.__dict__[section][a[0]] = a[1]
        else:
            print('line "%s" in section "%s" not parsed: %d elements after split on "=" unexpected'%(
                s,section, len(a)))

    def load(self, folder='.'):
        flnm = 'wmcs.conf'
        self.__dict__ = {}
        section = ''
        pth = os.path.join(folder, flnm)
        if not os.path.exists(pth):
            print('WMCS configuration file "%s" not found'%pth)
            return
        print('loading WMCS configuration from "%s"'%pth)
        with open(pth, 'r') as f:
            line = f.readline()
            while len(line) > 0:
                s = line.strip()
                if s.startswith('[') and s.endswith(']'):
                    section = s[1:-1]
                    print('read section "%s"'%section)
                    self.__dict__[section] = {}
                elif '=' in s:
                    self._parse_keyvalline(s, section)
                elif len(s) == 0:
                    pass
                else:
                    print('line "%s" in section "%s" not parsed: %s'%(
                        s, section, 'unexpected format'))
                line = f.readline()
            f.close()
    
    def fg_channel_property(self, chnl, property):
        settings = self.function_generator['channels'][chnl]
        mode = settings['mode']
        return settings[mode][property]

class wmcs_test_data:
    '''
    :purpose: read wmcs output, including channels, et cetera using file
        wmcs.conf
        
    :details: all files are in the given folder
    '''
    
    def __init__(self):
        self.testname = ''
        ''' test name (name of buffer file) '''
        self.plateaufile = ''
        ''' filename of plateau definition '''
        self.meas = None
        ''' wmc_data object '''
        self.datafolder = '.'
        ''' folder with buffer file '''
        self.conf = wmcs_configuration()
        ''' wmcs configuration '''
        self.channels = wmcs_channels()
        ''' channel definition '''
        self.rep_channels = repaired_channels()
        ''' repaired channels '''
        self.plateaus = targetplateaus()
        ''' plateau definition '''
        
    def load(self, folder):
        self.folder = folder
        self.conf.load(folder)
        self.channels.load(folder)
        self.rep_channels.load(folder)
        # obtain channels for function generator
        self.fg_channels = {}
        nr = self.conf.function_generator['channels']['size']
        for i in range(nr):
            key = i+1
            mode = self.conf.function_generator['channels'][key]['mode']
            # function generator channel number obtained from channels.set
            ifg = self.channels.fg_channels[i]
            # feedback channel number obtained from wmcs.conf
            ifb = self.conf.fg_channel_property(key, 'feedback_channel')
            self.fg_channels[key] = {'fg':self.channels.channels[ifg]['label']
                , 'fb': self.channels.channels[ifb]['label']
                }
        self.testname = self.conf.hardware['test_name']
        self.plateaufile = os.path.split(self.conf.plateau['plateau_file'])[1]
        self.plateaus.load(self.plateaufile)
        if len(self.datafolder) == 0:
            self.datafolder = self.folder
        path = os.path.join(self.datafolder, '%s.buffer'%self.testname)
        if not os.path.exists(path):
            print('WMCS output file "%s" not found'%path)
            return
        self.meas = load_wmcs(path, rep_channels=self.rep_channels)
        
class wmc_data_field:
    '''
    :purpose: field in test output
    '''
    fieldtype_time = 0
    ''' the one and only time signal '''
    fieldtype_channel_signal = 1
    ''' time series of measured channel '''
    fieldtype_range = 2
    ''' range of measured channel '''
    fieldtype_average = 3
    ''' average of measured channel '''
    fieldtype_min = 4
    ''' minimum of measured channel '''
    fieldtype_max = 5
    ''' maximum of measured channel '''
    fieldtype_counter = 6
    ''' cycle counter '''
    fieldtype_other_signal = 99
    ''' time series, but not of a measured channel '''

    def __init__(self, number, name, fieldtype=1, name_in_source=''
        , channelnumber=-1, channelname='', skip=False):
        self.number = number
        ''' (column) number of the field '''
        self.name = name
        ''' (column) name of the field '''
        self.name_in_source = name_in_source
        ''' (column) name in the source file '''
        self.fieldtype = fieldtype
        ''' type of the field
        could be important for repairing
        (e.g. offset not relevant for range fields) '''
        self.channelnumber = channelnumber
        ''' number of the channel '''
        self.channelname = channelname
        ''' name of the channel '''
        self.skip = skip
        ''' skip this field '''
        if len(channelname) == 0:
            self.channelname = self.name
        if len(name_in_source) == 0:
            self.name_in_source = self.name
    
    def __str__(self):
        s = ''
        if self.fieldtype == self.fieldtype_time:
            s = 'Time '
        elif self.fieldtype == self.fieldtype_range:
            s = 'Range '
        elif self.fieldtype == self.fieldtype_average:
            s = 'Average '
        elif self.fieldtype == self.fieldtype_min:
            s = 'Min '
        elif self.fieldtype == self.fieldtype_max:
            s = 'Max '
        elif self.fieldtype == self.fieldtype_counter:
            s = 'Counter '
        elif not self.is_channel_field():
            s = 'Other '
        if len(s) > 0:
            s += ' f'
        else:
            s += 'F'
        s += 'ield "%s", column number %d'%(self.name, self.number)
        if self.is_channel_field():
            if not (self.channelname == self.name):
                s += ', channel "%s"'%(self.channelname)
            if not (self.channelnumber == self.number):
                s += ' (%d)'%(self.channelnumber)
        return s
    
    def is_channel_field(self):
        return self.fieldtype in [
            self.fieldtype_channel_signal
            , self.fieldtype_range
            , self.fieldtype_average
            , self.fieldtype_min
            , self.fieldtype_max
            ]

    def is_channel_field_in_cycle(self):
        return self.fieldtype in [
            self.fieldtype_range
            , self.fieldtype_average
            , self.fieldtype_min
            , self.fieldtype_max
            ]
        
    def is_channel_signal(self):
        return self.fieldtype == self.fieldtype_channel_signal
        
class wmcs_channels:
    '''
    :purpose: channel data used by WMCS
    '''
    
    def __init__(self):
        self.channels = {}
        self.channels_by_label = {}
        self.fg_channels = {}
        self.columns = []
        # default column names in channels.set, are overwritten by load
        self.columns.append('label')
        self.columns.append('units')
        self.columns.append('calfac')
        self.columns.append('offset')
        
    def _parsedataline(self, s, section):
        chnl = {}
        idx = s.index(']')
        a = s[1:idx].split(',')
        chnl['id'] = int(a[0])
        chnl['id_in_section'] = int(a[1])
        a = s[idx+1:].split()
        if len(self.columns) != len(a):
            print('error parsing line\n%s'%s)
            print('lengths of column names (%d) and fields (%d) do not match'%(
                len(self.columns), len(a)))
            return
        for i, s in enumerate(self.columns):
            if s in ['label', 'units']:
                chnl[s] = a[i]
            elif s in ['nullable', 'limits']:
                chnl[s] = int(a[i])
            else:
                chnl[s] = float(a[i])
        chnl['section'] = section
        self.channels[chnl['id']] = chnl
        if section.startswith('function generator'):
            self.fg_channels[chnl['id_in_section']] = chnl['id']
        
    def load(self, folder='.'):
        pth = os.path.join(folder, 'channels.set')
        if not os.path.exists(pth):
            print('Channels file "%s" does not exist'%pth)
            return
        with open(pth, 'r') as f:
            line = f.readline()
            if line.startswith('#Knr'):
                print('Wrong format of channels file "%s": Blatest?'%pth)
                return
            section = ''
            while len(line) > 0:
                s = line.strip()
                if s.startswith('['):
                    if s.startswith('[         label'):
                        self.columns = s[1:-1].strip().split()
                    elif s.endswith(']'):
                        section = s[1:-1]
                    else:
                        self._parsedataline(s, section)
                line = f.readline()
            f.close()
        self.finalize()
            
    def add(self, id, name, calfac=1.0, offset=0.0, unit=''):
        ''' add channel '''
        self.channels[id] = {'id': id, 'label': name, 'calfac': calfac
            , 'offset': offset, 'units': unit}
        return self.channels[id]
        
    def _set_channels_by_label(self):
        self.channels_by_label = {}
        for key in self.channels.keys():
            label = self.channels[key]['label']
            self.channels_by_label[label] = key
    
    def get_channel_key_by_label(self, label):
        for key in self.channels.keys():
            if (label == self.channels[key]['label']):
                return key
        return None
    
    def finalize(self):
        self._set_channels_by_label()
        
    def compare(self, channels_old, prefixline=''):
        '''
        :purpose: compare 'self' to older version of channels
        '''
        addedorremoved = False
        msgs = []
        if len(channels_old.channels) > len(self.channels):
            addedorremoved = True
            msgs.append('%d channels removed'%(
                len(channels_old.channels) - len(self.channels)))
        if len(self.channels) > len(channels_old.channels):
            addedorremoved = True
            msgs.append('%d channels added'%(
                len(self.channels) - len(channels_old.channels)))
                
        removed = []
        for lbl in sorted(channels_old.channels_by_label.keys()):
            if not (lbl in self.channels_by_label.keys()):
                removed.append(lbl)
        if len(removed) > 0:
            msgs.append('Labels removed: %s'%','.join(removed))
        added = []
        for lbl in sorted(self.channels_by_label.keys()):
            if not (lbl in channels_old.channels_by_label.keys()):
                added.append(lbl)
        if len(added) > 0:
            msgs.append('Labels added: %s'%', '.join(added))
        if addedorremoved:
            return '\n'.join(msgs)
        for key in sorted(self.channels.keys()):
            chnl = self.channels[key]
            if key in channels_old.channels:
                chnl_old = channels_old.channels[key]
                if not (chnl['label'] == chnl_old['label']):
                    msgs.append('%sLabel for channel %d changed: "%s" -> "%s"'%(
                        prefixline, key, chnl_old['label'], chnl['label']))
                if not (chnl['units'] == chnl_old['units']):
                    msgs.append('%sUnit for channel %s (%d) changed: "%s" -> "%s"'%(
                        prefixline, chnl_old['label'], key, chnl_old['units'], chnl['units']))
                if not (chnl['calfac'] == chnl_old['calfac']):
                    msgs.append('%sCalibration factor for channel %s (%d) changed: %g -> %g'%(
                        prefixline, chnl_old['label'], key, chnl_old['calfac'], chnl['calfac']))
                if not (chnl['offset'] == chnl_old['offset']):
                    msgs.append('%sOffset for channel %s (%d) changed: %g -> %g'%(
                        prefixline, chnl_old['label'], key, chnl_old['offset'], chnl['offset']))
            else:
                msgs.append('%sNew channel "%s" (id=%d)'%(
                    prefixline, chnl['label'], key))
        return '\n'.join(msgs)
    
    def __str__(self):
        s = '     label     '
        if 'units' in self.columns:
            s += 'units         '
        if 'calfac' in self.columns:
            s += 'calfac        '
        if 'offset' in self.columns:
            s += 'offset       '
        s += '\n'
        for key in sorted(self.channels.keys()):
            chnl = self.channels[key]
            s += '\n%3d  '%(key)
            s += chnl['label'].ljust(10)
            if 'units' in self.columns:
                s += chnl['units'].ljust(10)
            if 'calfac' in self.columns:
                s += '%15.5e'%chnl['calfac']
            if 'offset' in self.columns:
                s += '%15.5e'%chnl['offset']
        return s
            
def add_function_generator_channels(fg_channel, feedback_channel
    , fg_channels=None):
    '''
    :purpose: add function generator and feedback channel to dictionary
    
    :param fg_channel: name of function generator channel
    :param feedback_channel: name of feedback channel
    :param fg_channels: dictionary of actuators
    '''
    if fg_channels is None:
        fg_channels = {}
        key = 1
    else:
        if len(list(fg_channels.keys())) == 0:
            key = 1
        else:
            key = max(list(fg_channels.keys())) + 1
    fg_channels[key] = {'fb': feedback_channel, 'fg': fg_channel}
    return fg_channels
    
 
def function_generator_channels(conf, channels):
    '''
    :purpose: create a dictionary of function generator channels
    
    :details: could be used in targetplateaus.createfilters
    
    :param conf: data from file wmcs.conf
    :param channels: data from file channels.set
    '''
    fg_channels = {}
    nr = conf.function_generator['channels']['size']
    for i in range(nr):
        key = i+1
        mode = conf.function_generator['channels'][key]['mode']
        # function generator channel number obtained from channels.set
        ifg = channels.fg_channels[i]
        fg_channel = channels.channels[ifg]['label']
        # feedback channel number obtained from wmcs.conf
        ifb = conf.fg_channel_property(key, 'feedback_channel')
        fb_channel = channels.channels[ifb]['label']
        add_function_generator_channels(fg_channel=fg_channel
            , feedback_channel=fb_channel
            , fg_channels=fg_channels)
    return fg_channels

def load_sokkia_repair(filename='sokkialabels.repair', folder='.'):
    newlabels = {}
    pth_repair = os.path.join(folder, filename)
    if os.path.exists(pth_repair):
        with open(pth_repair, 'r') as f:
            line = f.readline() # header line
            line = f.readline()
            while len(line) > 0:
                a = line.strip().split('\t')
                if len(a) >= 2:
                    newlabels[a[0]] = a[1]
                line = f.readline()
            f.close()
    return newlabels

def get_strain_gauge_channels(meas, label=''):
    ret = []
    channels = sorted(meas.keys())
    for channel in channels:
        sg = strain_gauge_channel(channel)
        if sg.isvalid():
            if (len(label) > 0) or (sg.baselabel() == label):
                ret.append(channel)
    return ret

class channel_type:
    def __init__(self, channel):
        self.channel = channel
        ''' channel name in wmc_data object '''
        self.pre_label = ''
        ''' 
        part of the label, e.g. indicating if it is the range or the average
        '''
        self.type = ''
        ''' type of the channel '''
        dct = self._get_dict(self.channel)
        for key in dct:
            self.__dict__[key] = dct[key]
            
    def isvalid(self):
        '''
        :purpose: check if the channel is recognized as the proper type
        '''
        return len(self.type) > 0
        
    def baselabel(self):
        if not self.isvalid():
            return ''
        return self.channel[len(self.pre_label):]
        
    def _get_dict(self, channel):
        return {}
        
    def __str__(self):
        if not self.isvalid():
            return 'type of channel "%s" unknown'%self.channel
        s = '== channel   %s'%self.channel
        s += '\n= type      %s'%self.type
        if len(self.pre_label) > 0:
            s += '\n= pre-label %s'%self.pre_label
            s += '\n= base      %s'%self.baselabel()
        return s

class strain_gauge_channel(channel_type):    
    def _get_dict(self, channel):
        return wmclibdata.strain_gauge_props_from_channel(channel)
    
class general_channel(channel_type): 
    def __init__(self, channel, type='G', possible_pre_labels=None):
        channel_type.__init__(self, channel)
        self.type = type
        a = possible_pre_labels
        if possible_pre_labels is None:
            a = wmclibdata.possible_pre_labels()
        for s in a:
            if channel.startswith(s):
                self.pre_label = s
        
class strain_gauge_channel(channel_type):    
    def _get_dict(self, channel):
        return wmclibdata.strain_gauge_props_from_channel(channel)
    
class force_channel(channel_type):
    def _get_dict(self, channel):
        return wmclibdata.force_props_from_channel(channel)
        
class displacement_channel(channel_type):
    def _get_dict(self, channel):
        return wmclibdata.displacement_props_from_channel(channel)

def load_sokkia(filename='sokkia.txt', folder='.', newlabels=None):
    '''
    :purpose:
        load positions from sokkia into dictionary
    :details:
        mapping E -> Z, N -> X, Z -> Y
        multiply by 1000 to convert to mm
    '''
    pth = os.path.join(folder, filename)
    ret = {}
    if not os.path.exists(pth):
        print('sokkia output file "%s" not found'%pth)
        return ret
    with open(pth, 'r') as f:
        print('reading positions from sokkia output file "%s"'%pth)

        cols = []
        colwidths = []
        line = f.readline()
        nxt = (len(line) > 0)
        while nxt:
            if line.startswith('------'):
                line = f.readline()
                a = line.rstrip().split('  ')
                for col in a:
                    if len(col.strip()) > 0:
                        cols.append(col.strip())
                colstarts = [0]
                for col in cols:
                    poscol = line.find(' %s '%col)
                    if poscol < 0:
                        poscol = line.find(' %s\n'%col)
                    colstarts.append(poscol + len(col)+1)
                line = f.readline()
                nxt = False
            line = f.readline()
            if (len(line) == 0):
                nxt = False
        while (len(line) > 0):
            lbl = ''
            for i, col in enumerate(cols):
                val = line[colstarts[i]:colstarts[i+1]].strip()
                # print(val)
                if i == 0:
                    lbl = val
                    dct = {}
                elif len(val) > 0:
                    if len(lbl) > 0:
                        dct[col] = float(val)
                if len(lbl) > 0:
                    ret[lbl] = dct
            line = f.readline()
            
        f.close()
    for lbl in ret:
        pos = ret[lbl]
        pos['position'] = 1000.0 * np.array([pos['N'], pos['Z'], pos['E']])
    return ret

def repair_sokkia_labels(positions, newlabels):
    '''
    :purpose: replace sokkia labels with other ones
    '''
    if newlabels is None:
        return positions
    else:
        keys = sorted(newlabels.keys())
        if len(keys) == 0:
            return positions
    # there are labels
    print('replacing sokkia labels')
    ret = {}
    for key in positions.keys():
        if key not in keys:
            ret[key] = positions[key]
        else:
            ret[newlabels[key]] = positions[key]
    return ret

def view_name(vw):
    if vw == view_from_top:
        return 'top'
    elif vw == view_from_side:
        return 'side'
    elif vw == view_from_tip:
        return 'tip'

def view_components(vw):
    if vw == view_from_top:
        # y in plot is x in 3-d, x in plot iz z in 3-d
        return 2, 0
    elif vw == view_from_side:
        # y in plot is y in 3-d, x in plot iz z in 3-d
        return 2, 1 
    elif vw == view_from_tip:
        # x and y in plot are x and y in 3-d
        return 0, 1
        
def replace_channel_part(meas, channel_src, channel_tgt
    , value_criterium, channel_criterium='counter', use_original=True):
    '''
    :purpose: replace the latter part of meas.channel_tgt by meas.channel_src
    
    :details: this can be necessary if two contact (unintentionally of course)
        have been switched during the (fatigue) test.
        The channels in the objects are first copied to channels chnl_original.
        Then the channels are switched if
        
         meas[channel_criterium] > value_criterium
        
    '''
    print('Replacing part of channel in wmc_data obect (meas)')
    print('meas.%s = meas.%s if meas.%s > %g'%(
        channel_tgt, channel_src, channel_criterium, value_criterium))
    criterium_found = False
    channels = []
    for chnl in meas:
        if chnl == channel_criterium:
            criterium_found = True
        ochannel = general_channel(chnl)
        if channel_src == ochannel.baselabel():
            a = [chnl]
            # source channel found, search for corresponding target
            chnl2 = '%s%s'%(ochannel.pre_label, channel_tgt)
            if chnl2 in meas:
                a.append(chnl2)
            channels.append(a)
    
    # sanity checks
    errorfnd = False
    if not criterium_found:
        errorfnd = True
        print('ERROR: Channel "%s" does not exist (criterium)'%(
            channel_criterium))
            
    if len(channels) == 0:
        errorfnd = True
        print('ERROR: No channel "%s" does not exist'%channel1)
    
    for pair in channels:
        if len(pair) < 2:
            errorfnd = True
            ochannel = general_channel(pair[0])
            chnl2 = '%s%s'%(ochannel.pre_label, channel2)
            print('ERROR: Channel "%s" for switching with "%s" does not exist'%(
            chnl2, pair[0]))
            
    if errorfnd:
        print('Error found: Do not switch')
        return
    
    mask_repair = (meas[channel_criterium]>value_criterium)
    if not max(mask_repair):
        print('Criterium meas.%s > %g never met: Do not switch'%(
            channel_criterium, value_criterium))
        return
    else:
        print('Switching %d values'%(sum(mask_repair)))       
        
    for pair in channels:
        src_chnl = pair[0]
        if use_original:
            # the channel has been changed already
            src_original = '%s_original'%src_chnl
            if src_original in meas:
                src_chnl = src_original
        
        tgt_chnl = pair[1]
        tgt_original = '%s_original'%tgt_chnl
        if not tgt_original in meas:
            print('copy meas.%s to meas.%s'%(tgt_chnl, tgt_original))
            meas[tgt_original] = np.array(meas[tgt_chnl])
        print('copy part of meas.%s to meas.%s'%(src_chnl, tgt_chnl))
        # replace each element True in mask_repair
        # with the value from the source 
        meas[tgt_chnl][mask_repair] = meas[src_chnl][mask_repair]

# ==== WMClib keyword-value file  ===================================
# ===================================================================

class key_value_file(object):
    """
    reads keyvalue files like config.set, system.set and transduc.set
    """
    
    def __init__(self,inFile=None,inOptions=''):
        if inFile is not None:
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
                        
                    if bVerbose: print(keyword," = ",value)

        f.close()

    def read_transduc_set(self,inFile,inOptions=''):
        """
        deze functie zet de gelezen waardes in de global namespace
        """

        # options
        bVerbose = 'v' in inOptions

        # first read the keywords/values
        self.read_key_value(inFile,inOptions)

        f = open(inFile,'r')
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

                        if bVerbose:  print(label,float(radius),'(',float(X),float(Y),float(Z),')',float(group))
                    
                    else :
                        print("error in line: '",line,"'")

        f.close()
    
    def info(self):
        """
        This functions displays the contents of the object
        """
        print('== key_value_file ==')
        for i in self.iteritems():
            print("%-20s"%i[0],i[1])

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

class transduc_set(key_value_file):
    """
    reads transduc.set
    """
    
    def read_key_value(self,inFile, inOptions=''):
        """
        deze functie zet de gelezen waardes in de global namespace
        """

        bVerbose = 'v' in inOptions
        f = open(inFile,'rb')
        self.groups = {}
        self.wire_groups = {}
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

                    if wmc.isFloat(radius) and \
                       wmc.isFloat(X)      and \
                       wmc.isFloat(Y)      and \
                       wmc.isFloat(Z)      and \
                       wmc.isInt(group)  :
                        labeltype = label[:-2]
                        labelno = int(label[-2:])
                        self.__dict__[label] = {
                            'position':[float(X), float(Y), float(Z)]
                            , 'group': int(group)
                            , 'radius': float(radius)
                            , 'labeltype':labeltype
                            , 'labelno':labelno}
                        i_group = int(group)
                        if not (i_group in self.groups):
                            self.groups[i_group] = {'radius': float(radius)}
                        if not labeltype in self.groups[i_group]:
                            self.groups[i_group][labeltype] = []
                        self.groups[i_group][labeltype].append(label)

                        if bVerbose:
                            print(label,float(radius),'(', \
                                float(X),float(Y),float(Z),')',float(group))
                    
                    else :
                        print("error in line: '",line,"'")

        f.close()


