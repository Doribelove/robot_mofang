import importlib.util
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import MagicMock, Mock, patch


SRC = Path(__file__).resolve().parents[1] / "src"


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SRC / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VisionCaptureTest(unittest.TestCase):
    def setUp(self):
        self.cv2 = Mock()
        self.hardware = Mock()
        self.cameras = [Mock() for _ in range(4)]
        self.cv2.VideoCapture.side_effect = self.cameras
        # Model imshow's rejection of an empty frame without opening a GUI.
        def show(window, frame):
            if frame is None or frame.size == 0:
                raise ValueError("imshow received an empty frame in " + window)
        self.cv2.imshow.side_effect = show
        deps = {name: Mock() for name in
                ("numpy", "kociemba", "twophase", "twophase.solver",
                 "moving", "KociembaTrans", "jixiecost")}
        deps.update(cv2=self.cv2, hardware=self.hardware)
        with patch.dict(sys.modules, deps):
            with patch.object(threading.Thread, "start"):
                self.vision = load_module("vision_")
            with patch.dict(sys.modules, vision_=self.vision):
                self.function = load_module("Function")

    def run_worker(self):
        self.vision.turn_false()
        self.vision.queue_t.start()
        self.vision.queue_t.join(2)
        self.assertFalse(self.vision.queue_t.is_alive())

    def test_drop_followed_by_complete_batch(self):
        batches = [[MagicMock(size=1) for _ in self.cameras] for _ in range(4)]
        for i, camera in enumerate(self.cameras):
            reads = [(True, batch[i]) for batch in batches]
            if i == 1:
                reads[0] = (False, None)
            if i == 0:
                # End the post-recognition preview without real devices.
                reads.extend([(False, None), (False, None)])
            camera.read.side_effect = reads

        # Two unrecognized complete batches followed by a solved cube.
        self.cv2.TERM_CRITERIA_EPS, self.cv2.TERM_CRITERIA_MAX_ITER = 1, 2
        labels = [[0] * 9 + [1] * 9, [2] * 9 + [3] * 9, [4] * 9, [5] * 9]
        unrecognized = [[0] * len(facelets) for facelets in labels]
        self.cv2.kmeans.side_effect = [(0, list(range(6)) + facelets, None)
                                       for facelets in unrecognized + unrecognized + labels]
        self.run_worker()
        self.assertEqual(self.vision.wait_for_cube(), "".join(face * 9 for face in "URFDLB"))
        displayed = [c[0][1] for c in self.cv2.imshow.call_args_list]
        self.assertEqual(displayed, [frame for batch in batches[1:] for frame in batch])
        self.assertEqual(self.cv2.imwrite.call_count, 8)

    def test_unopened_camera_stops_solve(self):
        self.cameras[1].isOpened.return_value = False
        self.run_worker()
        self.assert_solve_reports(self.vision.CAMERA_DEVICES[1])
        for camera in self.cameras[:2]:
            camera.release.assert_called_once_with()

    def test_incomplete_retry_stops_solve(self):
        for camera in self.cameras:
            camera.read.return_value = (True, Mock(size=1))
        self.cameras[-1].read.return_value = (False, None)
        self.vision.cube_recognize = Mock()
        self.run_worker()
        self.assert_solve_reports(self.vision.CAMERA_DEVICES[-1])
        self.vision.cube_recognize.assert_not_called()
        self.cv2.imshow.assert_not_called()
        for camera in self.cameras:
            camera.release.assert_called_once_with()

    def assert_solve_reports(self, device):
        errors = []
        def solve():
            try:
                self.function.SolvingCube()
            except Exception as exc:
                errors.append(exc)
        waiter = threading.Thread(target=solve, daemon=True)
        waiter.start()
        waiter.join(1)
        self.assertFalse(waiter.is_alive(), "Solve kept waiting after the vision worker exited")
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RuntimeError)
        self.assertIn(device, str(errors[0]))
        self.assertEqual(self.hardware.mock_calls, [])


if __name__ == "__main__":
    unittest.main()
