import { Tabs } from "./Tabs";

type Playlist = {
  name: string;
  description: string;
  link: string;
  size: number;
};

const data: Array<Playlist> = [
  {
    name: "Playlist 1",
    description: "Description 1",
    link: "https://www.example.com",
    size: 10,
  },
  {
    name: "Playlist 2",
    description: "Description 2",
    link: "https://www.example.com",
    size: 20,
  },
  {
    name: "Playlist 3",
    description: "Description 3",
    link: "https://www.example.com",
    size: 30,
  },
];

export function LibraryCard() {
  return (
    <div className="card h-full">
      <header>
        <h1 className="">Library</h1>
        <h2 className="">I dunno</h2>
      </header>
      <Tabs />
      <main>
        <table className="table-auto h-full">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Size</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            {[...data, ...data, ...data].map((playlist) => (
              <tr key={playlist.name}>
                <td>{playlist.name}</td>
                <td>{playlist.description}</td>
                <td>{playlist.size}</td>
                <td>
                  <a
                    href={playlist.link}
                    className="text-blue-500 hover:underline"
                  >
                    Link
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
