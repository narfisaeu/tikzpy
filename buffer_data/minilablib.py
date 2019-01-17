"""
minilablib

This module contains functions for post processing of standard WMC
minilab tests.
"""

import re
import os
import sys
import json
import numpy as np
import wmclib as wmc
import matplotlib.pyplot as plt
import itertools as it
from glob import glob
import wmclibdata

# some initialization of minilablib

version='20190104.11161'

print('minilablib %s'%version)

# functions...

def join_caseinsensitive(a, b, verbose = True, halt_on_not_found = True):
    """
    Internal helper function to join two path part's.
    
    (function is needed because we mixed up case sometimes)
    """
    return wmclibdata.join_caseinsensitive(a, b, verbose, halt_on_not_found)

def find_data_dir( identification, 
                   project, 
                   tvct,
                   verbose = True, 
                   halt_on_not_found = True,
                   series = '') :
    """
    derives the directory where the measurement data should be residing based
    on *project* name, *identification* and *tvct* number.
    
    *project* can be (like) 'innwind', 'upwind', 'rnd' or 'internal'
    """
    return wmclibdata.find_data_dir( identification, project, tvct,
                   verbose, halt_on_not_found, series)

def load_some_file( datadir, 
                    identification, 
                    testtype = 'some test', 
                    extensions = None, 
                    verbose = True, 
                    halt_on_not_found = True,
                    rep_channels = None,
                    **kwargs ) :
    """
    Helper function for the other load_xxx_file functions.
    
    Loads the BFG or WMCS file for a test from *datadir* with *identification*
    
    Returns : wmc_data object if the file is found
    """
    if verbose:
        print( 'Trying to find a %s file in \n %s \n with name : %s....' % 
               (testtype, datadir, identification) )
               
    if not extensions: 
        extensions = []  # make extensions iterable if it is the default None
    
    # name_without_ext = os.path.join(datadir, testname) 
    
    print(rep_channels)
    for ext in extensions:
        filename = join_caseinsensitive( datadir, 
                                         identification + ext,
                                         halt_on_not_found = False)
                                         
        if filename is not None and os.path.exists(filename):
            if verbose:
                print('Loading : %s\n'% (filename))
            root, ext2 = os.path.splitext(filename)
            ext2 = ext2.lower()
            if ext2 in ['.buffer', '.rngavg', '.points']:
                return wmc.load_wmcs(filename
                    , rep_channels = rep_channels
                    , **kwargs)
            if ext2 == '.dfx':
                return wmc.load_dfx(filename)
            if ext2 == '.st3':
                return wmc.load_st3(filename)
            if ext2 == '.dmp':
                return wmc.load_dmp(filename)
            # and then we assume it is a BFG buffer file, for .slw .nul etc...
            return wmc.load_buf(filename)

    if halt_on_not_found:
        raise ValueError('File not found' )
        
    return None

def load_slow_cycle_file( datadir, 
                          identification,
                          verbose = True, 
                          halt_on_not_found = True,
                          rep_channels = None,
                          **kwargs ) :
    """
    Loads the BFG or WMCS file for a slow cycle test from *datadir* 
    with *testname*
    
    Returns : wmc_data object if the file is found
    """
    return load_some_file( datadir, 
                           identification,
                           testtype = 'slow cycle',
                           extensions = ['.slw', 
                                         '_slow.buffer' ] ,
                           verbose = verbose, 
                           halt_on_not_found = halt_on_not_found,
                           rep_channels = rep_channels,
                           **kwargs)  

def load_fatigue_file( datadir, 
                       identification,
                       verbose = True, 
                       halt_on_not_found = True,
                       rep_channels = None,
                       **kwargs ) :
    """
    Loads the BFG or WMCS file for a fatigue test from *datadir* 
    with *testname*
    
    If 
    
    Returns : wmc_data object if the file is found
    """
    return load_some_file( datadir, 
                           identification,
                           testtype = 'fatigue',
                           extensions = ['.dfx', 
                                         '.st3',
                                         '_fat.rngavg' ] , 
                           verbose = verbose, 
                           halt_on_not_found = halt_on_not_found,
                           rep_channels = rep_channels,
                           **kwargs ) 

def load_static_file( datadir, 
                      identification,
                      verbose = True, 
                      halt_on_not_found = True,
                      rep_channels = None,
                      **kwargs ) :
    """
    Loads the BFG or WMCS file for a fatigue test from *datadir* 
    with *testname*
    
    Returns : wmc_data object if the file is found
    """
    return load_some_file( datadir, 
                           identification,
                           testtype = 'static',
                           extensions = ['.buf', 
                                         '.dmp',
                                         '_tens.buffer', 
                                         '_comp.buffer',
                                         '.slw',
                                         '_slow.buffer',
                                         '.buffer'] , 
                           verbose = verbose, 
                           halt_on_not_found = halt_on_not_found,
                           rep_channels = rep_channels,
                           **kwargs )  

def find_fatigue_buffers( identification, 
                          project, 
                          tvct, 
                          cycle_list = None):
    """
    Find a filtered selection of buffer files of the test identified with
    *identification*, *project*, and *tvct*.
    
    *cycle_list* can be either:
        - None, every buffer is returned
        - A list of numbers, the buffer nearest to every number is returned
        - One of '1k', '10k', '100k' or '1000k' (or 1000, 10000, 100000 or
          1000000), a selection of buffers is returned according 
          some standard (?)
    
    Note: works only for WMCS buffer files
    
    Returns: list of filenames and a list of actual cycles
    """
 
    # find the data directory on the M:\ drive
    data_dir = find_data_dir(identification, project, tvct)
 
    # find fatigue buffers
    pattern = data_dir + '\\' + identification + '_fat_*.buffer'
    bufs = glob(pattern)
 
    # find cycle numbers from filename
    cycles = []
    start  = len(data_dir + '\\' + identification + '_fat_')
    for buf in bufs:
        end = len(buf) - len('.buffer')
        cycles.append(int(buf[start:end]))

    # sort bufs and cycles using argsort
    ar = np.argsort(cycles)
    bufs = list(np.asarray(bufs)[ar])
    cycles = list(np.asarray(cycles)[ar])
    
    if not cycle_list:
        # we're done, return everything found
        return bufs, cycles
    
    # find at which cycles we want a buffer file..
    max_cycle = max(cycles)
    
    if      cycle_list == '1k'     or cycle_list == 1000:
        
        wanted_cycles = [1]
        step = 100
        wanted_cycles += [s for s in range(step, max_cycle + step, step)]
        
    elif cycle_list == '10k'    or cycle_list == 10000:
        
        wanted_cycles = [1, 500]
        step = 1000
        wanted_cycles += [s for s in range(step, max_cycle + step, step)]

    elif cycle_list == '100k'   or cycle_list == 100000:
        
        wanted_cycles = [1, 1000]
        step = 10000
        wanted_cycles += [s for s in range(step, max_cycle + step, step)]

    elif cycle_list == '1000k'   or cycle_list == 1000000:

        wanted_cycles = [1, 1000, 10000]
        step = 100000
        wanted_cycles += [s for s in range(step, max_cycle + step, step)]

    else:
        try: # check if cycle_list is iterable, we don't check for item type...
            _ = (c for c in cycle_list) 
            wanted_cycles = cycle_list
        except:
            raise ValueError('wrong value for cycle_list')
    
    # find the buffers closest to the recorded buffers...
    filtered_bufs = []
    filtered_cycles = []
    last_one = None
    for cycle in wanted_cycles:
        # find the buffer closest to te requested number of cycles
        index = np.argmin(np.abs(np.asarray(cycles)-cycle))
        # don't do the same buffer twice
        if index != last_one:
            last_one = index
            filtered_bufs.append(bufs[index])
            filtered_cycles.append(cycles[index])
    
    return filtered_bufs, filtered_cycles


def find_most_acurate_load_channel(m, verbose = True, halt_on_not_found = True):
    """
    Find label of the most accurate force channel wmc_data *m*.
    
    According to the convention(?) that force channels are labelled as
    'F01', 'F02', .... and that the label with the highest number is the
    most accurate.
    """
    
    rngavg = ( m.file_name[-6:] == 'rngavg' or
               m.file_name[-3:] == 'dfx'    or
               m.file_name[-3:] == 'st3') 

    if rngavg:
         F_labels = [label for label in m if re.match("^A_F\d{2}$", label)]
    else:
         F_labels = [label for label in m if re.match("^F\d{2}$", label)]

    if verbose:
        print ('Found load channel(s) : %s' % F_labels)
    
    if F_labels:
        F_labels.sort()
        F_labels.reverse() 
        if verbose:
            print ('Most acurate load channel : %s' % F_labels[0])
        if rngavg:
             return F_labels[0][-3:]
        else:
             return F_labels[0]
    else:
        if halt_on_not_found:
            raise ValueError('No force channel found')

    return None

def find_displ_channel(m, verbose = True, halt_on_not_found = True):
    """
    Find the label of the displacement channel
    
    At the moment just checks if label 'S01' or 'A_S01' is present.
    """
    retval = None
    if 'S01' in m or 'A_S01' in m:
        retval = 'S01'
        
    if verbose:
        print('Found displacement channel : %s' % retval)
    
    if halt_on_not_found and not retval:
        msg = 'Could not find displacement channel'
        raise ValueError(msg)
        
    return retval

def find_tamb_channel(m, verbose = True, halt_on_not_found = True):
    """
    Find the label of the ambient temperature channel
    """
    
    bT01  = 'T01'  in m or 'A_T01'  in m
    bTC01 = 'TC01' in m or 'A_TC01' in m
    
    retval = None
    if bT01 and bTC01:
        print('WARNING: Both T01 and TC01 in measurement')
    else:
        if bT01:  retval = 'T01'
        if bTC01: retval = 'TC01'
    
    if halt_on_not_found and not retval:
        msg = 'Could not find ambient temperature channel'
        raise ValueError(msg)
        
    if verbose:
        print('Found ambient temperature channel : %s' % retval)
        
    return retval
    
def find_tspec_channel(m, verbose = True, halt_on_not_found = True):
    """
    Find the label of the specimen temperature channel
    """
    
    bT02  = 'T02'  in m or 'A_T02'  in m
    bTC02 = 'TC02' in m or 'A_TC02' in m
    
    retval = None
    if bT02 and bTC02:
        print('WARNING: Both T02 and TC02 in measurement')
    else:
        if bT02:  retval = 'T02'
        if bTC02: retval = 'TC02'
    
    if halt_on_not_found and not retval:
        msg = 'Could not find speciment temperature channel'
        raise ValueError(msg)
        
    if verbose:
        print('Found speciment temperature channel : %s' % retval)
        
    return retval


# Some functions to find particular strain gauge labels
def find_some_strain( m, 
                      prefix = '001',
                      postfix = '999',
                      gauge_name = 'some strain gauge',
                      verbose = True, 
                      halt_on_not_found = True):
    """
    Helper function for the find_xx_strain functions
    """

    rngavg = ( m.file_name[-6:] == 'rngavg' or
               m.file_name[-3:] == 'dfx'    or
               m.file_name[-3:] == 'st3') 
               
    if rngavg: 
        prefix = 'A_' + prefix
    
    pos = [ prefix + c + postfix for c in[ 'S', 'C', 'R', 'O',
                                           's', 'c', 'r', 'o' ] ]

    retval = next((label for label in pos if label in m), None)

    if verbose:
        print('Found %s strain gauge : %s' % (gauge_name, retval))
        
    if halt_on_not_found and not retval:
        msg = 'Could not find %s strain gauge label' % gauge_name
        raise ValueError(msg)
    
    if retval and rngavg:
        retval = retval[2:]   # strip 'A_' from labelname
    
    return retval

def valid_orientation(orientation = 0,verbose = True, halt_on_not_found = True):
    """
    """
    if (isinstance(orientation, int) or isinstance(orientation, long)):
        orientation = '{0:03d}'.format((orientation))
    
    if orientation in ['000', '090', '045', '135']:
        return orientation
        
    if halt_on_not_found:
        msg = 'Could not find valid orientation for: {0}'.format(orientation)
        raise ValueError(msg)

def find_front_strain(m, orientation, verbose = True, halt_on_not_found = True):
    """
    Find the strain gauge in axial direction on the front.
    """
    orientation = valid_orientation( orientation = orientation,
                                     verbose = verbose, 
                                     halt_on_not_found = halt_on_not_found )

    return find_some_strain( m,
                             prefix = '001',
                             postfix = orientation,
                             gauge_name = 'front {0}'.format(orientation),
                             verbose = verbose, 
                             halt_on_not_found = halt_on_not_found )

def find_back_strain(m, orientation, verbose = True, halt_on_not_found = True):
    """
    Find the strain gauge in axial direction on the back.
    """
    orientation = valid_orientation( orientation = orientation,
                                     verbose = verbose, 
                                     halt_on_not_found = halt_on_not_found )
    return find_some_strain( m,
                             prefix = '002',
                             postfix = orientation,
                             gauge_name = 'back {0}'.format(orientation),
                             verbose = verbose, 
                             halt_on_not_found = halt_on_not_found )
    

def add_remarks_public(output, remark):
    if output['remarks_public'] :
        output['remarks_public'] += ',\n '
    output['remarks_public'] += remark

def print_coupon_json(coupon_json):
    """
    Print (coupon) JSON.
    """
    json_keys = list(coupon_json.keys())
    json_keys.sort()
    print('\n')
    if 'identification' in coupon_json:
        print('JSON data for : %s \n' % coupon_json['identification'])
    for k in json_keys:
        try:
            print (' %-30s: %s' % (k, coupon_json[k]))
        except:
            print('Unexpected error printing key "%s": %s'%(k, sys.exc_info()[1]))
    print('\n')

def read_json(filename='coupons.json'):
    f = open('coupon.json','r')
    coupons = json.load(f)
    f.close()
    return coupons

def write_json(inJSON, filename='output.json'):
    """
    Write (test output) JSON to a file.
    """
    f=open(filename,'w')
    json.dump(inJSON, f, indent=4, sort_keys=True)
    f.close()


def find_limits(x, start_level=500.0, end_level=2500.0, verbose = True):
    """
    Find the start and end index in a strain signal to calculate the Youngs
    modulus and the Poisson ratio etc....
    
    We try to find the part were the strain *x* rises from *start_level* to
    *end_level*.
    
    Arguments:
        *x*:
            1D np.ndarray with a strain signal
            
        *start_level*:
            strain level were we want to start, default 500 mu
        
        *end_level*:
            strain level were we want to end, default 2500 mu
    
    Returns:
        start_index, end_index, max_index
        
    Note:
        for compressive tests, negate *x* in the function call
    """
    max_index = np.argmax(x)
    records = np.arange(len(x), dtype=np.int)

    # start record
    if np.any(x <= start_level):
        mask = np.logical_and(x <= start_level, records <= max_index)
        # we'll take the last one of this mask, and add one
        start_index = records[mask][-1] + 1
    else:
        start_index = 0
    
    # end record
    mask = np.logical_and(x <= end_level, records <= max_index)
    end_index = records[mask][-1]
    
    if verbose:
        print ('\nfind_limits: start, end and max index: {0}, {1}, {2}\n'.format(
               start_index, end_index, max_index))
    
    return start_index, end_index, max_index

def E_core(load, stress, strain, factor = 1.0):
    """
    Function to calculate maximum slope (E-modulus) from stress/strain curves.
	
	Used for DIAB, project M16-006
	Range comes from ISO 844 (25% - 75%), remaining algorithm from DIAB
	
	Algorithm divides the load (in range 25%-75% of maximum load) in 6 intervals. For these 6 intervals, the slope is determined.
	Succesive intervals are added and the maximum of these combinedintervals is determined. The maximum of the two slopes in this maximum of 
	these combined slopes, is the output E-modulus.
	
    Arguments:
    
        *load*, *stress* , *strain*: 
        
            np.ndarrays with load and stress and strain signals
        
                 
        *factor*:
			factor for the output
            
    Returns:
		factor * maxslope, min_record, max_record

                    maxslope= the maximum slope of the two combined slopes that have the highest slope.
                    min_record is the first record of the maxslope
                    max_record is the last record of the maxslope
    """
    # determine interesting data points from load
    i_argmax = np.argmax(np.abs(load))
    maxvalue = load[i_argmax]
    if maxvalue > 0:
        min_interesting = 0.25 * maxvalue
        max_interesting = 0.75 * maxvalue
    else:
        max_interesting = 0.25 * maxvalue
        min_interesting = 0.75 * maxvalue
    intervals = np.arange(min_interesting, max_interesting, (max_interesting-min_interesting)/6)
	
    slopes = []
    filterlist=[]
	
    for i, minval in enumerate(intervals):
        if i == len(intervals)-1:
            maxval = max_interesting
        else:
            maxval = intervals[i+1]
        fltr = np.logical_and(load >= minval, load < maxval)
        stress0 = stress[fltr]-np.average(stress[fltr])
        strain0 = strain[fltr]-np.average(strain[fltr])
        slopes.append(np.sum(stress0 * strain0)/np.sum(strain0*strain0))
        filterlist.append(fltr)
	
    combinedslopes = []
    for i, slope in enumerate(slopes):
        if i > 0:
            combinedslopes.append(slope + slopes[i-1])
    #determine the maximum slope of the segment (combinedslopes) with the maximum slope
    a=slopes[np.argmax(combinedslopes):np.argmax(combinedslopes)+2]#slopes[0:2] when maximum in first combinedslopes.
    maxslope=np.max(a) 
    argmaxslope=(np.argmax(a)+np.argmax(combinedslopes))
    b=filterlist[argmaxslope]
    selection=np.where(b==True)
    max_record=np.max(selection)
    min_record=np.min(selection)
    return factor * maxslope, min_record, max_record
        

def fit_and_plot( x, y, istart, iend, factor = 1.0, ax = None, lbl_fmt = ''):
    """
    General function to perform a linear regression and create a plot for
    Young's modulus, shear modulus and Poissons ratio's

    Arguments:
    
        *x*, *y*: 
        
            np.ndarrays with xand y signals
        
        *istart*, *iend*:
        
            indices for x and y to perform linear regression on
            
        *factor*:
            
            
        *ax*: 
        
            matplotlib Axes to plot on, if None no plot is made
            
        *lbl_fmt*:
        
            label formatuing string used to create the label of the plot
    """
    a, b = np.polyfit( x[istart:iend], y[istart:iend], 1)
    
    if ax:
        lbl = lbl_fmt.format(a * factor)
        
        ax.plot( x[[istart,iend]], x[[istart,iend]] * a + b,
                 'o--', lw = 2, label = lbl)
                
    return  a * factor, b * factor

    
def fat_statics_dyn(meas, ch):
    """
    returns a list of strings formatted with the (cycles) weighted mean 
    max/min and absolute max/min of dynamic signal ch from meas
    """
    # calculate de delta cycles if not done before
    if 'dCycles' not in meas.keys():
        meas['dCycles'] = meas['counter'] - np.roll(meas['counter'], 1)
        meas['dCycles'][0] = 0
        
    sig_max = meas['A_' + ch] + meas['R_' + ch] / 2
    sig_min = meas['A_' + ch] - meas['R_' + ch] / 2
    dCycles = meas['dCycles']
    N_max = np.nanmax(meas['counter'])
    
    return ['{0:.3f}'.format( (np.nansum((sig_max)* dCycles) / N_max) ),
            '{0:.3f}'.format( (np.nansum((sig_min)* dCycles) / N_max) ),
            '{0:.3f}'.format( np.nanmax(sig_max)                      ),
            '{0:.3f}'.format( np.nanmin(sig_min)                      ) ]

def fat_statics_stat(meas, ch):
    """
    returns a list of strings formatted with the (cycles) weighted mean 
    max/min and absolute max/min of signal ch from meas.
    """
    # calculate de delta cycles if not done before
    if 'dCycles' not in meas.keys():
        meas['dCycles'] = meas['counter'] - np.roll(meas['counter'], 1)
        meas['dCycles'][0] = 0
        
    sig_avg = meas['A_' + ch]
    dCycles = meas['dCycles']
    N_max = np.nanmax(meas['counter'])
    
    return ['{0:.3f}'.format( np.nanmax(sig_avg)                      ),
            '{0:.3f}'.format( np.nanmin(sig_avg)                      ),
            '{0:.3f}'.format( (np.nansum((sig_avg)* dCycles) / N_max) ) ]

def plot_stat_signals(meas):
    """
    Create a plot with the most important signals vs. record
    """
    plt.figure()
    plt.title('shear modulus for %s' %os.path.split(meas.file_name)[1])

    ax = plt.subplot(221)
    f_type = ['F', 'f']
    f_no   = ['{0:02d}'.format(i) for i in range(0,11)]
    for t, n in it.product(f_type, f_no):
        label = t + n
        if label in meas.keys():
            plt.plot(meas[label], label=label)
    plt.legend(loc='best')
    
    ax = plt.subplot(222)
    s_type = ['S', 's']
    s_no   = ['{0:02d}'.format(i) for i in range(0,11)]
    for t, n in it.product(s_type, s_no):
        label = t + n
        if label in meas.keys():
            plt.plot(meas[label], label=label)
    plt.legend(loc='best')

    ax = plt.subplot(223)
    sg_no   = ['{0:03d}'.format(i) for i in range(1,11)]
    sg_type = ['S', 'C', 'R', 'O', 's', 'c', 'r', 'o']
    sg_dir  = ['000', '045', '090', '135']
    for n, t, d in it.product(sg_no, sg_type, sg_dir):
        label = n + t + d
        if label in meas.keys():
            plt.plot(meas[label], label=label)
    cg_no   = ['{0:02d}'.format(i) for i in range(0,11)]
    cg_type = ['CG', 'Cg', 'cg', 'cG']
    for t, n in it.product(cg_no, cg_type):
        label = t + n
        if label in meas.keys():
            plt.plot(meas[label], label=label)
    plt.legend(loc='best')

    ax = plt.subplot(224)
    t_type = ['T', 't']
    t_no   = ['{0:02d}'.format(i) for i in range(0,11)]
    for t, n in it.product(t_type, t_no):
        label = t + n
        if label in meas.keys():
            plt.plot(meas[label], label=label)
    rh_no   = ['{0:02d}'.format(i) for i in range(0,11)]
    rh_type = ['RH', 'Rh', 'rH', 'rh']
    for t, n in it.product(rh_no, rh_type):
        label = t + n
        if label in meas.keys():
            plt.plot(meas[label], label=label)
    plt.legend(loc='best')
    
    wmc.savefig('all signals.png')

class channel(wmc.channel):
    '''
    :purpose: override of channel based on name for minilab
    
    :details:
    
        * F01 and S01 are main force and displacement
        * F02 and S02 additional force and displacement
        * T01: ambient temperature
        * T02: specimen temperature
        * Strain gauges
        
            * nr 1: front, 2: back
            * angle: 0:axial, 90: transverse
        
    '''
    def __init__(self, channelname):
        
        wmc.channel.__init__(self, channelname)
        if self.channeltype == 'F':
            if self.number == 1:
                self.displayname = 'Force'
            elif self.number == 2:
                self.displayname = 'Force additional'
            elif self.number > 2:
                self.displayname = 'Force additional %d'%(self.number - 1)
        elif self.channeltype == 'S':
            if self.number == 1:
                self.displayname = 'Displacement actuator'
            elif self.number == 2:
                self.displayname = 'Displacement additional'
            elif self.number > 2:
                self.displayname = 'Displacement additional %d'%(self.number - 1)
        elif self.channeltype == 'T':
            if self.number == 1:
                self.displayname = 'Temperature ambient'
            elif self.number == 2:
                self.displayname = 'Temperature specimen'
            elif self.number > 2:
                self.displayname = 'Temperature additional %d'%(self.number - 1)
        elif self.channeltype == 'SG':
            side = ''
            if self.number == 1:
                side = 'front'
            elif self.number == 2:
                side = 'back'
            else:
                side = 'side %d'%self.number
            direction = ''
            if np.abs(self.angle) < 0.5:
                direction = 'axial'
            elif np.abs(self.angle-90.0) < 0.5:
                direction = 'transverse'
            else:
                direction = '%g degrees'%self.angle
            self.displayname = '%s %s %s'%(self.quantity, direction, side) 

def mapped_channellist(meas, default=True, extrachannels=None):
    '''
    :purpose: obtain a list of channels for user-friendly excel output
    
    :details: default channels
        F01, F02, S01, S02
        strain gauges 00[1,2][S,C,R,O][000,090]
        temperatures T01, T02
    '''
    ret = []
    a =[]
    if default:
        # 2 force channels, 2 displacement channels
        for chnl in ['record', 'testtime'
            , 'F01', 'F02', 'S01', 'S02']:
            a.append(chnl)
        # strain gauges
        for sg in ['001', '002']:
            for sgtype in ['S', 'C', 'R', 'O']:
                for sgangle in ['000', '090']:
                    a.append('%s%s%s'%(sg, sgtype, sgangle))
        for sgnl in ['T01', 'T02']:
            a.append(sgnl)
    if not (extrachannels is None):
        for chnl in extrachannels:
            a.append(chnl)
    a.append('unixtime')
    for chnl in a:
        if chnl in meas:
            ret.append(channel(chnl).mapped(meas))
    
        
    return ret

class wmc_data_instron(wmc.wmc_data_text):
    def __init__(self, specimen, instrontype=''):
        self.specimen = specimen
        ''' specimen name '''
        postypes = ['', 'stop', 'steps.tracking', 'steps.trends']
        if not (instrontype.lower() in postypes):
            raise ValueError('Instron file type "%s" unknown, choose one of\n%s'%(
                instrontype, ', '.join(postypes)))
        file_name = self.specimen
        if len(instrontype) > 0:
            file_name += '.%s'%instrontype
        file_name += '.csv'
        self.instrontype = instrontype
        ''' instron file type '''
        wmc.wmc_data_text.__init__(self, file_name=file_name)
        self.file_type = 'Instron'
        if len(instrontype) > 0:
            self.file_type += ' %s'%instrontype
    
    def get_all_occ(self, col, sub):
        ret = []
        istart = 0
        i = col.find(sub, istart)
        while i > 0:
            ret.append(i)
            istart = i+1
            i = col.find(sub, istart)
        return ret
    
    def _field_from_label(self, icol, name_in_source , fieldtype=-1, verbose=False):
        '''
        :details: mapping default
            Total Time (s): testtime [s]
            Cycle Elapsed Time (s): cycle_elapsed_time [s]
            Total Cycles: counter, unit [-]
            Elapsed Cycles: elapsed_cycles, [-]
            Step: step [-]
            Total Cycle Count(8800 (10.0.0.2 : 0) Waveform): total_cycle_count [-]
            Position(8800 (10.0.0.2 : 0):Position) (mm): S01 [mm]
            Load(8800 (10.0.0.2 : 0):Load) (kN): F01 [kN]
            Time Stamp(PC): time_stamp [s]
            Strain(8800 (10.0.0.2 : 0):Position) (%):001S000 [-]
            Stress(8800 (10.0.0.2 : 0):Load) (MPa): 
            
            mapping steps.trends
            signal(8800 (10.0.0.2 : 0):XX):Maximum (unit) - MIN_CHANNEL
            signal(8800 (10.0.0.2 : 0):XX):Maximum (unit) - MAX_CHANNEL

        '''
        dummyfld = wmc.wmc_data_field(name='dummy', number=0)
        colname = name_in_source
        fieldtype = dummyfld.fieldtype_channel_signal
        skip = name_in_source.lower() in ['time stamp(pc)']
        # find pattern (*(*)*)
        # find all (
        ileft = self.get_all_occ(name_in_source, '(')
        if len(ileft) >= 2:
            iright = self.get_all_occ(name_in_source, ')')
            if not (len(iright) == len(ileft)):
                raise ValueError('Unequal number of () in "%s"'%name_in_source)
            colname = colname[:ileft[0]] + colname[iright[1]+1:]
        ileft = self.get_all_occ(colname, '(')
        unit = '-'
        if len(ileft) == 0:
            unit = '-'
        elif len(ileft) == 1:
            iright = self.get_all_occ(colname, ')')
            if not (len(iright) == len(ileft)):
                raise ValueError('Unequal number of () in "%s"'%colname)
            unit = colname[ileft[0]+1:iright[0]]
            colname = colname[:ileft[0]] + colname[iright[0]+1:]
        else:
            raise ValueError('Unexpected number of () in "%s": %d'%(
                colname, len(ileft)))
        fieldname = colname.strip()
        if fieldname.lower() == 'total time':
            if verbose:
                print('Parse time column "%s"'%fieldname)
            fieldname = 'testtime'
            fieldtype = dummyfld.fieldtype_time
        elif fieldname.lower() == 'total cycles':
            if verbose:
                print('Parse counter column "%s"'%fieldname)
            fieldname = 'counter'
            fieldtype = dummyfld.fieldtype_counter
        elif fieldname.lower() == 'position':
            if verbose:
                print('Parse position column "%s"'%fieldname)
            fieldname = 'S01'
        elif fieldname.lower() == 'load':
            if verbose:
                print('Parse force column "%s"'%fieldname)
            fieldname = 'F01'
        elif fieldname.lower() == 'strain':
            if verbose:
                print('Parse strain column "%s"'%fieldname)
            fieldname = '001S000'
        elif fieldname.lower() == 'stress':
            if verbose:
                print('Parse stress column "%s"'%fieldname)
            fieldname = 'stress'
        elif fieldname.lower() in ['cycle elapsed time', 'elapsed cycles'
            , 'step', 'time stamp', 'total cycle count']:
            if verbose:
                print('Parse stress column "%s"'%fieldname)            
            fieldname = fieldname.replace(' ', '_')
            fieldtype = dummyfld.fieldtype_other_signal
            skip=True
        else:
            if verbose:
                print('Parse unknown column "%s"'%fieldname.lower())            
        
        return wmc.wmc_data_field(icol, fieldname, fieldtype=fieldtype
                , name_in_source=name_in_source
                , channelname=fieldname, skip=skip)

    def _unit_from_label(self, name_in_source, verbose=False):
        '''
        :purpose: obtain unit from last string between ()
        
        :details: error handling done in obtaining field and channel name
        '''
        colname = name_in_source
        # find pattern (*(*)*) and strip it
        # find all (
        ileft = self.get_all_occ(colname, '(')
        if len(ileft) >= 2:
            # find all )
            iright = self.get_all_occ(colname, ')')
            # remove the found part
            colname = colname[:ileft[0]] + colname[iright[1]+1:]
        ileft = self.get_all_occ(colname, '(')
        # find pattern (*) and obtain unit from it
        unit = '-'
        if len(ileft) == 0:
            return '-'
        elif len(ileft) == 1:
            iright = self.get_all_occ(colname, ')')
            return colname[ileft[0]+1:iright[0]]
