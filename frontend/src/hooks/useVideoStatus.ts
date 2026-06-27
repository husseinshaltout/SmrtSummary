import { useEffect, useState } from 'react';
import { api, Video } from '../api/client';

export function useVideoStatus(videoId: number, enabled: boolean) {
  const [video, setVideo] = useState<Video | null>(null);

  useEffect(() => {
    if (!enabled) {
      return undefined;
    }
    const interval = window.setInterval(() => {
      api.getVideo(videoId).then(setVideo).catch(() => undefined);
    }, 2000);
    api.getVideo(videoId).then(setVideo).catch(() => undefined);
    return () => window.clearInterval(interval);
  }, [videoId, enabled]);

  return video;
}
