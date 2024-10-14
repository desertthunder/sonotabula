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
    <table className="table-auto w-full my-0 overflow-scroll h-full text-xs text-left text-gray-800 ">
      <thead className="sticky top-0">
        <tr className="bg-gray-700">
          {headers.map((header) => (
            <th key={header}>
              {header === "Cover" ? (
                <span className="sr-only">Cover</span>
              ) : (
                header
              )}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="border-b bg-gray-50 border-gray-300">
        {data.map((item) => (
          <tr key={item.id}>
            <td>
              <img
                src={item.image_url}
                alt="Cover"
                width="100px"
                height="100px"
              />
            </td>
            <td>{item.name}</td>

            <td>
              <em>
                {item.description ? decodeUnicode(item.description) : "None"}
              </em>
            </td>
            <td className="text-center">
              {item.is_synced ? (
                <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
              ) : (
                <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
              )}
            </td>
            <td className="text-center">
              {item.is_analyzed ? (
                <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
              ) : (
                <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
              )}
            </td>
            <td className="text-center">
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
  );
}
