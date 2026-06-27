import { useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api, Video } from '../api/client';

function formatTimestamp(seconds: number): string {
  const pad = (value: number, size: number) => String(value).padStart(size, '0');
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  const millis = Math.floor((seconds % 1) * 1000);
  return `${pad(hours, 2)}:${pad(minutes, 2)}:${pad(secs, 2)}.${pad(millis, 3)}`;
}

export function SummaryPage() {
  const { id } = useParams();
  const videoId = Number(id);
  const [video, setVideo] = useState<Video | null>(null);
  const [timestamp, setTimestamp] = useState('00:00:00.000');
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    api.getVideo(videoId).then(setVideo).catch(() => undefined);
  }, [videoId]);

  const draw = () => {
    const canvas = canvasRef.current;
    const image = imageRef.current;
    if (!canvas || !image || !image.complete) {
      return;
    }
    canvas.width = image.width;
    canvas.height = image.height;
    canvas.getContext('2d')?.drawImage(image, 0, 0);
  };

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Video summary</h1>
      {video?.summary_url ? (
        <>
          <canvas
            ref={canvasRef}
            className="max-w-full rounded-lg bg-gray-600"
            onMouseDown={(event) => {
              const rect = event.currentTarget.getBoundingClientRect();
              const x = event.clientX - rect.left;
              setTimestamp(formatTimestamp(x / 30));
            }}
          />
          <img ref={imageRef} src={video.summary_url} alt="Summary" className="hidden" onLoad={draw} />
          <p className="mt-4 text-lg">Timestamp: {timestamp}</p>
          {video.video_url && (
            <a href={video.video_url} target="_blank" rel="noopener noreferrer" className="inline-block mt-4 bg-primary text-white rounded px-4 py-2">
              Play video
            </a>
          )}
        </>
      ) : (
        <p>No summary yet.</p>
      )}
      <Link to={`/videos/${videoId}`} className="inline-block mt-6 text-primary">Back to scanline</Link>
    </div>
  );
}
