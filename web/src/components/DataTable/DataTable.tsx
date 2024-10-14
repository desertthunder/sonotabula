import { decodeUnicode } from "@/libs/helpers";
import { Playlist } from "./types";
import { useNavigate } from "react-router-dom";

interface Props<T> {
  response: T[];
}

const headers = [
  "Cover",
  "Name",
  "Description",
  "Synced",
  "Analyzed",
  "Actions",
];

export function DataTable<T>({ response }: Props<T>) {
  const navigate = useNavigate();

  const handleClick = (id: string | number) => {
    navigate(`/dashboard/browser/playlists/${id}`);
  };

  const data = response as Playlist[];

  return (
    <div className="overflow-y-auto flex-1 max-h-[600px] rounded-lg">
      <table className="text-sm w-full">
        <thead className="rounded-md">
          <tr className="border-b bg-white">
            {headers.map((header) => (
              <th
                key={header}
                className={[
                  "h-10 px-2 text-left align-middle font-medium text-slate-800",
                ].join(" ")}
              >
                {header === "Cover" ? (
                  <span className="sr-only">Cover</span>
                ) : (
                  header
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="last:border-b-0">
          {data.map((item) => (
            <tr
              key={item.spotify_id}
              className={[
                "border-b transition-colors",
                "bg-white",
                "even:bg-slate-100",
              ].join(" ")}
            >
              <td className={["p-2 align-middle"].join(" ")}>
                <img
                  src={item.image_url}
                  alt="Cover"
                  width="100px"
                  height="100px"
                />
              </td>
              <td>{item.name}</td>

              <td className={["p-2 align-middle"].join(" ")}>
                <em>
                  {item.description ? decodeUnicode(item.description) : "None"}
                </em>
              </td>
              <td className={["p-2 align-middle", "text-center"].join(" ")}>
                {item.is_synced ? (
                  <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
                ) : (
                  <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
                )}
              </td>
              <td className={["p-2 align-middle", "text-center"].join(" ")}>
                {item.is_analyzed ? (
                  <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
                ) : (
                  <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
                )}
              </td>
              <td className={["p-2 align-middle", "text-center"].join(" ")}>
                <button
                  data-id={item.id}
                  type="button"
                  title="Open details"
                  className="rounded-md p-0 text-gray-500 hover:text-green-300 focus:text-secondary"
                  onClick={() => handleClick(item.id)}
                >
                  <i className="text-3xl i-ri-more-fill"></i>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
