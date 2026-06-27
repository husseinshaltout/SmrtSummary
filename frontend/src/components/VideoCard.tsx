import { Link } from 'react-router-dom';
import { Video } from '../api/client';

export function VideoCard({ video }: { video: Video }) {
  return (
    <Link to={`/videos/${video.id}`} className="card block hover:shadow-lg transition">
      {video.thumbnail_url ? (
        <img src={video.thumbnail_url} alt={video.title} className="h-40 w-full object-cover" />
      ) : (
        <div className="h-40 bg-gray-200 flex items-center justify-center text-sm">{video.status}</div>
      )}
      <div className="p-4">
        <h3 className="font-semibold truncate">{video.title}</h3>
        <p className="text-sm text-secondary-200">{video.video_duration || 'Processing...'}</p>
      </div>
    </Link>
  );
}
