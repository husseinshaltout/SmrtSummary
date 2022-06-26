from tkinter import N
import cv2 as cv
import time
from PIL import Image
from io import BytesIO
import numpy as np
from django.conf import settings
import boto3

# split video into frames
# concatenate all cropped images horizontaly
# create image summary uploaded to video
class SmrtSummary:
    def __init__(self, videoLocation: str) -> None:
        self.videoLocation = videoLocation
        self.cap = cv.VideoCapture(self.videoLocation)
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        # List storing splitted cropped frames as bytes
        self.croppedFramesAsBytesList = []

    def split_to_frames(self) -> np.ndarray:
        """Splits video to frames and store them in an numpy array."""
        framesAsArray = []
        i = 0
        while self.cap.isOpened():
            # read() returns tuple first element is a success flag, second is image array
            ret, frame = self.cap.read()
            if not ret:
                break
            framesAsArray.append(frame)
            print(f"Splitting Frame #{str(i)}")
            i += 1
        self.cap.release()
        framesAsArray = np.array(framesAsArray)
        return framesAsArray

    def store_frames_npz(self, framesArry: np.ndarray) -> bytes:
        """Stores an array of images to npz.
        Parameters:
        ---------------
        framesArry       images array, (N, 32, 32, 3) to be stored
        """
        arrayData = BytesIO()
        np.savez_compressed(arrayData, framesArry)
        return arrayData.getvalue()

    def read_npz(self, file) -> np.ndarray:
        """Reads images from npz.
        Parameters:
        ---------------
        file   npz file/url to read

        Returns:
        ----------
        images      images array, (N, 32, 32, 3) to be stored

        """
        response = self.bucket.Object(file).get()["Body"].read()
        imagesDict = np.load(BytesIO(response))
        images = imagesDict[imagesDict.files[0]]
        return images

    def get_video_duration(self) -> tuple[str, int]:
        fps = self.cap.get(cv.CAP_PROP_FPS)
        frame_count = self.cap.get(cv.CAP_PROP_FRAME_COUNT)
        duration = time.strftime("%H:%M:%S", time.gmtime(int(frame_count) / int(fps)))
        return duration, int(frame_count)

    # TODO append to linked list instead of list
    def crop_at_scanline(self, scanlineX: int, framesAsBytesList: np.ndarray) -> list:
        """Crop all frames at x-axis scanlineX.
        Parameters:
        ---------------
        scanlineX   x-axis postion to do the cropping at
        framesAsBytesList   list of frames to be cropped

        Returns:
        ----------
        croppedFramesAsBytesList      cropped frames as an array of bytes
        """
        for image in framesAsBytesList:
            rows = image.shape[0]
            cropped = image[0:rows, scanlineX - 1 : scanlineX]
            croppedFrameToString = cv.imencode(".jpg", cropped)[1].tobytes()
            self.croppedFramesAsBytesList.append(croppedFrameToString)
        print("cropping done!")
        return self.croppedFramesAsBytesList

    def concatenate_cropped_frames(self) -> bytes:
        """Concatenate all cropped images horizontaly.
        Parameters:
        ---------------
        croppedFramesAsBytesList      cropped frames as an array of bytes

        Returns:
        ----------
        file_stream.getvalue()      concatinated cropped images as bytes
        """
        for i, image in enumerate(self.croppedFramesAsBytesList):
            if i == 0:
                numpy_horizontal = cv.imdecode(np.asarray(bytearray(image)), cv.IMREAD_COLOR)
            else:
                img = cv.imdecode(np.asarray(bytearray(image)), cv.IMREAD_COLOR)
                numpy_horizontal = np.hstack((numpy_horizontal, img))
        # Create summary image
        file_stream = BytesIO()
        im = Image.fromarray(numpy_horizontal)
        im.save(file_stream, format="jpeg")
        return file_stream.getvalue()

    def create_summary(self, scanlineX: int, npz) -> bytes:
        framesAsArray = self.read_npz(npz)
        self.crop_at_scanline(scanlineX, framesAsArray)
        return self.concatenate_cropped_frames()

    def create_thumbnail(self, framesArray, thumbnailFrame) -> bytes:
        thumbnailAsArray = framesArray[thumbnailFrame]
        thumbnailStream = BytesIO()
        im = Image.fromarray(thumbnailAsArray)
        im.save(thumbnailStream, format="jpeg")
        return thumbnailStream.getvalue()
