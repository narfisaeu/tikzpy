.. _py_tikz_index_doc:
.. tikzpy documentation master file, created by
   sphinx-quickstart on Sat Oct 26 21:37:59 2013.

Welcome to **tikzpy** documentation!
====================================

Intro
=====
Documentation of **tikzpy**. Build your **TikZ** drawings for latex with python.
**tikzpy** is a python library that helps to build your tikZ pictures using python, instead of using directly tikZ sintaxis.

Main Index
==========

    * Main **tikzpy** class

        * **tikzpy** object which contains the drawing info

            * :doc:`tikZ = tikzpy.pytikz() <_00_pytikZ>`

        * **Points:** add and edit reference spatial points in a 3D space

            * **points** :doc:`tikZ.pto <_01_pytikZ_points>`

        * **2D shapes:** add and edit 2D shapes and text in a 3D space

            * **shapes** :doc:`tikZ.shp <_02_pytikZ_shapes>`

        * **plots:** buld-in plots based on tikzpy

            * **plots** :doc:`tikZ.plots <_03_pytikZ_plots>`

        * **labels:** add, edit, desactive labels of the different shapes

            * **labels** :doc:`tikZ.lbl <_04_pytikZ_labels>`

        * **colors:** add and define custom colors and transparencies

            * **colors** :doc:`tikZ.col <_05_pytikZ_colors>`

        * **groups:** add points and shapes to a group and operate with such container

            * **groups** :doc:`tikZ.grp <_06_pytikZ_groups>`

    * Utilities included in **tikzpy**

        * **files crawler:** utility to crawl files by extension or name in folders

            * **files_crawl** :doc:`tikzpy.files_crawl <_files_crawl>`

    Or check the :ref:`reference index <py_tikz_reference_index_doc>`

First steps **tikzpy**
======================

    First steps and introductory examples on how to use tikzpy can be found in this section.

    * **tikzpy: tikZ = tikzpy.pytikz()** --> :doc:`main class examples <_00_pytikZ>`

    * **Points: tikZ.pto** --> :doc:`points examples </_examples/tikzpy_points/test_gen>`

    * **2D shapes: tikZ.shp** --> :doc:`shapes examples </_examples/tikzpy_shapes/test_gen>`

    * **build-in plots:** --> :doc:`plots examples </_examples/tikzpy_plots/test_gen>`

    * **labels:** --> :doc:`labels examples </_examples/tikzpy_labels/test_gen>`

    * **colors: tikZ.col** --> :doc:`colors examples </_examples/tikzpy_colors/test_gen>`

    * **groups: tikZ.grp** --> :doc:`group examples </_examples/tikzpy_groups/test_gen>`

Requirements or pre-requisites
==============================

    * Install **Latex** in Windows:

        * Install MikTex (miktex.org)

    * Install **Latex** in Ubuntu:

        * sudo apt-get install texlive-full
        * sudo apt-get install xzdec
        * sudo tlmgr install pgf
        * sudo tlmgr install tikz-cd

    * Packages: **tikz, tikz-3dplot**

    * TikZ libraries: **shapes,arrows,decorations, decorations.pathmorphing,arrows.meta,patterns**

    * Recomended to install **ImageMagik** and **Ghostscript** for png creation in Windows

Gallery of drawings and pictures performed using **tikzpy**
===========================================================

    Code examples of drawings and pictures carried out using **tikzpy**.
    Contact and send us your drawings based of **tikzpy** if you want them to be included in this section.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
