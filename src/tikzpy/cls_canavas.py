# python3
# FLC 2014

class _canavas(object):

    """**Groups object:**

    .. _canavas_cls:

    :platform: Unix, Windows
    :synopsis: For a given list of points and shapes, treat them as a group and defines the canavas cube that contain them.

    :properties:
        * Get a group by unique id. (grp = tikzpy.grp[id])
        * Set values to a group by the unique id. (tikzpy.grp[id]=pto). The shape or point will be added.

    """

    """
        For the furture:
            * Move, rotate, scale ... -- Discarded, is shapes do it with group of points
            * Resume of unique points -- May 2016
            * General shape properties -- Discarded, is shapes do it with group of points
            * Max, min and canavas points
    """

    def __init__(self, parent):

        self.parent = parent
        self._grps = {}

    def __getitem__(self, key):

        return self.group(key)

    def __setitem__(self, key, value):

        grp = self.group(key)
        grp._add_elements(key, value)

    ######################### Functions
    def log(self, txt, ref = ""):
        self.parent.log(txt, ref = ref)

    def error(self, txt, ref = ""):
        self.parent.error(txt, ref = ref)

    def group(self, key):

        if key in self._grps:
            return self._grps[key]
        else:
            self.error("The alias name of the group does not exist. Create a new one.", ref = "01")

    def addgroup(self, key):

        """
        .. _groups_addgroup:

        **Synopsis:**
            * Creates a new group with a give name

        **Args:**
            * key: unique name of the group

        **Returns:**
            * A group object (see :ref:`group <py_tikz_group>`)

        .. note::

            * See :doc:`groups examples </_examples/tikzpy_groups/test_gen>`.

        """

        if key in self._grps:
            self.error("The alias name of the group does already exist", ref = "02")
        else:
            self._grps[key] = _group(self, key)

        return self.group(key)

    def _auxgroup(self):

        return _group(self, None)

    ###################################################################
    ###################################################################
    ###################################################################

class _group(object):

    """**Group object:**

    .. _group_cls:

    :platform: Unix, Windows
    :synopsis: Group object that contains the ids of points and shapes previously added. Allows to operate with them as a group.

    **Properties**

        :ivar id: get the unique key identificator
        :ivar add: add a point, shape or list of them
        :ivar ptos: return a list of the added points
        :ivar shps: return a list of the added shapes
        :ivar ptos_of_shapes: return a list of unique points forming the shapes
        :ivar all_ptos: return a list of unique points forming the shapes and added points

    """

    def __init__(self, parent, key):

        """
        Object groups

        """
        self.parent = parent
        self._key = key ### Parent dictionary key
        self._ptos = []
        self._shps = []

    ######################### Properties
    @property
    def id(self):
        return self._key

    @property
    def add(self, value):
        pass

    @add.setter
    def add(self, value):
        self.add_elements(value)

    @property
    def ptos(self):
        ### Returns a copy of the points ids
        #return self._ptos[:]
        return self._ptos_list_objects(self._ptos)

    @property
    def shps(self):
        ### Returns a copy of the shapes ids
        #return self._shps[:]
        return self._shps_list_objects(self._shps)

    @property
    def ptos_of_shapes(self):
        lst_ids = self._unique_points_of_shapes(self._shps, _initialpoints = [])
        return self._ptos_list_objects(lst_ids)

    @property
    def all_ptos(self):
        lst_ids = self._unique_points_of_shapes(self._shps, _initialpoints = self._ptos)
        return self._ptos_list_objects(lst_ids)

    ######################### Functions
    def log(self, txt, ref = ""):
        self.parent.log(txt, ref = ref)

    def error(self, txt, ref = ""):
        self.parent.error(txt, ref = ref)

    def canvas(self, ptos = None):
        """
        .. _groups_canvas:

        **Synopsis:**
            * Return the canavas plane positions that contain the list of points

        **Args:**
            * ptos = None: list of points. If none given use all_ptos.

        **Returns:**
            * [[min_x,max_x],[min_y,max_y],[min_z,max_z]] absolute position of the canavas coordinates

        """

        if ptos is None:
            _ptos = self.all_ptos
        else:
            _ptos = ptos

        size_x, size_y, size_z, max_size, _canavas = self.parent.parent.pto._canavas_size(_ptos)
        [[min_x,max_x],[min_y,max_y],[min_z,max_z]] = _canavas

        return [[min_x,max_x],[min_y,max_y],[min_z,max_z]]

    def _ptos_list_objects(self, lst_ids):
        ### Return a list of points object from a list of points ids
        _lst = []

        for id in lst_ids:
            _lst.append(self.parent.parent.pto[id])

        return _lst

    def _shps_list_objects(self, lst_ids):
        ### Return a list of shapes objects from a list of shapes ids
        _lst = []

        for id in lst_ids:
            _lst.append(self.parent.parent.shp[id])

        return _lst

    def _unique_points_of_shapes(self, _shps, _initialpoints = []):
        ### Return a list of unique poits ids from a list of shapes

        _lst = _initialpoints[:]

        # Iterate shapes
        for id in _shps:
            # Iterate shape points
            for _pto in self.parent.parent.shp[id].addpto:
                _id = _pto.id
                if _id not in _lst:
                    _lst.append(_id)

        return _lst

    def _choices_pto_shp(self, value):
        ### Points given by id, alias, or object
        ### Shapes given by id or object
        id = ""
        ttype = -1

        if type(value) == self.parent.parent.pto._type_of_point():
            ### Is point by object
            ttype = 0
            id = value.id
        elif type(value) == self.parent.parent.shp._type_of_shape():
            ### Is shape by object
            ttype = 1
            id = value.id
        elif type(value) == type(""):
            if value[0] == "#":
                ### Is shape or point by id
                if value[:2] == "#s":
                    ### Is shape by id
                    ttype = 1
                    id = self.parent.parent.shp[value].id
                else:
                    ### Is point
                    ttype = 0
                    id = self.parent.parent.pto._choices(value).id
            else:
                self.error("Wrong type of element or id given to the group.", ref = "05")
        else:
            self.error("Wrong type of element or id given to the group.", ref = "04")

        return ttype, id

    def add_elements(self, value):
        ### Add elements points or shapes in a list or not
        ### Points given by id, alias, or object
        ### Shapes given by id or object

        def _add_specific(self, ttype, id):
            if ttype == 0:
                if id not in self._ptos:
                    self._ptos.append(id)
            elif ttype == 1:
                if id not in self._shps:
                    self._shps.append(id)
            else:
                self.error("Ooops. Wrong type.", ref = "06")

        ### Iterate list of just value
        if type(value) == type([]):
            for val in value:
                ttype, id = self._choices_pto_shp(val)
                _add_specific(self, ttype, id)
        else:
            ttype, id = self._choices_pto_shp(value)
            _add_specific(self, ttype, id)

    def _add_elements(self, key, value):
        ### Internal add checking the key
        if key == self._key:
            self.add_elements(value)
        else:
            self.error("The element key does not agree.", ref = "03")
