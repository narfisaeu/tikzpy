.. _ex_shapes:

How to use the shapes object **tikzpy.shp**
*******************************************

Examples of how to use the shape objects :ref:`tikzpy.shp <py_tikz_shapes_doc>`.

Example 1 - Thick property of shpes options
--------------------------------------------
.. _ex_shapes_thick:

The property thick applies to the thickness of the line and path shapes, as well as the contour border of 2D shapes such as
rectangles, circles, arc, grid and parabole.

**Available thicknesses values for property thick:**

    .. image:: test_shp_thick.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_thick.py
    :linenos:
    :language: python

Further bibliography pages 311 `TkZ-PGFmanual <http://www.texample.net/media/pgf/builds/pgfmanualCVS2012-11-04.pdf>`_

Example 2 - Type  property of shpes options
--------------------------------------------
.. _ex_shapes_type:

**Available types of line values for property type:**

The property type applies to the line decoration of line and path shapes, as well as the contour border of 2D shapes such as
rectangles, circles, arc, grid and parabole.

In the case of snake, zigzag, random and saw types is possible to modify the amplitude and the segment length adding the values
with an underscore line. As in the following examples:

    * type = "line type"
    * type = "line type_segment length"
    * type = "line type_segment length_amplitude"

    .. image:: test_shp_type.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_type.py
    :linenos:
    :language: python

Further bibliography pages 159,377 `TkZ-PGFmanual <http://www.texample.net/media/pgf/builds/pgfmanualCVS2012-11-04.pdf>`_

Example 3 - Color property options
----------------------------------
.. _ex_shapes_color:

**Available color inputs for the color property:**

The shapes color property can set in three different ways by the default names, by color tranparency, by a rgb definition or
custom colors can be added in the :ref:`colors object <colors_cls>`. As in the following examples:

    * color = "color name"          , Color name
    * color = "color1!30"           , Transparency of a color
    * color = "color1!30!color2"    , Tranparency between two colors
    * color = "r_g_b"               , RGB values. Scale 0-255.
    * color = "r_g_b_trans"         , RGB values + transparency. Scale 0-255.
    * calor = "custom name"         , names defined in the :ref:`colors object <colors_cls>`

note that can also be used the **transparent!30** color, to create transparencies.


    .. image:: test_shp_color.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_color.py
    :linenos:
    :language: python

Example 4 - Add points property addpto
--------------------------------------
.. _ex_shapes_addpto:

Points can be added to shapes in the followin formats:

    * addpto = point object , as a point object
    * addpto = [point object] , as a list of point objects
    * addpto = point.id , by point id
    * addpto = [point.id] , as a list of point ids
    * addpto = point.alias , by point id
    * addpto = [point.alias] , as a list of point alias

See the following example:

    .. image:: test_shp_addpto.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_addpto.py
    :linenos:
    :language: python

Example 5 - Text shape options
------------------------------
.. _ex_shapes_text:

See the following example:

    .. image:: test_shp_text.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_text.py
    :linenos:
    :language: python

Example 6 - Fill properties options
-----------------------------------
.. _ex_shapes_fill:

**Available fill inputs values for the fill property:**

By **color**, in a similar way that is color property (see :ref:`colors examples <ex_shapes_color>`)

    * fill = "color name"          , Color name
    * fill = "color1!30"           , Transparency of a color
    * fill = "color1!30!color2"    , Tranparency between two colors
    * fill = "r_g_b"               , RGB values. Scale 0-255.
    * fill = "r_g_b_trans"         , RGB values + transparency. Scale 0-255.
    * fill = "custom name"         , names defined in the :ref:`colors object <colors_cls>`

With a **pattern**

    * the pattern is create with the function :ref:`pattern_build(pattern,color) <shapes_pattern_build>`

With a **shade path** (see section 41 TikZ manual)

    * the shade path is create with the function

see following examples:

    .. image:: test_shp_fill.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_fill.py
    :linenos:
    :language: python

Example 7 - Grid shape options
------------------------------
.. _ex_shapes_grid:

See the following example:

    .. image:: test_shp_grid.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_grid.py
    :linenos:
    :language: python

Example 8 - Bitmap shape options
--------------------------------
.. _ex_shapes_bitmap:

See the following example:

    .. image:: test_shp_bitmap.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_bitmap.py
    :linenos:
    :language: python

Example 9 - Arrow tip types
---------------------------
.. _ex_shapes_arrow:

**Available arrow tips types:**

A selected list of arrow tips are listed below (extracted from page 311 pgfmanualCVS2012-11-04),

    .. image:: test_shp_arrow.tikz.png
       :width: 500px
       :align: center

Drawing created with the following tikzpy code:

.. literalinclude:: /_examples/tikzpy_shapes/test_shp_arrow.py
    :linenos:
    :language: python
