const resizeCanvasContainer = () => {
  const canvasContainer = document.getElementById('canvas__container');
  const img = document.getElementById('video_summary_image');
  const { width } = img;
  const { height } = img;
  canvasContainer.style.width = `${width}px`;
  canvasContainer.style.height = `${height}px`;
};

const drawImageScaled = () => {
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  const img = document.getElementById('video_summary_image');
  const canvasCtx = ctx.canvas;
  const hRatio = canvasCtx.width / img.width;
  const vRatio = canvasCtx.height / img.height;
  const ratio = Math.min(hRatio, vRatio);
  const centerShiftOfX = (canvasCtx.width - img.width * ratio) / 2;
  const centerShiftOfY = (canvasCtx.height - img.height * ratio) / 2;
  ctx.clearRect(0, 0, canvasCtx.width, canvasCtx.height);
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
const summaryDrawImage = () =>{
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  const canvasContainer = document.getElementById('canvas__container');
  const imageObj = document.getElementById('video_summary_image');
  const { width } = imageObj;
  const { height } = imageObj;
  canvasContainer.style.width = `${width}px`;
  canvasContainer.style.height = `${height}px`;
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  // ...then set the internal size to match
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  // ctx.canvas.width = `${width}`;
  // ctx.canvas.height = 480;
  ctx.clearRect(0, 0, ctx.width, ctx.height);
  ctx.drawImage(imageObj, 0, 0, `${width}`, `${height}`);
};

window.onload = () => {
  // resizeCanvasContainer();
  // drawImageScaled();
  summaryDrawImage();
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
const timestampHandler = () => {
  const sliderValue = document.getElementById('default-range').value;
  const timestamp = sliderValue / 30; // positin of slected frame divided by (video frames/seconds)
  const timestampSpan = document.getElementById('timestamp');
  timestampSpan.textContent = sec2time(timestamp);
};
const drawScanline = () => {
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  const width = canvas.offsetWidth;
  document.getElementById('default-range').max = width;
  const sliderValue = document.getElementById('default-range').value;
  ctx.strokeStyle = '#FF0000';
  ctx.lineWidth = 20;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // drawImageScaled();
  summaryDrawImage();
  ctx.beginPath();
  ctx.moveTo(sliderValue, 0);
  ctx.lineTo(sliderValue, 480);
  ctx.stroke();
};
const videoSummarySliderHandler = () => {
  // resizeCanvasContainer();
  drawScanline();
  timestampHandler();
};
