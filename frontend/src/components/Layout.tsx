import { Link, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function Layout() {
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow px-8 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-semibold text-primary">SmrtSummary</Link>
        <div className="flex items-center gap-4">
          <Link to="/upload" className="text-sm font-medium hover:text-primary">Upload</Link>
          <span className="text-sm text-secondary-200">{user?.username}</span>
          <button type="button" onClick={() => logout()} className="text-sm font-medium hover:text-primary">
            Logout
          </button>
        </div>
      </nav>
      <main className="px-8 py-6">
        <Outlet />
      </main>
    </div>
  );
}
