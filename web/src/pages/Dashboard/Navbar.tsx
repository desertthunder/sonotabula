import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav className="fixed z-30 w-full bg-gray-100 border-b-4 border-green-500">
      <div className="py-1 px-8 font-sans font-bold flex justify-between items-center">
        <Link
          to="/"
          className="text-lg text-black flex-1 flex items-center hover:text-green-500"
        >
          <i className="i-ri-spotify-line text-xl  mr-1" />
          <span>Dashspot</span>
        </Link>
        <input
          type="text"
          placeholder="Search"
          className="border border-gray-300 p-2 px-3 rounded-lg w-1/4 ring-primary ring-1"
        />
      </div>
    </nav>
  );
}
