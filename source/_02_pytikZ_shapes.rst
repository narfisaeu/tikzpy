.. _py_tikz_shapes_doc:

Add 2D shapes in a 3D space to pyTikZ object (shapes object)
************************************************************

The shapes object allow to add 2D shapes to the pyTikZ object such as: 

    * Line between two points. See :ref:`shp.line <shapes_line>`
    * Path of multiple points. See :ref:`shp.path <shapes_path>`
    * Circle given by center and radius. See :ref:`shp.circle <shapes_circle>`
    * Arc given by starting point, radius and angles. See :ref:`shp.arc <shapes_arc>`
    * Text label. See :ref:`shp.text <shapes_text>`

Load main **pyTikZ** class as follow and create and edit spatial 2D shapes and text:

.. code-block:: python
   :linenos:

   import py_tikz as pytikz
   
   ### Load main object
   tikZ = py_tikZ.pytikz()
   
   ### Add point at x=0, y=0, z=0
   p0 = tikZ.pto.pto(0,0,0)
   
   ### Add point at x=1, y=1, z=1
   p2 = tikZ.pto.pto(1,1,1)   
   
   ### Add a line for example
   l1 = self.tikZ.shp.line(p0, p1)        
   l1.zorder = 1.1 ### Viewer Z-order
   
and start bulding your drawing. More examples on how to use the shapes object 
can be found in :doc:`shapes examples </_examples/pytikZ_shapes/test_gen>`.

Shapes functions. Class -> pyTikZ.shp
-------------------------------------

.. _py_tikz_shapes:
.. currentmodule:: cls_shapes
.. autoclass:: _shapes
   :members:
 
