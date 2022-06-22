import cv2 as cv
import time
from PIL import Image
from io import BytesIO
import numpy as np
from django.conf import settings
import boto3

# create directory with user id
# split video into frames in user directory
# concatenate all cropped images horizontaly
# create image summary uploaded to video
class SmrtSummary:
    def __init__(self, videoLocation: str, framesLocation: str) -> None:
        self.videoLocation = videoLocation
        self.framesLocation = framesLocation
        self.cap = cv.VideoCapture(self.videoLocation)
        self.croppedFramesLocation = f"{self.framesLocation}/cropped"
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        self.framesFileList = self.bucket.objects.filter(Prefix=self.framesLocation)

    def split_to_frames(self) -> None:
        i = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frameToString = cv.imencode(".jpg", frame)[1].tobytes()
            self.bucket.put_object(Key=f"{self.framesLocation}/frame{str(i)}.jpg", Body=frameToString)
            print("Splitting Frame #%s" % str(i))
            i += 1
        self.cap.release()

    def get_video_duration(self) -> None:
        fps = self.cap.get(cv.CAP_PROP_FPS)
        frame_count = self.cap.get(cv.CAP_PROP_FRAME_COUNT)
        duration = time.strftime("%H:%M:%S", time.gmtime(frame_count / fps))
        return duration, frame_count

    # Crop all frames at x-axis scanlineX
    def crop_at_scanline(self, scanlineX: int) -> None:
        for image in self.framesFileList:
            imageAsBytes = image.get()["Body"].read()
            im = cv.imdecode(np.asarray(bytearray(imageAsBytes)), cv.IMREAD_COLOR)
            rows = im.shape[0]
            cropped = im[0:rows, scanlineX - 1 : scanlineX]
            croppedFrameToString = cv.imencode(".jpg", cropped)[1].tobytes()
            self.bucket.put_object(
                Key=f'{self.croppedFramesLocation}/{image.key.split("/")[-1]}', Body=croppedFrameToString
            )
        print("cropping done!")

    def concatenate_cropped_frames(self) -> None:
        # Concatenate all cropped images horizontaly
        for i, image in enumerate(self.bucket.objects.filter(Prefix=self.croppedFramesLocation)):
            if i == 0:
                imageAsBytes = image.get()["Body"].read()
                numpy_horizontal = cv.imdecode(np.asarray(bytearray(imageAsBytes)), cv.IMREAD_COLOR)
            else:
                imageAsBytes = image.get()["Body"].read()
                img = cv.imdecode(np.asarray(bytearray(imageAsBytes)), cv.IMREAD_COLOR)
                numpy_horizontal = np.hstack((numpy_horizontal, img))
        # Create summary image
        file_stream = BytesIO()
        im = Image.fromarray(numpy_horizontal)
        im.save(file_stream, format="jpeg")
        self.bucket.put_object(Key=f"{self.croppedFramesLocation}/summary.png", Body=file_stream.getvalue())

    def create_summary(self, scanlineX: int) -> None:
        self.crop_at_scanline(scanlineX)
        self.concatenate_cropped_frames()
