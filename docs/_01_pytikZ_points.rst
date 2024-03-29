.. _py_tikz_points_doc:

Add spatial points to tikzpy object (points object)
***************************************************

Load main **tikzpy** class as follow and create and edit spatial points:

.. code-block:: python
    :linenos:

    ### Load tikzpy library
    import tikzpy

    ### Load main object
    tikZ = tikzpy.pytikz()
    # or
    tikZ = tikzpy.load()

    ### Add point at x=0, y=0, z=0
    p1 = tikZ.pto.pto(0.1,0.2,0.3, layer=0, alias='pto1')

    ### Add point at x=1, y=1, z=1
    p2 = tikZ.pto.pto(1,1,1, layer=0, alias='pto2')

    ### Vector between point 1 and 2
    vec = p2 - p1

    ### Access point variables
    x, y, z = p1.x, p1.y, p1.z


and start bulding your drawing.

More examples on how to use the points object can be found in :doc:`points examples </_examples/tikzpy_points/test_gen>`.

Points functions. Class -> tikzpy.pto
-------------------------------------

.. _py_tikz_points:
.. currentmodule:: cls_points
.. autoclass:: _points
   :members:
