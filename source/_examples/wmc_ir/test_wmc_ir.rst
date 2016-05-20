.. _test_wmc_ir:

How to use wmc_ir
*****************

Examples of how to use infrared images toolkit wmc_ir to work with
infrared images and sequences from the FLIR thermocamera.

* :ref:`Example 1 Open save FPF images<ex_wmc_ir_1>`
* :ref:`Example 2 Open save FFF images and coverted to FPF<ex_wmc_ir_2>`
* :ref:`Example 3 Open conver sequence file SEQ into FFF images<ex_wmc_ir_3>`
* :ref:`Example 4 Open convert sequence file SEQ into SEQ object ir_seq_obj <ex_wmc_ir_4>`

Example 1. Open save FPF images
-------------------------------

.. _ex_wmc_ir_1:

**Test code:**

.. literalinclude:: /_examples/wmc_ir/test_wmc_ir_fpf.py
    :linenos:
    :language: python

**This would output:**  

.. include:: /_examples/wmc_ir/test_wmc_ir_fpf.testout
   :literal:  

Example 2. Open save FFF images and coverted to FPF
---------------------------------------------------
   
.. _ex_wmc_ir_2:

**Test code:**

.. literalinclude:: /_examples/wmc_ir/test_wmc_ir_fff.py
    :linenos:
    :language: python

**This would output:**  

.. include:: /_examples/wmc_ir/test_wmc_ir_fff.testout
   :literal:   
   
Example 3. Open convert sequence file SEQ into FFF images
---------------------------------------------------------
   
.. _ex_wmc_ir_3:

**Test code:**

.. literalinclude:: /_examples/wmc_ir/test_wmc_ir_seq.py
    :linenos:
    :language: python

**This would output:**  

.. include:: /_examples/wmc_ir/test_wmc_ir_seq.testout
   :literal:  

Example 4. Open convert sequence file SEQ into SEQ object **ir_seq_obj**
------------------------------------------------------------------------
   
.. _ex_wmc_ir_4:

**Test code:**

.. literalinclude:: /_examples/wmc_ir/test_wmc_ir_seq_obj.py
    :linenos:
    :language: python

**This would output:**  

.. include:: /_examples/wmc_ir/test_wmc_ir_seq_obj.testout
   :literal:       
