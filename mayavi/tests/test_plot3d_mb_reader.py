# Author: Suyog Dutt Jain <suyog.jain@aero.iitb.ac.in>
#         Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2008,  Enthought, Inc.
# License: BSD Style.

# Standard library imports.
from os.path import abspath
from StringIO import StringIO
import copy
import unittest

# Local imports.
from common import get_example_data

# Enthought library imports
from mayavi.core.null_engine import NullEngine
from mayavi.sources.plot3d_reader import PLOT3DReader
from mayavi.filters.select_output import SelectOutput
from mayavi.modules.outline import Outline

class TestPlot3dMbReader(unittest.TestCase):

    def setUp(self):
        """Initial setting up of test fixture, automatically called by TestCase before any other test method is invoked"""
        e = NullEngine()
        # Uncomment to see visualization for debugging etc.
        #e = Engine()
        e.start()
        e.new_scene()
        self.e=e

        # Read the multi-block plot3d file.
        r = PLOT3DReader()
        r.reader.set(has_byte_count=True, multi_grid=True,
                     byte_order='little_endian')
        r.initialize(get_example_data('tiny.xyz'),
                     get_example_data('tiny.q'),
                     configure=False)
        e.add_source(r)
        # Add the filter.
        f = SelectOutput()
        e.add_filter(f)

        # Create an outline for the data.
        o = Outline()
        e.add_module(o)
        o.render()
        self.o=o
        self.r=r
        self.e=e
        self.scene = e.current_scene
        return

    def tearDown(self):
        """For necessary clean up, automatically called by TestCase after the test methods have been invoked"""
        self.e.stop()
        return

    def test_plot3d_mb_reader(self):
        "Test if the test fixture works"
        s=self.scene
        o=self.o
        #Check the bounds of the outline.
        self.assertEqual(o.outline_filter.output.bounds,
                                    (1.0, 2.0, 1.0, 2.0, 1.0, 2.0))

        #from mayavi.tools.show import show
        #show()


    def test_save_and_restore(self):
        """Test if saving a visualization and restoring it works."""
        engine = self.e
        scene = self.scene

        # Save visualization.
        f = StringIO()
        f.name = abspath('test.mv2') # We simulate a file.
        engine.save_visualization(f)
        f.seek(0) # So we can read this saved data.

        # Remove existing scene.

        engine.close_scene(scene)

        # Load visualization
        engine.load_visualization(f)
        s=self.scene = engine.current_scene

        o = s.children[0].children[0].children[0].children[0]
        self.assertEqual(o.outline_filter.output.bounds,
                                (1.0, 2.0, 1.0, 2.0, 1.0, 2.0))


    @unittest.skip("Plot3DReader and MultiBlock version are broken in 5.10.1")
    def test_deepcopied(self):
        """Test if the MayaVi2 visualization can be deep-copied.
           XXX: The plot 3d reader and multi block version are broken in
                vtk 5.10.1. This will be fixed in next Mayavi release."""
        ############################################################
        # Copy the reader to see if it does not pop up the UI.

        # Pop the source object.
        r=self.r
        e=self.e
        r1 = copy.deepcopy(r)
        e.add_source(r1)

        o1 = r1.children[0].children[0].children[0]
        self.assertEqual(o1.outline_filter.output.bounds,
                                    (1.0, 2.0, 1.0, 2.0, 1.0, 2.0))
        r1.children[0].output_index = 0
        self.assertEqual(o1.outline_filter.output.bounds,
                                    (2.0, 3.0, 1.0, 2.0, 1.0, 2.0))

if __name__ == '__main__':
    unittest.main()
