version='20190104.10681'
'''
environment specific data for wmclib and minilablib
'''

import os
import sys
import datetime
import numpy as np
import time

savefig_logo_text  = 'Knowledge Centre WMC'
savefig_logo_color = '#003F87'
savefig_logo_style = 'oblique'
savefig_logo_size  = 'small'
savefig_logo_x  = 0.995
savefig_logo_y  = 0.005

sql_host = '192.168.1.233'
sql_default_database = 'temperatuur_log'
sql_user     = 'lamineer_kelder'
sql_password = 'lamineer_kelder'
sql_port     = '5450'
# functions...


def join_caseinsensitive(a, b, verbose = True, halt_on_not_found = True):
    """
    Internal helper function to join two path part's.
    
    (function is needed because we mixed up case sometimes)
    """
    
    m = os.path.join(a, b)
    if os.path.exists(m):
        return m

    u = os.path.join(a, str(b).upper())
    if os.path.exists(u):
        return u
        
    l = os.path.join(a, str(b).lower())
    if os.path.exists(l):
        return l
    
    paths = os.listdir(a)
    paths_dict = dict([(name.lower(),name) for name in paths])
    if b.lower() in paths_dict:
        m = os.path.join(a, paths_dict[b.lower()])    
        if os.path.exists(m):
            return m
    
    if halt_on_not_found:
        raise ValueError('\nCould not find a joined path for:\n %s and %s' % 
                          (a, b))
    else:
        return None


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
    
    if verbose:
        print('Trying to locate measurement directory for:')
        print(' identification : %s' % identification)
        print(' project        : %s' % project)
        print(' tvct           : %s' % tvct)
        if series:
            print(' series         : %s' % series)
            

    # add platform specific stuff to the path
    if 'darwin' in sys.platform.lower():          
        raise ValueError('Mac OS not yet supported at WMC.')
    if 'win' in sys.platform.lower():
        datadir = 'M:\_MINILAB\projects'
        if not os.path.isdir(datadir):
            # probably new samba share
            datadir = 'M:\projects'
    elif 'linux' in sys.platform.lower():
        datadir = '/media/m/_MINILAB/projects'  # ....
    else:
        raise ValueError('Not on linux or Windows platform (i think).')

    # add project specific stuff to the path
    if project and ( 'rnd'     in project.lower() or
                     'upwind'  in project.lower() or
                     'innwind' in project.lower()    ) :
        datadir = join_caseinsensitive(datadir, 'eu_ez')
        datadir = join_caseinsensitive(datadir, 'inn-up')
    elif project and 'internal' in project.lower():
        datadir = join_caseinsensitive(datadir, 'internal')
    else:
        datadir = join_caseinsensitive(datadir, 'ind')
    
    # buffer the root
    datadir_root = datadir
    
    # add general stuff to the path
    datadir = join_caseinsensitive(datadir, tvct)
    
    datadir = join_caseinsensitive(datadir, identification, halt_on_not_found = False)
    
    # maybe we need also a series
    if not datadir:
        if series:
            print('Mapping by identification not found')
            datadir = datadir_root
            datadir = join_caseinsensitive(datadir, tvct)
            datadir = join_caseinsensitive(datadir, series) 
            datadir = join_caseinsensitive(datadir, identification)    
    
    # and we're done 
    if verbose and datadir:
        print('Found : %s\n'% datadir)
    else:
        raise ValueError('Source directory not found')
    return datadir
    
# ==== WMClib Ambient temperature function ==========================
# ===================================================================

def ambient_temp(location, start_date, end_date):
    '''
    
    retrieve the readings from database.
    
    Arguments:
        *location*:
            'hal', 'minilab', 'lamineerruimte'
            
    The result is returned as a dictionary.
    '''
    import psycopg2
    # check first argument
    if location not in ['hal', 'minilab', 'lamineerruimte']:
        raise(ValueError('location should be hal, minilab or lamineerruimte'))
    
    stop_date = end_date
    # we want a time difference of a least 15 minutes
    if stop_date - start_date < datetime.timedelta(0,900):
        stop_date = start_date + datetime.timedelta(0,900)
        
    # we have logged since  Oct 22nd 2014
    log_start = datetime.datetime(2014, 10, 22) 
    if start_date < log_start:
        raise(ValueError('Temperature log started Oct 22nd 2014 \n' +
                          ' No data for ' + repr(start_date)))


    cols = ['log_date', 'temperature', 'humidity', 'pressure', 'dewpoint']
    sql  = ' SELECT '
    sql +=  ', '.join(cols)
    sql += ' FROM ' + location + ' WHERE log_date >= %s AND log_date <= %s'
    sql += ' ORDER BY log_date ASC '
    sql += ' ; '
    conn = psycopg2.connect(host     = sql_host,
        database = sql_default_database,
        user     = sql_user, 
        password = sql_password,
        port     = sql_port)
    cur = conn.cursor()

    # and retrieve the data, and make a nice numpy array
    cur.execute(sql, [start_date, stop_date])
    data = np.asarray(cur.fetchall())
    cur.close()
    conn.close()
    
    dct = {}
    
    for i, label in enumerate(cols):
        a = []
        for rec in data:
            x = rec[i]
            if label == 'log_date':
                x = np.double(time.mktime(x.timetuple()))
            a.append(x)
        dct[label] = np.array(a)
    
    return dct

def strain_gauge_props_from_channel(channel):
    '''
    :purpose: obtain dictionary of strain gauge properties from channel name
    '''
    ret = {}
    if len(channel) < 7:
        return
    s = channel[-7:]
    try:
        snumber = np.float(s[:3])
        ssubtype = s[3]
        sangle = s[4:]
        print('number="%s", type="%s", angle="%s"'%(snumber, stype, sangle))
        if not (stype in ['S', 'R', 'C']):
            return ret
        fnumber = np.int(snumber)
        fangle = np.int(sangle)
        ret['subtype'] = stype
        ret['label'] = snumber
        ret['angle'] = sangle
    except:
        pass
    return ret



def props_from_channel_XNN(channel, type, labellength = 2):
    '''
    :purpose: obtain dictionary of strain gauge properties from channel name
    '''
    ret = {}
    required_length = len(type) + labellength
    if len(channel) == required_length:
        slabel = channel[-labellength:]
        stype = channel[:-labellength]
        if stype == type:
            try:
                flabel = np.int(slabel)
                ret['label'] = slabel
                ret['type'] = type
            except:
                pass
    return ret

def force_props_from_channel(channel):
    '''
    :purpose: obtain dictionary of strain gauge properties from channel name
    '''
    ret = props_from_channel_XNN(channel, type='F', labellength = 2)
    if 'type' in ret:
        return ret
    return {}

def displacement_props_from_channel(channel):
    '''
    :purpose: obtain dictionary of strain gauge properties from channel name
    '''
    ret = props_from_channel_XNN(channel, type='S', labellength = 2)
    if 'type' in ret:
        return ret
    return {}

def possible_pre_labels():
    '''
    :purpose: labels before channel name (in range-average file)
    '''
    return ['R_', 'A_']
