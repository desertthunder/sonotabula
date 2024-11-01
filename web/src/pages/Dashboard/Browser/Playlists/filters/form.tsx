import { useCallback, useState } from "react";
import { usePlaylistFilters } from "./store";
import _ from "lodash";

function Checkbox() {
  const [checked, setChecked] = useState(false);

  const onClick = useCallback(() => {
    setChecked((prev) => !prev);
  }, [setChecked]);

  return (
    <button
      className="rounded bg-white flex items-center justify-center group p-2"
      onClick={onClick}
    >
      {checked ? (
        <i className="i-ri-checkbox-fill text-emerald-500 group-hover:i-ri-blank-line p-2.5" />
      ) : (
        <i className="i-ri-checkbox-blank-line text-gray-500 group-hover:i-ri-checkbox-line p-2.5" />
      )}
    </button>
  );
}

function Range() {
  const [value, setValue] = useState(5);
  return (
    <div className="flex items-center gap-2">
      <input
        id="labels-range-input"
        type="range"
        value={value}
        min={10}
        step={5}
        max={100}
        onChange={(event) => setValue(parseInt(event.target.value, 10))}
        className="w-3/4 h-2 rounded appearance-none cursor-pointer"
      />
      {value > 95 ? (
        <span>{"> 100"}</span>
      ) : value < 15 ? (
        <span>{"< 10"}</span>
      ) : (
        <span>{value.toString()}</span>
      )}
    </div>
  );
}

export function FilterForm() {
  const pageSize = usePlaylistFilters((state) => state.pageSize);
  const updatePageSize = usePlaylistFilters((state) => state.updatePageSize);

  const handlePageSizeChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>) => {
      updatePageSize(parseInt(event.target.value, 10));
    },
    [updatePageSize]
  );

  return (
    <section className="p-4 bg-emerald-500 text-zinc-50 flex flex-col gap-2">
      <h2 className="text-lg">Form Filters</h2>
      <div className="flex gap-4">
        <div className="flex flex-col gap-2 text-sm items-center">
          <label htmlFor="pageSize">Per Page</label>
          <select
            name="pageSize"
            onChange={handlePageSizeChange}
            className={[
              "bg-gray-50 border border-gray-300 rounded",
              "text-gray-900",
              "focus:ring-green-500 focus:border-green-500 block w-full",
              "py-2",
            ].join(" ")}
            value={pageSize}
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={15}>15</option>
            <option value={20}>20</option>
            <option value={25}>25</option>
          </select>
        </div>
        <div className="flex flex-col gap-2 items-center">
          <label htmlFor="isPublic">Public</label>
          <Checkbox />
        </div>
        <div className="flex flex-col gap-2 items-center">
          <label htmlFor="isPrivate">Shared</label>
          <Checkbox />
        </div>
        <div className="flex flex-col gap-2 items-center">
          <label htmlFor="isCollaborative">Analyzed</label>
          <Checkbox />
        </div>
        <div className="flex flex-col gap-2 w-1/4">
          <label htmlFor="labels-range-input" className="flex flex-col gap-1">
            <span>Playlist Size</span>
            <span className="text-xs text-gray-200 italic">
              Number of tracks
            </span>
          </label>
          <Range />
        </div>
      </div>
    </section>
  );
}
