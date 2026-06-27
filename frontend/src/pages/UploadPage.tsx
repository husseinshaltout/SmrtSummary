import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

export function UploadPage() {
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const file = form.get('videofile');
    if (!(file instanceof File)) {
      setError('Choose a video file');
      return;
    }
    setUploading(true);
    setError('');
    try {
      const video = await api.uploadVideo(file, setProgress);
      navigate(`/videos/${video.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-xl">
      <h1 className="text-3xl font-semibold mb-6">Upload video</h1>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="card p-6 space-y-4">
        <input name="videofile" type="file" accept="video/mp4" required className="w-full" />
        {uploading && (
          <div>
            <div className="h-2 bg-gray-200 rounded">
              <div className="h-2 bg-primary rounded" style={{ width: `${progress}%` }} />
            </div>
            <p className="text-sm mt-2">{progress}% uploaded</p>
          </div>
        )}
        <button type="submit" disabled={uploading} className="bg-primary text-white rounded px-4 py-2 font-semibold disabled:opacity-50">
          Upload
        </button>
      </form>
    </div>
  );
}
