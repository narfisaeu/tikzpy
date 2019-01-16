.. _py_tikz_index_doc:
.. pyTikZ documentation master file, created by
   sphinx-quickstart on Sat Oct 26 21:37:59 2013.

Welcome to **pyTikZ** documentation!
====================================

Intro
=====
Documentation of **pyTikZ**. Build your **TikZ** drawings for latex with python.
**pyTikZ** is a python library that helps to build your tikZ pictures using python, instead of using directly tikZ sintaxis.

Main Index
==========

    * Main **pyTikZ** class

        * **pyTikZ** object which contains the drawing info

            * :doc:`tikZ = pyTikZ.pytikz() <_00_pytikZ>`

        * **Points:** add and edit reference spatial points in a 3D space

            * **points** :doc:`tikZ.pto <_01_pytikZ_points>`

        * **2D shapes:** add and edit 2D shapes and text in a 3D space

            * **shapes** :doc:`tikZ.shp <_02_pytikZ_shapes>`

        * **plots:** buld-in plots based on pyTikZ

            * **plots** :doc:`tikZ.plots <_03_pytikZ_plots>`

        * **labels:** add, edit, desactive labels of the different shapes

            * **labels** :doc:`tikZ.lbl <_04_pytikZ_labels>`

        * **colors:** add and define custom colors and transparencies

            * **colors** :doc:`tikZ.col <_05_pytikZ_colors>`

        * **groups:** add points and shapes to a group and operate with such container

            * **groups** :doc:`tikZ.grp <_06_pytikZ_groups>`

    * Utilities included in **pyTikZ**

        * **files crawler:** utility to crawl files by extension or name in folders

            * **files_crawl** :doc:`pyTikZ.files_crawl <_files_crawl>`

    Or check the :ref:`reference index <py_tikz_reference_index_doc>`

First steps **pyTikZ**
======================

    First steps and introductory examples on how to use pyTikZ can be found in this section.

    * **pyTikZ: tikZ = pyTikZ.pytikz()** --> :doc:`main class examples <_00_pytikZ>`

    * **Points: tikZ.pto** --> :doc:`points examples </_examples/pytikZ_points/test_gen>`

    * **2D shapes: tikZ.shp** --> :doc:`shapes examples </_examples/pytikZ_shapes/test_gen>`

    * **build-in plots:** --> :doc:`plots examples </_examples/pytikZ_plots/test_gen>`

    * **labels:** --> :doc:`labels examples </_examples/pytikZ_labels/test_gen>`

    * **colors: tikZ.col** --> :doc:`colors examples </_examples/pytikZ_colors/test_gen>`

    * **groups: tikZ.grp** --> :doc:`group examples </_examples/pytikZ_groups/test_gen>`

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

Gallery of drawings and pictures performed using **pyTikZ**
===========================================================

    Code examples of drawings and pictures carried out using **pyTikZ**.
    Contact and send us your drawings based of **pyTikZ** if you want them to be included in this section.

    :doc:`Visit the gallery <_00_pytikZ>`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
