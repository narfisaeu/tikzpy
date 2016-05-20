.. _py_tikz_assembly_doc:

Add assemblies of shapes to pyTikZ object (assemblies object)
*************************************************************

Load main **pyTikZ** class as follow and add assemblies of shapes:

.. code-block:: python
   :linenos:

   import py_tikz as pytikz
   
   ### Load main object
   tikZ = py_tikZ.pytikz()
   
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
   
and start bulding your drawing.

Shapes functions. Class -> pyTikZ.asse
--------------------------------------

.. _py_tikz_assembly:
.. currentmodule:: cls_assembly
.. autoclass:: _assemblys
   :members:
 
