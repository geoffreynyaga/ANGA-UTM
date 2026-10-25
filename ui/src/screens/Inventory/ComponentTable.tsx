import {
  type ColumnDef,
  type FilterFn,
  type SortingState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useMemo, useState } from "react";

import { type IAircraftModel, type IComponent, aircraftName } from "./api";
import { ComponentImage, StockBadge } from "./ui";

export type StockFilter = "available" | "out" | "all";

// Matches name, part number, diagram and tags, so "gen" finds generator parts
const searchComponent: FilterFn<IComponent> = (row, _columnId, value: string) => {
  const query = value.trim().toLowerCase();
  if (query === "") return true;
  const c = row.original;
  return [c.name, c.part_number ?? "", c.diagram_name, ...c.tags].some((text) =>
    text.toLowerCase().includes(query),
  );
};

export default function ComponentTable({
  components,
  aircraftModels,
  search,
  stockFilter,
  aircraftFilter,
  view,
  onSelect,
  onTagClick,
}: {
  components: IComponent[];
  aircraftModels: IAircraftModel[];
  search: string;
  stockFilter: StockFilter;
  aircraftFilter: number | null;
  view: "list" | "grid";
  onSelect: (component: IComponent) => void;
  onTagClick: (tag: string) => void;
}) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const aircraftById = useMemo(
    () => new Map(aircraftModels.map((model) => [model.id, aircraftName(model)])),
    [aircraftModels],
  );

  const rows = useMemo(
    () =>
      components.filter((c) => {
        if (aircraftFilter !== null && !c.aircraft_models.includes(aircraftFilter)) return false;
        if (stockFilter === "available") return c.available > 0;
        if (stockFilter === "out") return c.available === 0 && c.has_stock_history;
        return true;
      }),
    [components, stockFilter, aircraftFilter],
  );

  const tagList = (c: IComponent) => (
    <div className="flex flex-wrap gap-1">
      {c.tags.map((tag) => (
        <button
          key={tag}
          onClick={(event) => {
            event.stopPropagation();
            onTagClick(tag);
          }}
          className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-600 hover:bg-blue-100 hover:text-blue-700"
        >
          {tag}
        </button>
      ))}
    </div>
  );

  const columns = useMemo<Array<ColumnDef<IComponent>>>(
    () => [
      {
        id: "image",
        header: "",
        enableSorting: false,
        cell: ({ row }) => (
          <ComponentImage src={row.original.image} name={row.original.name} className="h-12 w-12 rounded" />
        ),
      },
      {
        accessorKey: "name",
        header: "Component",
        filterFn: searchComponent,
        cell: ({ row }) => (
          <div>
            <div className="font-medium text-gray-900">{row.original.name}</div>
            {row.original.status === "pending" && (
              <span className="text-xs text-amber-700">Pending review</span>
            )}
          </div>
        ),
      },
      { accessorKey: "part_number", header: "Part number", cell: ({ getValue }) => getValue<string>() ?? "—" },
      {
        id: "aircraft",
        header: "Aircraft",
        enableSorting: false,
        cell: ({ row }) =>
          row.original.aircraft_models.map((id) => aircraftById.get(id)).filter(Boolean).join(", ") || "—",
      },
      { id: "tags", header: "Tags", enableSorting: false, cell: ({ row }) => tagList(row.original) },
      {
        accessorKey: "unserviceable_units",
        header: "Unserviceable",
        cell: ({ getValue }) => getValue<number>() || "—",
      },
      {
        accessorKey: "available",
        header: "Stock",
        cell: ({ getValue }) => <StockBadge available={getValue<number>()} />,
      },
    ],
    // tagList only depends on onTagClick
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [aircraftById, onTagClick],
  );

  // A new filter array on every render makes the table reset its state and re-render forever
  const columnFilters = useMemo(() => [{ id: "name", value: search }], [search]);

  const table = useReactTable({
    data: rows,
    columns,
    state: { sorting, columnFilters },
    onSortingChange: setSorting,
    autoResetPageIndex: false,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  const visible = table.getRowModel().rows;

  if (visible.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-sm text-gray-500">
        No components match these filters.
      </div>
    );
  }

  if (view === "grid") {
    return (
      <div className="grid grid-cols-[repeat(auto-fill,minmax(12rem,1fr))] gap-4">
        {visible.map(({ original: c }) => (
          <div
            key={c.id}
            role="button"
            tabIndex={0}
            onClick={() => {
              onSelect(c);
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") onSelect(c);
            }}
            className={`flex cursor-pointer flex-col overflow-hidden rounded-lg border bg-white shadow-sm transition hover:shadow-md ${c.available === 0 ? "opacity-70" : ""}`}
          >
            <ComponentImage src={c.image} name={c.name} className="h-40 w-full border-b" />
            <div className="flex flex-1 flex-col gap-2 p-3">
              <div className="text-sm font-medium leading-snug text-gray-900">{c.name}</div>
              {c.part_number !== null && <div className="text-xs text-gray-500">{c.part_number}</div>}
              {tagList(c)}
              <div className="mt-auto pt-1">
                <StockBadge available={c.available} />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border bg-white shadow-sm">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map((group) => (
            <tr key={group.id}>
              {group.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  className={`px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500 ${header.column.getCanSort() ? "cursor-pointer select-none" : ""}`}
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {{ asc: " ↑", desc: " ↓" }[header.column.getIsSorted() as string] ?? ""}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="divide-y divide-gray-100">
          {visible.map((row) => (
            <tr
              key={row.id}
              onClick={() => {
                onSelect(row.original);
              }}
              className="cursor-pointer hover:bg-gray-50"
            >
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-2 align-middle text-gray-700">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
