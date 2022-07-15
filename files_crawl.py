
#!/usr/bin/python
# FLC 2013

import os, sys, copy

##############################################
### Lib log functions

def lib_log(txt, Error = 0, Id = 78):
    ### Log bottle neck
    print( "Log: %s" % txt)

def lib_error(txt, out=False, Id = 78):
    ### Error bottle neck
    print( "Error: %s" % txt)

##############################################
### Supplier of files functions

def load_obj_files():

    """

    .. _load_obj_files:

    **Synopsis:**
        * Returns empty files object

    :Dependences: None

    **Args:**
        * None

    **Optional parameters:**
        * None

    **Returns:**
        * Empty files object

    **Error:**
        * Not handle

    .. note::

        * None

    """

    return _files()

def read_folder_list_file_multi(folder, extNoPoint = [""], prefix = "", max_recursive_level = 0, data = False):

        """

        .. _read_folder_list_file_multi:

        **Synopsis:**
            * Returns a list of paths to images in a folder
            * Filtered by extension images and / or filter by a prefix

        :Dependences: None

        **Args:**
            * folder: folder to crawl

        **Optional parameters:**
            * extNoPoint = [""]: list or extension or single extension to filter. Example extNoPoint = ["jpg", "png"] or extNoPoint = "jpg"
            * prefix = "": prefix to filter. Example prefix = "000"
            * max_recursive_level = 0: maximum hycherarchy level of recursivity form folder to look in subfolders
            * data = False: populate extra data

        **Returns:**
            * List of object images (see :ref:`obj_files()<obj_files_00>`)

        **Error:**
            * Not handle

        .. note::

            Attributes of object images:

            * obj_images[index].path
            * obj_images[index].folder
            * obj_images[index].file_name
            * obj_images[index].extension
            * obj_images[index].file_name_noExt
            * obj_images[index].path_noExt
            * Is iterable

        """

        ### extension
        if type(extNoPoint) is type([]):
            _extNoPoint = extNoPoint
        else:
            _extNoPoint = [extNoPoint]

        m_lst = read_folder_list_files(folder, extNoPoint = _extNoPoint[0], \
                            prefix = prefix, max_recursive_level = max_recursive_level, data = data)

        for ext in range(1, len(_extNoPoint)):

            m_lst = m_lst + read_folder_list_files(folder, extNoPoint = ext, \
                                                           prefix = prefix, max_recursive_level = max_recursive_level, data = data)

        return m_lst

def read_folder_list_files(folder, extNoPoint, prefix = "", max_recursive_level = 0, data = False, case_sensitive = False):

    """

    .. _read_folder_list_files:

    **Synopsis:**
        * Returns a list of paths to files in a folder
        * Filtered by extension images and / or filter by a prefix

    :Dependences: None

    **Args:**
        * folder: folder to look in
        * extNoPoint: single extension to filter, for example extNoPoint = "jpg"

    **Optional parameters:**
        * prefix = "": prefix of files to filter with
        * max_recursive_level = 0: maximum hycherarchy level of recursivity from starting folder to look in subfolders
        * data = False: populet extra data

    **Returns:**
        * List of object images (see :ref:`obj_files()<obj_files_00>`)

    **Error:**
        * Not handle

    .. note::

        Attributes of object images:

        * obj_images[index].path
        * obj_images[index].folder
        * obj_images[index].file_name
        * obj_images[index].extension
        * obj_images[index].file_name_noExt
        * obj_images[index].path_noExt
        * Is iterable
        * Is case sensitive

        See :ref:`Example 1<ex_files_crawl>`

    """

    ### Reads folder recursevely and filter by extension and prefix
    ### Returns images object

    ### Get the reference
    top_folder = folder

    ### Start object
    images =  _files()

    _rec_read_folder_list_files(folder, extNoPoint, images, top_folder,
                                prefix = prefix, max_recursive_level = max_recursive_level, data = data)

    return images

##############################################
### Other files functions

def _rec_read_folder_list_files(folder, extNoPoint, images, top_folder, prefix = "", max_recursive_level = 0, data = False):

    ### Recursive function

    if not os.path.isdir(folder): lib_log(txt = "Folder do not exists: %s" % folder, Error = 0)

    for file in os.listdir(folder):

        fname = os.path.basename(file)
        ext = os.path.splitext(fname)[1]

        if ext[1:] == extNoPoint and fname.startswith(prefix):

            __path = os.path.join(folder, fname)
            images.set_by_path(__path)
        else:
            sub_folder = os.path.join(folder, fname)

            if os.path.isdir(sub_folder):

                level = _find_level(top_folder, sub_folder)

                if level <= max_recursive_level and max_recursive_level > 0:

                    _rec_read_folder_list_files(sub_folder, extNoPoint, images, top_folder,
                                                prefix = prefix, max_recursive_level = max_recursive_level, data = data)

def _find_level(top_folder, folder):

    ### Find the level hycherachy level btw top_folder and folder

    level = 0
    root = os.path.splitdrive(top_folder)
    if root[0] != os.path.splitdrive(folder)[0]:
        lib_log(txt = "Not even roots", Error = 1)
        return -1

    start_folder = folder
    if start_folder == top_folder:
        return level

    while True:

        level = level + 1

        start_folder = os.path.abspath(os.path.join(start_folder, os.pardir))

        if start_folder == top_folder:
            break

        if start_folder == root:
            break

    return level

class _file(object):

    ###
    ###  Single file object
    ###

    def __init__(self, parent, __path):

        self._path = ""
        self._parent = parent

        self._ini_others()

        self.path = __path

    def _ini_others(self):
        self.folder_idx = ""
        pass

    def __str__(self):

        txt = []
        txt.append(self._path)
        txt.append(self.folder_idx)

        return str(txt)

    def __get__(self, instance, owner):

        return self

    def __set__(self, instance, value):

        self.path = value

    @property
    def path(self):

        return os.path.join(self.folder, self._path)

    @path.setter
    def path(self, value):

        folder = os.path.dirname(value)
        file = os.path.basename(value)

        idx = self._parent._folders.set_by_path(folder)
        if idx < 0: return

        self._path = file
        self._ini_others()

        self.folder_idx = idx

    @property
    def folder(self):

        return self._parent._folders[self.folder_idx].path

    @property
    def file_name(self):

        return os.path.basename(self.path)

    @property
    def extension(self):

        return os.path.splitext(self.file_name)[1]

    @property
    def file_name_noExt(self):

        return os.path.splitext(self.file_name)[0]

    @property
    def path_noExt(self):

        return os.path.splitext(self.path)[0]

class _files(object):

    """

       .. _obj_files_00:

       Object files

       :platform: Unix, Windows
       :synopsis: Container of files paths names
       :get: **obj[index].path**: return the full path to the file
       :get: **obj[index].folder**: return the folder of the file
       :get: **obj[index].file_name**: return the file name
       :get: **obj[index].extension**: return the file extension
       :get: **obj[index].file_name_noExt**: return file name without extension *basename*
       :get: **obj[index].path_noExt**: return path without extension
       :get: **obj.folders**: list of folders indexed

       .. note::

            * Paths are indexed as a list so it can be use as a list
            * Use **obj[index].property** or **obj[index].function**
            * Is iterable (not reversed)
            * Methods as len and print emulates lists behaviour
            * Objects can be added

        .. seealso::

            * see :ref:`read_folder_list_files()<read_folder_list_files>`

    """

    def __init__(self):

        self._lst = []
        self._folders = _folders()

    def __str__(self):

        txt = []
        for ls in self._lst:
            txt.append(str(ls))

        return str(txt)

    def _new(self, path):
        ## add entry

        if not os.path.isfile(path): return -1

        self._lst.append(_file(self, os.path.abspath(path) ))

        return len(self._lst) - 1 ## index

    def get_index_by_path(self, path):
        """

        .. _get_index_by_path_00:

        **Synopsis:**
            * Get index by path, if is not indexed return -1

        **Args:**
            * path: full path to file

        **Returns:**
            * Index of the path

        """

        ## get index by specific path or -1 No
        No = -1

        if len(self._lst) == 0: return No

        inn = False
        for ii in range(0, len(self._lst)):

            if self._lst[ii].path == path:
                inn = True
                break

        if inn:
            return ii
        else:
            return No

    def set_by_path(self, path):

        """

        .. _set_by_path_00:

        **Synopsis:**
            * Add a new path if is not indexed already

        **Args:**
            * path: full path to file

        **Returns:**
            * Index of the path.
            * If files does not exist returns -1 and is not added

        """

        ## set main item value
        ## set data as obj[5].data

        idx = self.get_index_by_path(path)

        if idx < 0:
            idx = self._new(path)
        else:
            pass
            #self._lst[idx].path = path

        return idx

    def index_exists(self, key):
        """

        .. _index_exists_00:

        **Synopsis:**
            * Check if an index is valid

        **Args:**
            * key: index to the path

        **Returns:**
            * True / False

        """

        ## Check index exists

        if key >= 0 and key < len(self._lst):
            return True
        else:
            return False

    def __len__(self):
        ## len items

        return len(self._lst)

    def __getitem__(self, key):
        ## return main value of item
        ## return data as obj[5].data
        if self.index_exists(key):
            return self._lst[key]
        else:
            return _file(self, "")

    def __setitem__(self, key, value):
        ## set main item value
        ## set data as obj[5].data

        if not self.index_exists(key):
            idx = self._new(value)
        else:
            self._lst[key].path = value

    def __delitem__(self, key):

        return
        #del self._lst[key]

    def __iter__(self):

        return iter(self._lst)

    def __add__(self, obj_files):

        buff = copy.deepcopy(self)

        for xx in obj_files:

            buff.set_by_path(xx.path)

        return buff

    @property
    def folders(self):

        lst = []

        for ff in self._folders:

            lst.append(ff.path)

        return lst

class _folder(object):

    ###
    ### Single folder object
    ###

    def __init__(self, path):

        self._path = path
        self._ini_others()

    def _ini_others(self):
        self.other = ""
        pass

    def __str__(self):

        txt = []
        txt.append(self.path)
        txt.append(self.other)

        return str(txt)

    def __get__(self, instance, owner):

        return self

    def __set__(self, instance, value):

        self.path = value

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value
        self._ini_others()

class _folders(object):

    ###
    ### Folders of folder
    ###

    def __init__(self):

        self._lst = []

    def __str__(self):

        txt = []
        for ls in self._lst:
            txt.append(str(ls))

        return str(txt)

    def _new(self, path):
        ## add entry

        self._lst.append(_folder(path))

        return len(self._lst) - 1 ## index

    def get_index_by_path(self, path):
        ## get index by specific path or -1 No
        No = -1

        if len(self._lst) == 0: return No

        inn = False
        for ii in range(0, len(self._lst)):

            if self._lst[ii].path == path:
                inn = True
                break

        if inn:
            return ii
        else:
            return No

    def set_by_path(self, __path):
        ## set main item value
        ## set data as obj[5].data

        idx = self.get_index_by_path(__path)

        if idx < 0:
            idx = self._new(__path)

        else:
            self._lst[idx].path = __path

        return idx

    def index_exists(self, key):
        ## Check index exists

        if key >= 0 and key < self._lst[ii]:
            return True
        else:
            return False

    def __len__(self):
        ## len items

        return len(self._lst)

    def __getitem__(self, key):
        ## return main value of item
        ## return data as obj[5].data

        return self._lst[key]

    def __setitem__(self, key, value):
        ## set main item value
        ## set data as obj[5].data

        if not self.index_exists(key):
            idx = self._new(value)
        else:
            self._lst[key].path = value

    def __delitem__(self, key):

        return
        #del self._lst[key]

    def __iter__(self):

        return iter(self._lst)

    def __add__(self, obj_files):

        buff = copy.deepcopy(self)

        for xx in obj_files:

            buff.set_by_path(xx.path)

        return buff
