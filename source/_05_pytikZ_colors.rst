.. _py_tikz_colors_doc:

Add custom colors and filles to pyTikZ object (colors object)
*************************************************************

Load main **pyTikZ** class as follow and add colors to be used in 2D shapes and texts:

.. code-block:: python
   :linenos:

   import py_tikz as pytikz
   
   ### Load main object
   tikZ = py_tikZ.pytikz()
   
   ### Add point at x=0, y=0, z=0
   p0 = tikZ.pto.pto(0,0,0)
   
   ### Add point at x=1, y=1, z=1
   p2 = tikZ.pto.pto(1,1,1)   
   
   ### Define custom color
   tikZ.col["custom_color_rgb"] = "150_50_5"
   tikZ.col["custom_color"] = "red!50"
   
   ### Add a line for example
   l1 = self.tikZ.shp.line(p0, p1, color = "custom_color")        
      
and start bulding your drawing. More examples on how to use the colors object 
can be found in :doc:`colors examples </_examples/pytikZ_colors/test_gen>` 
as well as in the :ref:`color property examples <ex_shapes_color>`.

Colors functions. Class -> pyTikZ.col
-------------------------------------

.. _py_tikz_shapes:
.. currentmodule:: cls_colors
.. autoclass:: _colors
   :members:
 
