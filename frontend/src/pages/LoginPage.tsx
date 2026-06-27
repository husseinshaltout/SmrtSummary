import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    try {
      await login(String(form.get('username')), String(form.get('password')));
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 card p-8">
      <h1 className="text-2xl font-semibold mb-6">Login</h1>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="username" required placeholder="Username" className="w-full border rounded px-3 py-2" />
        <input name="password" type="password" required placeholder="Password" className="w-full border rounded px-3 py-2" />
        <button type="submit" className="w-full bg-primary text-white rounded py-2 font-semibold">Login</button>
      </form>
      <p className="mt-4 text-sm">
        Need an account? <Link to="/register" className="text-primary">Register</Link>
      </p>
    </div>
  );
}
