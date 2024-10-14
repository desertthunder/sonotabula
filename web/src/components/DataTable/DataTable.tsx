import { decodeUnicode } from "@/libs/helpers";
import { Playlist } from "./types";
import { useNavigate } from "react-router-dom";
import { Table } from "@radix-ui/themes";

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
    <Table.Root variant="surface">
      <Table.Header>
        <Table.Row>
          {headers.map((header) => (
            <Table.ColumnHeaderCell key={header}>
              {header === "Cover" ? (
                <span className="sr-only">Cover</span>
              ) : (
                header
              )}
            </Table.ColumnHeaderCell>
          ))}
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {data.map((item) => (
          <Table.Row key={item.id}>
            <Table.RowHeaderCell>
              <img
                src={item.image_url}
                alt="Cover"
                width="100px"
                height="100px"
              />
            </Table.RowHeaderCell>
            <Table.Cell>{item.name}</Table.Cell>

            <Table.Cell>
              <em>
                {item.description ? decodeUnicode(item.description) : "None"}
              </em>
            </Table.Cell>
            <Table.Cell className="text-center">
              {item.is_synced ? (
                <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
              ) : (
                <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
              )}
            </Table.Cell>
            <Table.Cell className="text-center">
              {item.is_analyzed ? (
                <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
              ) : (
                <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
              )}
            </Table.Cell>
            <Table.Cell className="text-center">
              <button
                data-id={item.id}
                type="button"
                title="Open details"
                className="rounded-md p-0 text-gray-500 hover:text-green-300 focus:text-secondary"
                onClick={() => handleClick(item.id)}
              >
                <i className="text-3xl i-ri-more-fill"></i>
              </button>
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  );
}
