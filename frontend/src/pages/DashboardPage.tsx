import { useEffect, useState } from 'react';
import { api, Video } from '../api/client';
import { VideoCard } from '../components/VideoCard';

export function DashboardPage() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    api.listVideos().then(setVideos).catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-6">Your videos</h1>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {videos.map((video) => (
          <VideoCard key={video.id} video={video} />
        ))}
      </div>
    </div>
  );
}
