#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 3/17/20, 9:10 PM
#  License: See LICENSE.txt
#
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/17/20, 10:53 PM
#  License: See LICENSE.txt
#

from beets.util.confit import Subview

from test.helper import TestHelper, Assertions, PLUGIN_NAME, capture_stdout
from beetsplug.goingrunning.command import GoingRunningCommand
from beetsplug.goingrunning import common as GoingRunningCommon
import unittest

class ConfigurationTest(TestHelper, Assertions):


    def test_user_config_main(self):
        """ Root level values check """
        self.reset_beets(config_file=b"config_user.yml")
        cfg: Subview = self.config[PLUGIN_NAME]

        # Check keys
        cfg_keys = cfg.keys()
        cfg_keys.sort()
        chk_keys = ['duration', 'targets', 'target', 'query', 'ordering', 'trainings']
        chk_keys.sort()
        self.assertEqual(chk_keys, cfg_keys)

        # Check values
        self.assertTrue(cfg["query"].exists())
        self.assertIsInstance(cfg["query"].get(), dict)
        self.assertEqual("0..999", cfg["query"]["bpm"].get())
        self.assertEqual("0..999", cfg["query"]["length"].get())

        self.assertTrue(cfg["ordering"].exists())
        self.assertIsInstance(cfg["ordering"].get(), dict)
        self.assertEqual(100, cfg["ordering"]["year+"].get())
        self.assertEqual(100, cfg["ordering"]["bpm+"].get())

        self.assertEqual(120, cfg["duration"].get())
        self.assertEqual("drive_1", cfg["target"].get())

    def test_user_config_targets(self):
        """ Check Targets"""
        self.reset_beets(config_file=b"config_user.yml")
        cfg: Subview = self.config[PLUGIN_NAME]
        targets = cfg["targets"]

        self.assertIsInstance(targets, Subview)
        self.assertEquals(["drive_1", "drive_2", "drive_3", "drive_not_connected"], list(targets.get().keys()))

        # Check single target
        target = targets["drive_1"]
        self.assertIsInstance(target, Subview)
        self.assertTrue(target.exists())
        self.assertEqual("/tmp/beets-goingrunning-test-drive", target["device_root"].get())

        # Check single target
        target = targets["drive_2"]
        self.assertIsInstance(target, Subview)
        self.assertTrue(target.exists())
        self.assertEqual("/mnt/UsbDrive", target["device_root"].get())

        # Check single target
        target = targets["drive_3"]
        self.assertIsInstance(target, Subview)
        self.assertTrue(target.exists())
        self.assertEqual("~/Music/", target["device_root"].get())

        # Check single target
        target = targets["drive_not_connected"]
        self.assertIsInstance(target, Subview)
        self.assertTrue(target.exists())
        self.assertEqual("/media/this/probably/does/not/exist", target["device_root"].get())



    def test_user_config_trainings(self):
        """ Root level values check """
        self.reset_beets(config_file=b"config_user.yml")
        cfg: Subview = self.config[PLUGIN_NAME]

        # Check values at Trainings level
        trainings = cfg["trainings"]
        self.assertTrue(trainings.exists())
        self.assertIsInstance(trainings["query"].get(), dict)
        self.assertEqual("50..200", trainings["query"]["bpm"].get())
        self.assertEqual("30..600", trainings["query"]["length"].get())
        self.assertIsInstance(trainings["ordering"].get(), dict)
        self.assertEqual(100, trainings["ordering"]["year+"].get())
        self.assertEqual(100, trainings["ordering"]["bpm+"].get())
        self.assertEqual(60, trainings["duration"].get())
        self.assertEqual("drive_2", trainings["target"].get())

        # Check Training-1
        t1 = trainings["training-1"]
        self.assertTrue(t1.exists())
        self.assertIsInstance(t1["query"].get(), dict)
        self.assertEqual("150..180", t1["query"]["bpm"].get())
        self.assertEqual("120..240", t1["query"]["length"].get())
        self.assertIsInstance(t1["ordering"].get(), dict)
        self.assertEqual(75, t1["ordering"]["year+"].get())
        self.assertEqual(50, t1["ordering"]["bpm+"].get())
        self.assertEqual(55, t1["duration"].get())
        self.assertEqual("drive_3", t1["target"].get())
        self.assertEqual("Born to run", t1["alias"].get())

        # Check Training-2
        t2 = trainings["training-2"]
        self.assertTrue(t2.exists())
        self.assertIsInstance(t2["query"].get(), dict)
        self.assertEqual("170..180", t2["query"]["bpm"].get())
        self.assertEqual("90..180", t2["query"]["length"].get())
        self.assertIsInstance(t2["ordering"].get(), dict)
        self.assertEqual(50, t2["ordering"]["year+"].get())
        self.assertEqual(25, t2["ordering"]["bpm+"].get())
        self.assertEqual(25, t2["duration"].get())
        self.assertEqual("drive_3", t2["target"].get())
        self.assertEqual("Born to run", t2["alias"].get())

    def test_method_list_training_attributes(self):
        """ Generic check to see if plugin related configuration is present
        coming from user configuration file """
        self.reset_beets(config_file=b"config_user.yml")
        plg = GoingRunningCommand(self.config[PLUGIN_NAME])

        name = "training-1"
        with capture_stdout() as out:
            plg.list_training_attributes(name)
        self.assertIn(name, out.getvalue())
        self.assertIn("alias: Born to run", out.getvalue())
        self.assertIn("duration: 55", out.getvalue())
        # self.assertIn("song_bpm: [150, 180]", out.getvalue())
        # self.assertIn("song_len: [120, 240]", out.getvalue())
        self.assertIn("target: drive_3", out.getvalue())

        name = "training-2"
        with capture_stdout() as out:
            plg.list_training_attributes(name)
        self.assertIn(name, out.getvalue())
        self.assertIn("alias: Born to run", out.getvalue())
        self.assertIn("duration: 25", out.getvalue())
        # self.assertIn("song_bpm: [170, 180]", out.getvalue())
        # self.assertIn("song_len: [90, 180]", out.getvalue())
        self.assertIn("target: drive_3", out.getvalue())
