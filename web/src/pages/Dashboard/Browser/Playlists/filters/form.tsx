import { useCallback, useEffect, useMemo, useState } from "react";
import { FilterKeys } from "@/store/filters";
import { useQueryParams } from "@/libs/hooks";
import { useLocation } from "wouter";

interface CheckboxProps {
  filter: FilterKeys;
}

function Checkbox({ filter }: CheckboxProps) {
  const [checked, setChecked] = useState(false);
  const [, setLocation] = useLocation();

  const onClick = useCallback(() => {
    setChecked((prev) => {
      return !prev;
    });
  }, [setChecked]);

  useEffect(() => {
    if (checked) {
      setLocation(`?${filter}=1`);
    } else {
      setLocation(`?${filter}=0`);
    }
  }, [checked, filter, setLocation]);

  return (
    <button
      className="rounded bg-white flex items-center justify-center group p-2"
      onClick={onClick}
    >
      {checked ? (
        <i className="i-ri-checkbox-fill text-primary group-hover:i-ri-blank-line p-2.5" />
      ) : (
        <i className="i-ri-checkbox-blank-line text-gray-500 group-hover:i-ri-checkbox-line p-2.5" />
      )}
    </button>
  );
}

export function Range() {
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
  const params = useQueryParams();
  const [, setLocation] = useLocation();
  const pageSize = useMemo(() => {
    return parseInt(params.get("pageSize") ?? "5", 10);
  }, [params]);

  const handlePageSizeChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>) => {
      const value = parseInt(event.target.value, 10);
      setLocation(`?pageSize=${value}`);
    },
    [setLocation]
  );

  return (
    <div className="flex flex-1 gap-4 justify-evenly">
      <section className="flex gap-2 text-sm items-center">
        <label className="flex-1">Per Page</label>
        <select
          name="pageSize"
          onChange={handlePageSizeChange}
          className={[
            "bg-gray-50 border border-gray-300 rounded",
            "text-gray-900",
            "focus:ring-green-500 focus:border-green-500 block max-w-full",
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
      </section>
      <div className="flex gap-2 items-center">
        <label>My Playlists</label>
        <Checkbox filter="my_playlists" />
      </div>
      <div className="flex gap-2 items-center">
        <label>Private</label>
        <Checkbox filter="private" />
      </div>
      <div className="flex gap-2 items-center">
        <label>Analyzed</label>
        <Checkbox filter="is_analyzed" />
      </div>
    </div>
  );
}
