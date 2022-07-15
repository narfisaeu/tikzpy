.. _py_tikz_groups_doc:

Add shapes and points to a group entity and operate as one
**********************************************************

Load main **tikzpy** class as follow and create points and shapes and add it to a group:

.. code-block:: python
   :linenos:

   import tikzpy

   ### Load main object
   tikZ = tikzpy.pytikz()

   ### Add point at x=0, y=0, z=0
   p0 = tikZ.pto.pto(0,0,0)

   ### Add point at x=1, y=1, z=1
   p1 = tikZ.pto.pto(1,1,1)

   ### Create a group
   grp = tikZ.grp.addgroup("grp1")

   ### Add shapes or points to a group
   grp.add = tikZ.shp.line(p0, p1, color = "custom_color")
   grp.add = p0
   grp.add = p1



and start bulding your drawing. More examples on how to use the group object
can be found in :doc:`groups examples </_examples/tikzpy_groups/test_gen>`.

Groups functions. Class -> tikzpy.grp
-------------------------------------

.. _py_tikz_groups:
.. currentmodule:: cls_canavas
.. autoclass:: _canavas
   :members:

.. _py_tikz_group:
.. currentmodule:: cls_canavas
.. autoclass:: _group
   :members:
