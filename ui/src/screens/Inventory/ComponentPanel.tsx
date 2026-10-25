import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import {
  API,
  type IAircraftModel,
  type IComponentDetail,
  type IMe,
  type IRpas,
  type IStockLot,
  type IUnit,
  aircraftName,
  postJson,
  useComponentDetail,
} from "./api";
import { ComponentImage, ErrorText, Field, Modal, StockBadge, inputClass, primaryButton, secondaryButton } from "./ui";

type RequestTarget = { lot: IStockLot } | { unit: IUnit };

function RequestForm({
  component,
  target,
  rpasList,
  onDone,
}: {
  component: IComponentDetail;
  target: RequestTarget;
  rpasList: IRpas[];
  onDone: () => void;
}) {
  const queryClient = useQueryClient();
  const [showAll, setShowAll] = useState(component.aircraft_models.length === 0);
  const [rpas, setRpas] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [note, setNote] = useState("");

  const fits = (r: IRpas) => r.aircraft_model === null || component.aircraft_models.includes(r.aircraft_model);
  const options = showAll ? rpasList : rpasList.filter(fits);
  const selected = rpasList.find((r) => r.id === Number(rpas));

  const mutation = useMutation({
    mutationFn: async () =>
      await postJson(`${API}/requests/`, {
        rpas: Number(rpas),
        note,
        ...("lot" in target ? { lot: target.lot.id, quantity } : { unit: target.unit.id }),
      }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["inventory"] });
      onDone();
    },
  });

  return (
    <form
      className="space-y-3 rounded-md border border-blue-200 bg-blue-50 p-4"
      onSubmit={(event) => {
        event.preventDefault();
        mutation.mutate();
      }}
    >
      <div className="text-sm font-medium text-gray-900">
        Request {"unit" in target ? `unit #${target.unit.serial_number}` : `from ${target.lot.condition} stock`}
      </div>
      <Field label="Drone">
        <select required className={inputClass} value={rpas} onChange={(e) => { setRpas(e.target.value); }}>
          <option value="">Select a drone</option>
          {options.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name} ({r.rpas_serial})
            </option>
          ))}
        </select>
      </Field>
      {component.aircraft_models.length > 0 && (
        <label className="flex items-center gap-2 text-sm text-gray-600">
          <input type="checkbox" checked={showAll} onChange={(e) => { setShowAll(e.target.checked); }} />
          Show drones this part is not listed for
        </label>
      )}
      {selected !== undefined && !fits(selected) && (
        <p className="rounded-md bg-amber-50 px-3 py-2 text-sm text-amber-800">
          This part is not listed for this drone's aircraft model.
        </p>
      )}
      {"lot" in target && (
        <Field label={`Quantity (${target.lot.quantity} in stock)`}>
          <input
            type="number"
            min={1}
            max={target.lot.quantity}
            className={inputClass}
            value={quantity}
            onChange={(e) => { setQuantity(Number(e.target.value)); }}
          />
        </Field>
      )}
      <Field label="Note">
        <input className={inputClass} value={note} onChange={(e) => { setNote(e.target.value); }} placeholder="Optional" />
      </Field>
      <ErrorText error={mutation.error} />
      <div className="flex gap-2">
        <button type="submit" className={primaryButton} disabled={mutation.isPending}>
          Send request
        </button>
        <button type="button" className={secondaryButton} onClick={onDone}>
          Cancel
        </button>
      </div>
    </form>
  );
}

function TagEditor({ component }: { component: IComponentDetail }) {
  const queryClient = useQueryClient();
  const [value, setValue] = useState(component.tags.join(", "));
  const mutation = useMutation({
    mutationFn: async () =>
      await postJson(
        `${API}/components/${component.id}/`,
        { tags: value.split(",").map((t) => t.trim()).filter(Boolean) },
        "PATCH",
      ),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["inventory", "components"] });
    },
  });

  return (
    <form
      className="flex gap-2"
      onSubmit={(event) => {
        event.preventDefault();
        mutation.mutate();
      }}
    >
      <input
        className={inputClass}
        value={value}
        onChange={(e) => { setValue(e.target.value); }}
        placeholder="Comma separated, e.g. generator, fuel"
      />
      <button type="submit" className={secondaryButton} disabled={mutation.isPending}>
        Save tags
      </button>
    </form>
  );
}

const lifecycleStyle: Record<IUnit["lifecycle"], string> = {
  available: "bg-green-100 text-green-800",
  reserved: "bg-amber-100 text-amber-800",
  issued: "bg-blue-100 text-blue-800",
  installed: "bg-gray-100 text-gray-700",
  scrapped: "bg-red-100 text-red-700",
};

export default function ComponentPanel({
  componentId,
  me,
  rpasList,
  aircraftModels,
  onClose,
}: {
  componentId: number;
  me: IMe | undefined;
  rpasList: IRpas[];
  aircraftModels: IAircraftModel[];
  onClose: () => void;
}) {
  const queryClient = useQueryClient();
  const { data: component, error } = useComponentDetail(componentId);
  const [target, setTarget] = useState<RequestTarget | null>(null);
  const canWrite = me !== undefined && !me.read_only;

  const scrap = useMutation({
    mutationFn: async (unit: IUnit) =>
      await postJson(`${API}/units/${unit.id}/`, { lifecycle: "scrapped", serviceable: false }, "PATCH"),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["inventory"] });
    },
  });

  return (
    <Modal title={component?.name ?? "Component"} onClose={onClose} wide>
      <ErrorText error={error} />
      {component !== undefined && (
        <div className="space-y-6">
          <div className="flex flex-col gap-4 sm:flex-row">
            <ComponentImage src={component.image} name={component.name} className="h-40 w-40 shrink-0 rounded border" />
            <dl className="grid flex-1 grid-cols-[auto,1fr] gap-x-4 gap-y-1 text-sm">
              <dt className="text-gray-500">Part number</dt>
              <dd>{component.part_number ?? "—"}</dd>
              <dt className="text-gray-500">Diagram</dt>
              <dd>
                {component.diagram_name !== "" ? `${component.diagram_name} #${component.diagram_number}` : "—"}
              </dd>
              <dt className="text-gray-500">Aircraft</dt>
              <dd>
                {aircraftModels
                  .filter((m) => component.aircraft_models.includes(m.id))
                  .map(aircraftName)
                  .join(", ") || "—"}
              </dd>
              {component.parent_name != null && (
                <>
                  <dt className="text-gray-500">Part of</dt>
                  <dd>{component.parent_name}</dd>
                </>
              )}
              <dt className="text-gray-500">Stock</dt>
              <dd>
                <StockBadge available={component.available} />
              </dd>
              {component.description !== "" && (
                <>
                  <dt className="text-gray-500">Description</dt>
                  <dd>{component.description}</dd>
                </>
              )}
            </dl>
          </div>

          {canWrite && (
            <div>
              <h3 className="mb-2 text-sm font-semibold text-gray-900">Tags</h3>
              <TagEditor component={component} />
            </div>
          )}

          {target !== null && (
            <RequestForm
              component={component}
              target={target}
              rpasList={rpasList}
              onDone={() => {
                setTarget(null);
              }}
            />
          )}

          {!component.is_serialized && (
            <div>
              <h3 className="mb-2 text-sm font-semibold text-gray-900">Stock</h3>
              {component.lots.length === 0 && <p className="text-sm text-gray-500">None in stock yet.</p>}
              <ul className="divide-y rounded-md border">
                {component.lots.map((lot) => (
                  <li key={lot.id} className="flex items-center justify-between gap-3 px-3 py-2 text-sm">
                    <span>
                      <strong>{lot.quantity}</strong> {lot.condition}, {lot.origin}
                      {lot.source_rpas_name !== null && ` from ${lot.source_rpas_name}`}
                    </span>
                    {canWrite && lot.quantity > 0 && (
                      <button className={secondaryButton} onClick={() => { setTarget({ lot }); }}>
                        Request
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {component.is_serialized && (
            <div>
              <h3 className="mb-2 text-sm font-semibold text-gray-900">Units</h3>
              {component.units.length === 0 && <p className="text-sm text-gray-500">No units recorded yet.</p>}
              {component.units.length > 0 && (
                <div className="overflow-x-auto rounded-md border">
                  <table className="min-w-full divide-y text-sm">
                    <thead className="bg-gray-50 text-left text-xs uppercase text-gray-500">
                      <tr>
                        <th className="px-3 py-2">Serial</th>
                        <th className="px-3 py-2">Status</th>
                        <th className="px-3 py-2">Condition</th>
                        <th className="px-3 py-2">Drone</th>
                        <th className="px-3 py-2">Last serviced</th>
                        <th className="px-3 py-2" />
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {component.units.map((unit) => (
                        <tr key={unit.id}>
                          <td className="px-3 py-2 font-medium">{unit.serial_number}</td>
                          <td className="px-3 py-2">
                            <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${lifecycleStyle[unit.lifecycle]}`}>
                              {unit.lifecycle}
                            </span>
                          </td>
                          <td className="px-3 py-2">
                            {unit.condition}
                            {!unit.serviceable && <span className="ml-1 text-red-600">(unserviceable)</span>}
                          </td>
                          <td className="px-3 py-2">{unit.rpas_name ?? "—"}</td>
                          <td className="px-3 py-2">{unit.last_serviced ?? "—"}</td>
                          <td className="space-x-2 whitespace-nowrap px-3 py-2 text-right">
                            {canWrite && unit.lifecycle === "available" && unit.serviceable && (
                              <button className="text-blue-600 hover:underline" onClick={() => { setTarget({ unit }); }}>
                                Request
                              </button>
                            )}
                            {canWrite && unit.lifecycle === "available" && (
                              <button
                                className="text-red-600 hover:underline"
                                disabled={scrap.isPending}
                                onClick={() => {
                                  if (confirm(`Scrap unit #${unit.serial_number}?`)) scrap.mutate(unit);
                                }}
                              >
                                Scrap
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
              <ErrorText error={scrap.error} />
            </div>
          )}
        </div>
      )}
    </Modal>
  );
}
