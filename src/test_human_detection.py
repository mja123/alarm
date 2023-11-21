import unittest

from human_detection import HumanDetection


class HumanDetectionTest(unittest.TestCase):
    # def test_security_camera(self):
    #     human_detection = HumanDetection("./../resources/securityCamera.mp4", alarm_integration=False)
    #     detections, execution_time = human_detection.detection()
    #     self.assertGreater(detections, 5, "More than five detections")
    #     # self.assertLess(human_detection.duration - execution_time, 3)

    def test_security_record_thief(self):
        human_detection = HumanDetection(
            "./../resources/XVR_ch4_main_20230519021800_20230519022524 (online-video-cutter.com).mp4",
            alarm_integration=False)
        detections, execution_time = human_detection.detection()
        self.assertGreater(detections, 75, "More than seventy five detections")
        # self.assertLess(human_detection.duration - execution_time, 5)

    def test_security_record_day(self):
        human_detection = HumanDetection("./../resources/XVR_ch4_main_20230526184600_20230526184700.asf",
                                         alarm_integration=False)
        detections, execution_time = human_detection.detection()
        self.assertGreater(detections, 1, "More than five detections")
        # self.assertLess(human_detection.duration - execution_time, 3)

    # def test_video_without_people(self):
    #     human_detection = HumanDetection("./../resources/pexels-andrew-kota-3852660-3840x2160-30fps.mp4",
    #                                      alarm_integration=False)
    #     detections, execution_time = human_detection.detection()
    #     self.assertEquals(detections, 0, "No detections")
    #     # self.assertLess(human_detection.duration - execution_time, 3)


if __name__ == '__main__':
    unittest.main()
