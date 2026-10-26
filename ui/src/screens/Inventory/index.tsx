import { useCallback, useMemo, useState } from "react";

import AddStockDialog from "./AddStockDialog";
import ComponentPanel from "./ComponentPanel";
import ComponentTable, { type StockFilter } from "./ComponentTable";
import RequestsList from "./RequestsList";
import { aircraftName, useAircraftModels, useComponents, useMe, useRequests, useRpas } from "./api";
import { ErrorText, controlClass, primaryButton } from "./ui";

const VIEW_KEY = "inventory-view";

function readView(): "list" | "grid" {
  try {
    return localStorage.getItem(VIEW_KEY) === "grid" ? "grid" : "list";
  } catch {
    return "list";
  }
}

function SummaryTile({ label, value, tone }: { label: string; value: number; tone: string }) {
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="text-sm text-gray-500">{label}</div>
      <div className={`mt-1 text-2xl font-semibold tabular-nums ${tone}`}>{value}</div>
    </div>
  );
}

export default function InventoryPage() {
  const components = useComponents();
  const requests = useRequests();
  const { data: me } = useMe();
  const { data: aircraftModels = [] } = useAircraftModels();
  const { data: rpasList = [] } = useRpas();

  const [tab, setTab] = useState<"components" | "requests">("components");
  const [search, setSearch] = useState("");
  // null until the user picks a filter; then we default based on whether the organization has stock
  const [chosenStockFilter, setStockFilter] = useState<StockFilter | null>(null);
  const [showSmallParts, setShowSmallParts] = useState(false);
  const [aircraftFilter, setAircraftFilter] = useState<number | null>(null);
  const [view, setView] = useState<"list" | "grid">(readView);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [addingStock, setAddingStock] = useState(false);

  const all = components.data ?? [];
  const requestList = requests.data ?? [];

  // A new organization has no stock yet, so start on the whole catalog instead of an empty list
  const stockFilter: StockFilter =
    chosenStockFilter ?? (all.some((c) => c.has_stock_history) ? "available" : "all");

  const summary = useMemo(
    () => ({
      inStock: all.filter((c) => c.available > 0).length,
      outOfStock: all.filter((c) => c.available === 0 && c.has_stock_history).length,
      unserviceable: all.reduce((total, c) => total + c.unserviceable_units, 0),
      pending: requestList.filter((r) => r.status === "pending").length,
    }),
    [all, requestList],
  );

  const changeView = (next: "list" | "grid") => {
    setView(next);
    try {
      localStorage.setItem(VIEW_KEY, next);
    } catch {}
  };

  const onTagClick = useCallback((tag: string) => {
    setSearch(tag);
  }, []);

  const tabClass = (active: boolean) =>
    `border-b-2 px-1 pb-3 text-sm font-medium ${active ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500 hover:text-gray-700"}`;

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Components</h1>
          <p className="text-sm text-gray-500">Spare parts, assemblies and tracked units for your organization.</p>
        </div>
        {me !== undefined && !me.read_only && (
          <button className={primaryButton} onClick={() => { setAddingStock(true); }}>
            Add stock
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <SummaryTile label="Components in stock" value={summary.inStock} tone="text-gray-900" />
        <SummaryTile label="Out of stock" value={summary.outOfStock} tone="text-red-600" />
        <SummaryTile label="Unserviceable units" value={summary.unserviceable} tone="text-amber-600" />
        <SummaryTile label="Pending requests" value={summary.pending} tone="text-blue-600" />
      </div>

      <div className="flex gap-6 border-b">
        <button className={tabClass(tab === "components")} onClick={() => { setTab("components"); }}>
          Inventory
        </button>
        <button className={tabClass(tab === "requests")} onClick={() => { setTab("requests"); }}>
          Requests{summary.pending > 0 && ` (${summary.pending})`}
        </button>
      </div>

      <ErrorText error={components.error ?? requests.error} />

      {tab === "components" && (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <input
              type="search"
              className={`${controlClass} w-full sm:w-72`}
              placeholder="Search name, part number or tag"
              value={search}
              onChange={(e) => { setSearch(e.target.value); }}
            />
            <select
              className={controlClass}
              value={stockFilter}
              onChange={(e) => { setStockFilter(e.target.value as StockFilter); }}
            >
              <option value="available">Available</option>
              <option value="out">Out of stock</option>
              <option value="all">Whole catalog</option>
            </select>
            <label
              className="inline-flex items-center gap-2 text-sm text-gray-600"
              title="Screws, nuts, seals and other bulk items. Search always finds them."
            >
              <input
                type="checkbox"
                className="rounded border-gray-300"
                checked={showSmallParts}
                onChange={(e) => { setShowSmallParts(e.target.checked); }}
              />
              Show small parts
            </label>
            <select
              className={controlClass}
              value={aircraftFilter ?? ""}
              onChange={(e) => { setAircraftFilter(e.target.value === "" ? null : Number(e.target.value)); }}
            >
              <option value="">All aircraft</option>
              {aircraftModels.map((model) => (
                <option key={model.id} value={model.id}>
                  {aircraftName(model)}
                </option>
              ))}
            </select>
            <div className="ml-auto inline-flex rounded-md border bg-white p-0.5 shadow-sm">
              {(["list", "grid"] as const).map((option) => (
                <button
                  key={option}
                  onClick={() => { changeView(option); }}
                  className={`rounded px-3 py-1.5 text-sm font-medium capitalize ${view === option ? "bg-gray-900 text-white" : "text-gray-600 hover:bg-gray-100"}`}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>

          {components.isLoading ? (
            <p className="text-sm text-gray-500">Loading components…</p>
          ) : (
            <ComponentTable
              components={all}
              aircraftModels={aircraftModels}
              search={search}
              stockFilter={stockFilter}
              showSmallParts={showSmallParts}
              aircraftFilter={aircraftFilter}
              view={view}
              onSelect={(c) => { setSelectedId(c.id); }}
              onTagClick={onTagClick}
            />
          )}
        </div>
      )}

      {tab === "requests" && <RequestsList requests={requestList} me={me} />}

      {selectedId !== null && (
        <ComponentPanel
          componentId={selectedId}
          me={me}
          rpasList={rpasList}
          aircraftModels={aircraftModels}
          onClose={() => { setSelectedId(null); }}
        />
      )}

      {addingStock && (
        <AddStockDialog
          components={all}
          aircraftModels={aircraftModels}
          rpasList={rpasList}
          onClose={() => { setAddingStock(false); }}
        />
      )}
    </div>
  );
}
