import React, { useMemo } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  RadialBarChart,
  RadialBar,
  Legend,
  ResponsiveContainer,
} from "recharts";

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

function createColumns(cat: "min" | "max") {
  return [
    superlativeColumnHelper.accessor("label", {
      id: "label",
      header: "Feature",
      cell: (props) => <span>{_.startCase(props.getValue())}</span>,
    }),
    superlativeColumnHelper.accessor(cat, {
      id: cat,
      header: _.startCase(cat),
      cell: (props) => <span>{_.round(props.getValue(), 3)}</span>,
    }),
    superlativeColumnHelper.accessor(`${cat}_track_name`, {
      id: `${cat}_track_name`,
      header: "Track Name",
    }),
    superlativeColumnHelper.accessor(`${cat}_track_artists`, {
      id: `${cat}_track_artists`,
      header: "Track Artists",
    }),
  ];
}

const minColumns = createColumns("min");
const maxColumns = createColumns("max");

function TooltipContent({ active, payload, label }: any) {
  if (active && payload && payload.length) {
    const dataPair = payload[0].payload;

    const title = _.startCase(label);
    const minValue = _.round(dataPair.min, 3);
    const maxValue = _.round(dataPair.max, 3);
    const minTrack = dataPair.min_track_name;
    const maxTrack = dataPair.max_track_name;
    const minArtists = dataPair.min_track_artists;
    const maxArtists = dataPair.max_track_artists;

    return (
      <section className="text-xs">
        <p className="font-semibold">{`${title}`}</p>
        <p className="font-light">{`${title} Range`}</p>
        <p className="font-medium">{`Min: ${minValue} - ${minTrack} by ${minArtists}`}</p>
        <p className="font-medium">{`Max: ${maxValue} - ${maxTrack} by ${maxArtists}`}</p>
      </section>
    );
  }

  return null;
}

function RadialBarTooltipContent({ active, payload }: any) {
  if (active && payload && payload.length) {
    const pt = payload[0].payload;

    const subtitle = _.startCase(pt.name);
    const value = _.round(pt.value, 3);
    const title = `Average ${subtitle}`;

    return (
      <section className="text-xs bg-white p-2 rounded-md border border-gray-200">
        <p className="font-semibold">{title}</p>
        <p className="font-medium">Value: {`${value}`}</p>
      </section>
    );
  }

  return null;
}

function CustomTick({ x, y, payload }: any) {
  return (
    <g transform={`translate(${x},${y})`}>
      <text x={0} y={0} dy={16} textAnchor="end" fill="#666" fontSize={10}>
        {_.startCase(payload.value).slice(0, 5)}.
      </text>
    </g>
  );
}

export function SuperlativeBarChart({
  cleaned,
  lookups,
}: {
  data: Superlatives;
  lookups: Map<string, BrowserPlaylistTrack>;
  cleaned: Omit<Superlatives, "duration_ms" | "loudness" | "tempo">;
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

  return (
    <section className="grid grid-cols-5">
      <div className="p-4 col-span-2 flex flex-col">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={flattened}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="label"
              angle={30}
              height={60}
              padding="gap"
              tick={<CustomTick />}
            />
            <YAxis />
            <Tooltip content={<TooltipContent />} />

            <Bar dataKey="min" fill="#f87171" />
            <Bar dataKey="max" fill="#0ea5e9" />
          </BarChart>
        </ResponsiveContainer>
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
          <React.Fragment key={index}>
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
          </React.Fragment>
        ))}
      </div>
    </section>
  );
}

export function AverageRadialBarChart(props: {
  data: {
    name: string;
    value: number;
    fill: string;
  }[];
}) {
  return (
    <ResponsiveContainer width="50%" height={500}>
      <RadialBarChart
        innerRadius="10%"
        outerRadius="80%"
        barSize={20}
        data={props.data}
        endAngle={0}
        startAngle={180}
      >
        <RadialBar background dataKey="value" />
        <Legend
          iconSize={5}
          width={150}
          fontSize={10}
          layout="vertical"
          verticalAlign="top"
          align="right"
        />
        <Tooltip content={<RadialBarTooltipContent />} />
      </RadialBarChart>
    </ResponsiveContainer>
  );
}
