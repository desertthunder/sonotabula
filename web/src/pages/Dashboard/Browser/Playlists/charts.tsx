import { useEffect, useMemo, useRef } from "react";
import "chart.js/auto";
import { Chart } from "chart.js";

import type { BrowserPlaylistTrack, Superlatives } from "@/libs/types/api";
import _ from "lodash";
import {
  useReactTable,
  createColumnHelper,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";

const DOCS = [
  {
    name: "Danceability",
    description:
      "Describes how suitable a track is for dancing based on tempo, rhythm stability, beat strength, and overall regularity.",
  },
  {
    name: "Energy",
    description: "Represents a perceptual measure of intensity and activity.",
  },
  {
    name: "Speechiness",
    description: "The presence of spoken words in a track.",
  },
  {
    name: "Acousticness",
    description:
      "A confidence measure from 0.0 to 1.0 of whether the track is acoustic.",
  },
  {
    name: "Instrumentalness",
    description: "Predicts whether a track contains no vocals.",
  },
  {
    name: "Liveness",
    description: "Detects the presence of an audience in the recording.",
  },
  {
    name: "Valence",
    description:
      "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.",
  },
];
type FlattenedSuperlatives = {
  label: string;
  min: number;
  min_track_id: string;
  min_track_name: string;
  min_track_artists: string;
  max: number;
  max_track_id: string;
  max_track_name: string;
  max_track_artists: string;
};

const superlativeColumnHelper = createColumnHelper<FlattenedSuperlatives>();
const minColumns = [
  superlativeColumnHelper.accessor("label", {
    id: "label",
    header: "Feature",
  }),
  superlativeColumnHelper.accessor("min", {
    id: "min",
    header: "Min",
    cell: (props) => <span>{_.round(props.getValue(), 3)}</span>,
  }),
  superlativeColumnHelper.accessor("min_track_name", {
    id: "min_track_name",
    header: "Track Name",
  }),
  superlativeColumnHelper.accessor("min_track_artists", {
    id: "min_track_artists",
    header: "Track Artists",
  }),
];
const maxColumns = [
  superlativeColumnHelper.accessor("label", {
    id: "label",
    header: "Feature",
  }),
  superlativeColumnHelper.accessor("max", {
    id: "max",
    header: "Max",
    cell: (props) => <span>{_.round(props.getValue(), 3)}</span>,
  }),
  superlativeColumnHelper.accessor("max_track_name", {
    id: "max_track_name",
    header: "Track Name",
  }),
  superlativeColumnHelper.accessor("max_track_artists", {
    id: "max_track_artists",
    header: "Track Artists",
  }),
];

export function BarChart({
  cleaned,
  labels,
  lookups,
}: {
  data: Superlatives;
  lookups: Map<string, BrowserPlaylistTrack>;
  cleaned: Omit<Superlatives, "duration_ms" | "loudness" | "tempo">;
  labels: string[];
}) {
  const flattened = useMemo(() => {
    return _.map(cleaned, (value, label) => {
      const minTrack = lookups.get(value.min_track_id);
      const maxTrack = lookups.get(value.max_track_id);
      return {
        label,
        min: value.min,
        min_track_id: value.min_track_id,
        min_track_name: minTrack?.name || "N/A",
        min_track_artists:
          minTrack?.artists.map((artist) => artist.name).join(", ") || "N/A",
        max: value.max,
        max_track_id: value.max_track_id,
        max_track_name: maxTrack?.name || "N/A",
        max_track_artists:
          maxTrack?.artists.map((artist) => artist.name).join(", ") || "N/A",
      };
    });
  }, [cleaned, lookups]);

  const minTable = useReactTable({
    columns: minColumns,
    data: flattened,
    getCoreRowModel: getCoreRowModel(),
  });

  const maxTable = useReactTable({
    columns: maxColumns,
    data: flattened,
    getCoreRowModel: getCoreRowModel(),
  });

  const datasets = useMemo(
    () => [
      {
        label: "Max",
        data: _.values(_.mapValues(cleaned, "max")),
        stack: "Stack 0",
        backgroundColor: "#0ea5e9",
      },
      {
        label: "Min",
        data: _.values(_.mapValues(cleaned, "min")),
        stack: "Stack 1",
        backgroundColor: "#f43f5e",
      },
    ],
    [cleaned]
  );

  // use a ref to store the chart instance since it it mutable
  const chart = useRef<Chart | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    return () => {
      if (chart.current) {
        chart.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    const ctx = canvasRef.current;
    if (ctx) {
      const newChart = new Chart(ctx, {
        type: "bar",
        data: { labels, datasets },
        options: { responsive: true },
      });

      chart.current = newChart;
    }

    return () => {
      if (chart.current) {
        chart.current.destroy();
      }
    };
  }, [datasets, labels]);

  return (
    <section className="grid grid-cols-5">
      <div className="p-4 col-span-2 flex flex-col">
        <canvas ref={canvasRef} />
        <header className="py-4 border-b">
          <h3 className="text-lg">Feature Descriptions</h3>
          <p>
            For more information see the{" "}
            <a
              href="https://developer.spotify.com/documentation/web-api/reference/get-audio-features"
              target="_blank"
              rel="noreferrer"
              className="text-emerald-700 hover:underline transition-colors duration-200 ease-in-out hover:text-green-400"
            >
              Spotify API documentation
            </a>
            .
          </p>
        </header>
        <section className="py-4">
          {DOCS.map((attr) => (
            <div key={attr.name} className="border-b py-2">
              <h2 className="text-base">{attr.name}</h2>
              <p className="text-xs">{attr.description}</p>
            </div>
          ))}
        </section>
      </div>
      <div className="p-4 col-span-3 text-xs flex flex-col">
        {[minTable, maxTable].map((table, index) => (
          <>
            <header className="p-4 border-b">
              <h3 className="text-lg">{index === 0 ? "Min" : "Max"}</h3>
              <p className="text-sm">
                {index === 0
                  ? "The minimum value for each feature."
                  : "The maximum value for each feature."}
              </p>
            </header>
            <div className="p-4 w-full">
              <table
                key={`${index === 0 ? "min-table" : "max-table"}`}
                className="table-auto w-3/4"
              >
                <thead>
                  {table.getHeaderGroups().map((headerGroup) => (
                    <tr
                      key={
                        headerGroup.id +
                        headerGroup.headers.map((h) => h.colSpan).join("")
                      }
                    >
                      {headerGroup.headers.map((header) => (
                        <th key={header.id} className="text-left">
                          {header.isPlaceholder
                            ? null
                            : flexRender(
                                header.column.columnDef.header,
                                header.getContext()
                              )}
                        </th>
                      ))}
                    </tr>
                  ))}
                </thead>
                <tbody>
                  {table.getRowModel().rows.map((row) => (
                    <tr key={row.id}>
                      {row.getVisibleCells().map((cell) => (
                        <td key={cell.id}>
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        ))}
      </div>
    </section>
  );
}
