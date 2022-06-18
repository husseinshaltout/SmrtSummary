import cv2 as cv
import os
import time
import glob
import numpy as np


# create directory with user id
# split video into frames in user directory
# concatenate all cropped images horizontaly
# create image summary uploaded to video
class SmrtSummary:
    def __init__(self, videoLocation: str, framesLocation: str) -> None:
        self.videoLocation = videoLocation
        self.framesLocation = framesLocation
        self.cap = cv.VideoCapture(self.videoLocation)
        self.croppedFramesLocation = "%s/cropped" % self.framesLocation
        self.framesFileList = glob.glob("%s\\*.jpg" % self.framesLocation)

    def split_to_frames(self) -> None:
        i = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            cv.imwrite(os.path.join(self.framesLocation, "frame" + str(i) + ".jpg"), frame)
            print("Splitting Frame #%s" % str(i))
            i += 1
        self.cap.release()
        # cv.destroyAllWindows()

    def get_video_duration(self) -> None:
        fps = self.cap.get(cv.CAP_PROP_FPS)
        frame_count = self.cap.get(cv.CAP_PROP_FRAME_COUNT)
        duration = time.strftime("%H:%M:%S", time.gmtime(frame_count / fps))
        return duration, frame_count

    # Crop all frames at x-axis scanlineX
    def crop_at_scanline(self, scanlineX: int) -> None:
        for image in self.framesFileList:
            im = cv.imread(image, cv.IMREAD_COLOR)
            rows = im.shape[0]
            cropped = im[0:rows, scanlineX - 1 : scanlineX]
            cv.imwrite(os.path.join(self.croppedFramesLocation, image.split("\\")[-1]), cropped)
        print("cropping done!")

    def concatenate_cropped_frames(self) -> None:
        # Concatenate all cropped images horizontaly
        for i in range(len(self.framesFileList)):
            if i == 0:
                numpy_horizontal = cv.imread(os.path.join(self.croppedFramesLocation, "frame{0}.jpg").format(i))
            else:
                img = cv.imread(os.path.join(self.croppedFramesLocation, "frame{0}.jpg").format(i))
                numpy_horizontal = np.hstack((numpy_horizontal, img))
        print("Concatenating done!")
        print(f"numpy_horizontal value {numpy_horizontal}")
        # Create summary image
        cv.imwrite(os.path.join(self.croppedFramesLocation, "summary.png"), numpy_horizontal)

    def create_summary(self, scanlineX: int) -> None:
        self.crop_at_scanline(scanlineX)
        self.concatenate_cropped_frames()
