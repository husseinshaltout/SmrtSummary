const API_BASE = '/api';

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? decodeURIComponent(match[2]) : null;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }
  const csrf = getCookie('csrftoken');
  if (csrf) {
    headers.set('X-CSRFToken', csrf);
  }
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: 'same-origin',
  });
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorBody.detail || 'Request failed');
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Video {
  id: number;
  title: string;
  status: string;
  video_duration: string;
  frame_count: number;
  frame_width: number;
  upload_date: string;
  thumbnail_url?: string | null;
  summary_url?: string | null;
  video_url?: string | null;
  processing_error?: string;
}

export const api = {
  me: () => request<User>('/auth/me'),
  login: (username: string, password: string) =>
    request<User>('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  register: (payload: Record<string, string>) =>
    request<User>('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request<{ detail: string }>('/auth/logout', { method: 'POST', body: '{}' }),
  listVideos: () => request<Video[]>('/videos'),
  getVideo: (id: number) => request<Video>(`/videos/${id}`),
  uploadVideo: (file: File, onProgress?: (percent: number) => void) =>
    new Promise<Video>((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append('videofile', file);
      xhr.open('POST', `${API_BASE}/videos`);
      xhr.withCredentials = true;
      const csrf = getCookie('csrftoken');
      if (csrf) {
        xhr.setRequestHeader('X-CSRFToken', csrf);
      }
      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable && onProgress) {
          onProgress(Math.round((event.loaded / event.total) * 100));
        }
      };
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText) as Video);
          return;
        }
        reject(new Error(xhr.responseText || 'Upload failed'));
      };
      xhr.onerror = () => reject(new Error('Upload failed'));
      xhr.send(formData);
    }),
  createSummary: (id: number, scanline: number) =>
    request<Video>(`/videos/${id}/summary`, {
      method: 'POST',
      body: JSON.stringify({ scanline }),
    }),
};
