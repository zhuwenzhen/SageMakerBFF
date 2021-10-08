"""
video_utils.py
----------------
This file holds all the utilities to convert video to frame

@author Zhu, Wenzhen (zhu_wenzhen@icloud.com)
@date   09/15/2021
"""

import cv2
from utils import make_directory


def video_2_frame(file_key, img_data_folder):
    """
    :param file_key: string key on the s3 bucket
    :return:
    """
    cap = cv2.VideoCapture(file_key)
    prefix = file_key.split(".")[-2].split("/")[-1]
    print(prefix)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    fps = cap.get(cv2.CAP_PROP_FPS)

    second_cnt = 0
    frame_cnt = 0

    print("Video has %s frames" % video_length)
    print("Video fps = %s" % fps)

    file_dir = img_data_folder + "/"
    make_directory(file_dir)
    while cap.isOpened():
        ret, frame = cap.read()
        if frame_cnt == int(fps):
            second_cnt += 1
            frame_cnt = 0

        if ret:
            frame_name = prefix + "_{sec:04d}_{frame:03d}.png".format(
                sec=second_cnt, frame=frame_cnt
            )
            target_path = file_dir + frame_name
            frame_cnt += 1
            cv2.imwrite(target_path, frame)
        else:
            break

    cap.release()
