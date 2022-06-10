const drawImageScaled = () => {
  const canvas = document.getElementById('scanline_canvas');
  const ctx = canvas.getContext('2d');
  const img = document.getElementById('first_frame_image');
  const canvasCtx = ctx.canvas;
  const hRatio = canvasCtx.width / img.width;
  const vRatio = canvasCtx.height / img.height;
  const ratio = Math.min(hRatio, vRatio);
  const centerShiftOfX = (canvasCtx.width - img.width * ratio) / 2;
  const centerShiftOfY = (canvasCtx.height - img.height * ratio) / 2;
  // ctx.clearRect(0, 0, canvasCtx.width, canvasCtx.height);
  ctx.drawImage(
    img,
    0,
    0,
    img.width,
    img.height,
    centerShiftOfX,
    centerShiftOfY,
    img.width * ratio,
    img.height * ratio,
  );
};
const summaryDrawImage = () => {
  const canvas = document.getElementById('video_summary_canvas');
  const ctx = canvas.getContext('2d');
  const canvasContainer = document.getElementById('canvas__container');
  const imageObj = document.getElementById('video_summary_image');
  const { width } = imageObj;
  const { height } = imageObj;
  canvasContainer.style.width = `${width}px`;
  canvasContainer.style.height = `${height}px`;
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  // ctx.clearRect(0, 0, ctx.width, ctx.height);
  ctx.drawImage(imageObj, 0, 0, `${width}`, `${height}`);
};

window.onload = () => {
  try {
    drawImageScaled();
  } catch (error) {
    summaryDrawImage();
  }
};

const sec2time = (timeInSeconds) => {
  const pad = (num, size) => (`000${num}`).slice(size * -1);
  const time = parseFloat(timeInSeconds).toFixed(3);
  const hours = Math.floor(time / 60 / 60);
  const minutes = Math.floor(time / 60) % 60;
  const seconds = Math.floor(time - minutes * 60);
  const milliseconds = time.slice(-3);
  return (
    `${pad(hours, 2)
    }:${
      pad(minutes, 2)
    }:${
      pad(seconds, 2)
    }.${
      pad(milliseconds, 3)}`
  );
};
const timestampHandler = (mouseXPosition) => {
  // positin of slected frame divided by (video frames/seconds)
  const timestamp = mouseXPosition / 30;
  const timestampSpan = document.getElementById('timestamp');
  timestampSpan.textContent = sec2time(timestamp);
};
const drawRedLine = (drawInCanvas, canvas, xValue) => {
  const ctx = canvas.getContext('2d');
  ctx.strokeStyle = '#FF0000';
  ctx.lineWidth = 5;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawInCanvas();
  ctx.beginPath();
  ctx.moveTo(xValue, 0);
  ctx.lineTo(xValue, canvas.height);
  ctx.stroke();
  ctx.closePath();
};

function getMousePosition(canvas, event) {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  return x;
}

const scanlineSliderHandler = () => {
  const canvas = document.getElementById('scanline_canvas');
  const width = canvas.offsetWidth;
  document.getElementById('canvas_range').max = width;
  const sliderValue = document.getElementById('canvas_range').value;
  drawRedLine(drawImageScaled, canvas, sliderValue);
};

const videoSummaryCanvas = document.getElementById('video_summary_canvas');
videoSummaryCanvas.addEventListener('mousedown', (e) => {
  timestampHandler(getMousePosition(videoSummaryCanvas, e));
  drawRedLine(summaryDrawImage, videoSummaryCanvas, getMousePosition(videoSummaryCanvas, e));
});
