import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    try {
      await register({
        firstname: String(form.get('firstname')),
        lastname: String(form.get('lastname')),
        username: String(form.get('username')),
        email: String(form.get('email')),
        password: String(form.get('password')),
        password2: String(form.get('password2')),
      });
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 card p-8">
      <h1 className="text-2xl font-semibold mb-6">Register</h1>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="firstname" required placeholder="First name" className="w-full border rounded px-3 py-2" />
        <input name="lastname" required placeholder="Last name" className="w-full border rounded px-3 py-2" />
        <input name="username" required placeholder="Username" className="w-full border rounded px-3 py-2" />
        <input name="email" type="email" required placeholder="Email" className="w-full border rounded px-3 py-2" />
        <input name="password" type="password" required placeholder="Password" className="w-full border rounded px-3 py-2" />
        <input name="password2" type="password" required placeholder="Confirm password" className="w-full border rounded px-3 py-2" />
        <button type="submit" className="w-full bg-primary text-white rounded py-2 font-semibold">Register</button>
      </form>
      <p className="mt-4 text-sm">
        Already have an account? <Link to="/login" className="text-primary">Login</Link>
      </p>
    </div>
  );
}
