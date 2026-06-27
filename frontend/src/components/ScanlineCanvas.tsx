import { useEffect, useRef } from 'react';

interface ScanlineCanvasProps {
  imageUrl: string;
  frameWidth: number;
  sliderValue: number;
  onSliderChange: (canvasX: number, frameX: number) => void;
}

function canvasXToFrameX(canvasX: number, canvas: HTMLCanvasElement, img: HTMLImageElement, frameWidth: number) {
  const hRatio = canvas.width / img.width;
  const vRatio = canvas.height / img.height;
  const ratio = Math.min(hRatio, vRatio);
  const centerShiftX = (canvas.width - img.width * ratio) / 2;
  const frameX = Math.round((canvasX - centerShiftX) / ratio);
  return Math.max(0, Math.min(frameX, frameWidth - 1));
}

export function ScanlineCanvas({ imageUrl, frameWidth, sliderValue, onSliderChange }: ScanlineCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  const draw = () => {
    const canvas = canvasRef.current;
    const img = imageRef.current;
    if (!canvas || !img || !img.complete) {
      return;
    }
    const context = canvas.getContext('2d');
    if (!context) {
      return;
    }
    const hRatio = canvas.width / img.width;
    const vRatio = canvas.height / img.height;
    const ratio = Math.min(hRatio, vRatio);
    const centerShiftX = (canvas.width - img.width * ratio) / 2;
    const centerShiftY = (canvas.height - img.height * ratio) / 2;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(img, 0, 0, img.width, img.height, centerShiftX, centerShiftY, img.width * ratio, img.height * ratio);
    context.strokeStyle = '#FF0000';
    context.lineWidth = 5;
    context.beginPath();
    context.moveTo(sliderValue, 0);
    context.lineTo(sliderValue, canvas.height);
    context.stroke();
  };

  useEffect(() => {
    draw();
  }, [imageUrl, sliderValue]);

  return (
    <div>
      <canvas ref={canvasRef} width={720} height={480} className="rounded-lg bg-gray-600 w-full max-w-3xl" />
      <img ref={imageRef} src={imageUrl} alt="Video thumbnail" className="hidden" onLoad={draw} />
      <input
        type="range"
        min={0}
        max={720}
        value={sliderValue}
        aria-label="Scanline position"
        className="w-full mt-4"
        onChange={(event) => {
          const canvas = canvasRef.current;
          const img = imageRef.current;
          if (!canvas || !img) {
            return;
          }
          const canvasX = Number(event.target.value);
          onSliderChange(canvasX, canvasXToFrameX(canvasX, canvas, img, frameWidth || img.width));
        }}
      />
    </div>
  );
}
