.. _py_tikz_plots_doc:

Use one of the build-in plots included in tikzpy object (plots object)
**********************************************************************

Load main **tikzpy** class as follow and add a new plot:

.. code-block:: python
   :linenos:

   import tikzpy

   ### Load main object
   tikZ = tikzpy.pytikz()

   ### Add point at x=0, y=0, z=0
   p0 = tikZ.pto.pto(0,0,0)

   ### Add point at x=1, y=1, z=1
   p1 = tikZ.pto.pto(1,1,1)

   ### Assembly type racime
   rac = tik.asse.racime(group = 0)
   rac.l1 = 10.             #Add length 1 value
   rac.l2 = 5.              #Add length 2 value
   rac.l3 = 1.              #Add length 3 value
   rac.origin = p0          #Add point
   rac.add_element("Example", thickness = None, separation = None)
   rac.move(p1-p0)          #Move assembly
   rac.addlabel="patatin"   #Add a label

and start bulding your drawing. See more :doc:`plots examples </_examples/tikzpy_plots/test_gen>`.

Plots functions. Class -> tikzpy.plots
---------------------------------------

.. _py_tikz_plot:
.. currentmodule:: cls_plots
.. autoclass:: _plots
   :members:

Vertical bars plot
---------------------------------------

.. _py_tikz_bars_vertical:
.. currentmodule:: plots.cls_bars_vertical
.. autoclass:: _bars_vertical
  :members:

Vertical arrow plot
---------------------------------------

.. _py_tikz_arrow_vertical:
.. currentmodule:: plots.cls_arrow_vertical
.. autoclass:: _arrow_vertical
  :members:

.. autoclass:: cls_plots._assembly
  :members: load_data_buffer, draw_plot
