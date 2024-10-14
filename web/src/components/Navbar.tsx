import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav className="flex border-b-4 border-green-500 px-4 pr-8 py-1 bg-white justify-between">
      <Link
        to="/"
        className="text-lg text-black flex items-center hover:text-green-500"
      >
        <i className="i-ri-spotify-line text-xl  mr-1" />
        <span>Dashspot</span>
      </Link>
      <input
        placeholder="Search..."
        className={[
          "min-w-[20%]",
          "flex h-9 rounded-lg",
          "border border-input bg-transparent px-3 py-1 text-sm shadow-sm",
          "transition-colors text-zinc-300",
          "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed",
          "disabled:opacity-50",
        ].join(" ")}
      />
    </nav>
  );
}
