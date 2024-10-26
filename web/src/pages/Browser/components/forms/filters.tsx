import { useState } from "react";
import {
  NumericFilterType,
  BooleanFilterType,
  numericalFilters,
  booleanFilters,
  stringFilters,
  FilterSet,
  FilterMap,
  SearchMap,
} from "@libs/types";

export function FilterForm(props: {
  updateFilters: (filters: string[][]) => void;
}) {
  // key=value pairs
  // tracks > n ex. ?num_tracks_gt=10
  // tracks < n ex. ?num_tracks_lt=10
  // private ex. ?num_tracks_gt=10&private=1
  // is_analyzed ex. ?is_analyzed=1
  // my_playlists ex. ?my_playlists=1
  const [filterSet, updateFilterSet] = useState<FilterSet>(new Set());
  const [filterMap, setFilterMap] = useState<FilterMap>(new Map());
  const [searchMap, setSearchMap] = useState<SearchMap>(new Map());

  const handleCheckbox = (filter: BooleanFilterType) => {
    if (filterSet.has(filter)) {
      filterSet.delete(filter);
    } else {
      filterSet.add(filter);
    }
    updateFilterSet(new Set(filterSet));
  };

  const handleNumericalFilter = (filter: NumericFilterType, value: number) => {
    setFilterMap(new Map(filterMap.set(filter, value)));
  };

  return (
    <div className="flex flex-col gap-2 bg-slate-200 p-4 text-sm border-b border-b-slate-500">
      <div className="grid grid-cols-3 gap-2">
        <div className="flex flex-col col-span-1">
          <h3 className="text-lg font-bold">Search</h3>
          {stringFilters.map(([filter, label]) => (
            <div key={filter} className="flex flex-col">
              <label>Playlist {label.toLowerCase()}:</label>
              <div className="flex py-2">
                <input
                  placeholder={`Search by ${label.toLowerCase()}...`}
                  value={searchMap.get(filter)}
                  className="rounded-l-md p-2 flex-1"
                  onChange={(e) =>
                    setSearchMap(new Map(searchMap.set(filter, e.target.value)))
                  }
                />
                <button className="bg-slate-100 p-2 rounded-r-md">
                  Search
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-col col-span-2">
          <h3 className="text-lg font-bold">Filters</h3>
          <div className="flex gap-2 space-x-2">
            {numericalFilters.map(([filter, label]) => (
              <div key={filter} className="flex flex-col">
                <label>{label}: </label>
                {[10, 25, 50, 100].map((value) => (
                  <button
                    key={`${filter}-${value}`}
                    disabled={Array.from(filterMap.values()).includes(value)}
                    className={[
                      "p-2",
                      "rounded-md",
                      "m-2",
                      "max-w-[100px]",
                      filterMap.get(filter) === value
                        ? "bg-gray-300 pointer-events-none"
                        : "bg-green-400",
                      "hover:bg-green-300 hover:ring-1 hover:ring-green-400",
                    ].join(" ")}
                    onClick={() => handleNumericalFilter(filter, value)}
                  >
                    {value}
                  </button>
                ))}
              </div>
            ))}

            <div className="flex flex-col flex-shrink gap-8">
              {booleanFilters.map(([filter, label]) => (
                <div
                  key={filter}
                  className="flex justify-between gap-4 items-end"
                >
                  <label>{label}</label>

                  <button
                    className={[
                      "border border-primary ring-green-500 bg-white",
                      "rounded-md p-1 flex items-center",
                      filterSet.has(filter) ? "bg-green-400" : "bg-slate-100",
                    ].join(" ")}
                    onClick={() => handleCheckbox(filter)}
                  >
                    {filterSet.has(filter) ? (
                      <i className="i-ri-check-fill text-lg text-bold" />
                    ) : (
                      <i className="i-ri-close-fill text-lg text-bold" />
                    )}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          type="button"
          className={[
            "flex gap-2 items-center",
            "border border-slate-300",
            "rounded-md",
            "p-1",
            "bg-green-400",
            "hover:ring-1 hover:ring-green-500 hover:bg-green-300",
          ].join(" ")}
          onClick={(e) => {
            e.preventDefault();
            props.updateFilters([
              ...searchMap.entries(),
              ...filterMap.entries(),
              ...filterSet.entries().map(([key]) => [key, "1"]),
            ] as string[][]);
          }}
        >
          Search
        </button>
        <button
          type="reset"
          className={[
            "flex gap-2 items-center",
            "border border-slate-300",
            "rounded-md",
            "p-1",
            filterSet.size === 0 && filterMap.size === 0
              ? "cursor-not-allowed bg-gray-300 text-slate-500"
              : "cursor-pointer bg-red-400 hover:bg-red-500",
          ].join(" ")}
          disabled={filterSet.size === 0 && filterMap.size === 0}
          onClick={() => {
            setFilterMap(new Map());
            setSearchMap(new Map());
            updateFilterSet(new Set());
          }}
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
}
