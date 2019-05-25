.. _py_tikz_labels_doc:

Manage labels to pyTikZ object (labels object)
**********************************************

Each shape, assembly... is associated with a one or more labels or layers. Using the active property of the label 
is possible to manage to draw or not the shapes associated with such labels and filter by them. Initially every 
shape created is created with the label **default** that can be manage as any other label.

Load main **pyTikZ** class as follow and add, edit, desactive and manage labels of the different shapes:

.. code-block:: python
    :linenos:

    ### Load pyTikZ library
    import pyTikZ as py_tikZ
    import os, sys

    ### Load main object
    tikZ = py_tikZ.load()

    ### Add point at x=0, y=0, z=0
    p0 = tikZ.pto.pto(0,0,0)

    ### Add point at x=1, y=1, z=1
    p1 = tikZ.pto.pto(1,1,1)

    ### Add a line for example
    l1 = tikZ.shp.line(p0, p1)
    l1.addlabel = "patatin"

    l2 = tikZ.shp.line(p1, p0)
    l2.addlabel = "patatan"

    ### Labels
    print tikZ.lbl.list_active_labels(active = True)  ## Return list of active labeels

    tikZ.lbl["patatin"].active = False                ## Inactive a label

    print tikZ.lbl.list_active_labels(active = False) ## Return list of inactive labeels
   
and start bulding yor drawing.  More examples on how to use the labels object 
can be found in :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.

Labels functions. Class -> pyTikZ.lbl
-------------------------------------

.. _py_tikz_labels:
.. currentmodule:: cls_labels
.. autoclass:: _labels
   :members:
 
