import "./App.css";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      <aside className="w-full md:w-1/4 bg-green-800 text-white p-4">
        <h2 className="text-xl font-bold mb-4">Sidebar</h2>
        <ul>
          <li className="mb-2"><a href="#" className="hover:underline">Link 1</a></li>
          <li className="mb-2"><a href="#" className="hover:underline">Link 2</a></li>
          <li className="mb-2"><a href="#" className="hover:underline">Link 3</a></li>
        </ul>
      </aside>
      <main className="flex-1 bg-white p-4">
        <h1 className="text-2xl font-bold mb-4">Main Content</h1>
        <p>Welcome to the dashboard!</p>
      </main>
    </div>
  );
}
