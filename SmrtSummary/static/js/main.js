const getScanlineContext = () => {
  const canvas = document.getElementById('scanline_canvas');
  const img = document.getElementById('first_frame_image');
  if (!canvas || !img) {
    return null;
  }
  const hRatio = canvas.width / img.width;
  const vRatio = canvas.height / img.height;
  const ratio = Math.min(hRatio, vRatio);
  const centerShiftX = (canvas.width - img.width * ratio) / 2;
  const frameWidth = parseInt(canvas.dataset.frameWidth || img.width, 10);
  return { canvas, img, ratio, centerShiftX, frameWidth };
};

const canvasXToFrameX = (canvasX) => {
  const ctx = getScanlineContext();
  if (!ctx) {
    return 0;
  }
  const frameX = Math.round((canvasX - ctx.centerShiftX) / ctx.ratio);
  return Math.max(0, Math.min(frameX, ctx.frameWidth - 1));
};

const drawImageScaled = () => {
  const ctxData = getScanlineContext();
  if (!ctxData) {
    return;
  }
  const { canvas, img, ratio, centerShiftX, centerShiftY } = {
    ...ctxData,
    centerShiftY: (canvas.height - img.height * ratio) / 2,
  };
  const context = canvas.getContext('2d');
  context.drawImage(
    img,
    0,
    0,
    img.width,
    img.height,
    centerShiftX,
    centerShiftY,
    img.width * ratio,
    img.height * ratio,
  );
};

const summaryDrawImage = () => {
  const canvas = document.getElementById('video_summary_canvas');
  const canvasContainer = document.getElementById('canvas__container');
  const imageObj = document.getElementById('video_summary_image');
  if (!canvas || !canvasContainer || !imageObj) {
    return;
  }
  const { width } = imageObj;
  const { height } = imageObj;
  canvasContainer.style.width = `${width}px`;
  canvasContainer.style.height = `${height}px`;
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  canvas.getContext('2d').drawImage(imageObj, 0, 0, width, height);
};

window.onload = () => {
  try {
    drawImageScaled();
  } catch (error) {
    summaryDrawImage();
  }
  const statusUrl = document.body.dataset.videoStatusUrl;
  if (statusUrl) {
    pollVideoStatus(statusUrl);
  }
};

const pollVideoStatus = (statusUrl) => {
  const interval = setInterval(async () => {
    const response = await fetch(statusUrl, { credentials: 'same-origin' });
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    const banner = document.getElementById('processing-banner');
    if (!banner) {
      return;
    }
    if (data.status === 'ready') {
      banner.textContent = 'Video is ready.';
      banner.className = 'text-green-700';
      clearInterval(interval);
      window.location.reload();
    } else if (data.status === 'failed') {
      banner.textContent = data.processing_error || 'Processing failed.';
      banner.className = 'text-red-700';
      clearInterval(interval);
    } else {
      banner.textContent = `Processing video (${data.status})...`;
    }
  }, 2000);
};

const sec2time = (timeInSeconds) => {
  const pad = (num, size) => (`000${num}`).slice(size * -1);
  const time = parseFloat(timeInSeconds).toFixed(3);
  const hours = Math.floor(time / 60 / 60);
  const minutes = Math.floor(time / 60) % 60;
  const seconds = Math.floor(time - minutes * 60);
  const milliseconds = time.slice(-3);
  return `${pad(hours, 2)}:${pad(minutes, 2)}:${pad(seconds, 2)}.${pad(milliseconds, 3)}`;
};

const timestampHandler = (mouseXPosition) => {
  const fps = parseFloat(document.body.dataset.videoFps || '30', 10);
  const timestamp = mouseXPosition / fps;
  const timestampSpan = document.getElementById('timestamp');
  if (timestampSpan) {
    timestampSpan.textContent = sec2time(timestamp);
  }
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
  return event.clientX - rect.left;
}

const scanlineSliderHandler = () => {
  const canvas = document.getElementById('scanline_canvas');
  const range = document.getElementById('canvas_range');
  const frameInput = document.getElementById('scanline_frame_x');
  if (!canvas || !range) {
    return;
  }
  range.max = canvas.offsetWidth;
  const sliderValue = range.value;
  if (frameInput) {
    frameInput.value = canvasXToFrameX(Number(sliderValue));
  }
  drawRedLine(drawImageScaled, canvas, sliderValue);
};

const videoSummaryCanvas = document.getElementById('video_summary_canvas');
if (videoSummaryCanvas) {
  videoSummaryCanvas.addEventListener('mousedown', (e) => {
    timestampHandler(getMousePosition(videoSummaryCanvas, e));
    drawRedLine(summaryDrawImage, videoSummaryCanvas, getMousePosition(videoSummaryCanvas, e));
  });
}
