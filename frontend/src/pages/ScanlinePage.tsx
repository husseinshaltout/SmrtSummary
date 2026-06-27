import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ScanlineCanvas } from '../components/ScanlineCanvas';
import { useVideoStatus } from '../hooks/useVideoStatus';
import { api } from '../api/client';

export function ScanlinePage() {
  const { id } = useParams();
  const videoId = Number(id);
  const navigate = useNavigate();
  const video = useVideoStatus(videoId, true);
  const [canvasX, setCanvasX] = useState(360);
  const [frameX, setFrameX] = useState(0);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!video) {
    return <p>Loading video...</p>;
  }

  const isReady = video.status === 'ready';

  const handleGenerate = async () => {
    setSubmitting(true);
    setError('');
    try {
      await api.createSummary(videoId, frameX);
      navigate(`/videos/${videoId}/summary`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not generate summary');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-2">Select scanline</h1>
      {!isReady && (
        <p className="mb-4 text-secondary-200">
          Processing ({video.status}){video.processing_error ? `: ${video.processing_error}` : '...'}
        </p>
      )}
      {video.thumbnail_url && (
        <ScanlineCanvas
          imageUrl={video.thumbnail_url}
          frameWidth={video.frame_width}
          sliderValue={canvasX}
          onSliderChange={(nextCanvasX, nextFrameX) => {
            setCanvasX(nextCanvasX);
            setFrameX(nextFrameX);
          }}
        />
      )}
      {error && <p className="text-red-600 mt-4">{error}</p>}
      <div className="mt-6 flex gap-4">
        <button
          type="button"
          disabled={!isReady || submitting}
          onClick={handleGenerate}
          className="bg-primary text-white rounded px-4 py-2 font-semibold disabled:opacity-50"
        >
          Get Summary
        </button>
        {video.summary_url && (
          <Link to={`/videos/${videoId}/summary`} className="bg-secondary-200 text-white rounded px-4 py-2 font-semibold">
            View last summary
          </Link>
        )}
      </div>
    </div>
  );
}
