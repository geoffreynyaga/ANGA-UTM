import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { apiFetch, useMe } from "../Inventory/api";
import { ErrorText, Field, Modal, controlClass, inputClass, primaryButton, secondaryButton } from "../Inventory/ui";

const API = "/api/maintenance/v1";

interface IDrone {
  id: number;
  name: string;
  rpas_serial: string;
  last_serviced: string | null;
  record_count: number;
}

interface IRecord {
  id: number;
  rpas: number;
  rpas_name: string;
  performed_by_name: string;
  date_performed: string;
  service_type: "scheduled" | "repair" | "inspection";
  description: string;
  report: string | null;
  components_used: Array<{ id: number; component_name: string; serial_number?: string | null; quantity: number }>;
  units_serviced: Array<{ id: number; component_name: string; serial_number: string }>;
}

interface IInstallable {
  id: number;
  component_name: string;
  serial_number: string | null;
  quantity: number;
}

interface IUnit {
  id: number;
  component_name: string;
  serial_number: string;
  last_serviced: string | null;
}

const SERVICE_TYPES: Record<IRecord["service_type"], string> = {
  scheduled: "Scheduled service",
  repair: "Repair",
  inspection: "Inspection",
};

const today = () => new Date().toISOString().slice(0, 10);

function NewRecordDialog({ drones, initialDrone, onClose }: { drones: IDrone[]; initialDrone: number | null; onClose: () => void }) {
  const queryClient = useQueryClient();
  const [rpas, setRpas] = useState(initialDrone !== null ? String(initialDrone) : "");

  const installable = useQuery({
    queryKey: ["maintenance", "installable", rpas],
    queryFn: async () => await apiFetch<IInstallable[]>(`${API}/installable-requests/?rpas=${rpas}`),
    enabled: rpas !== "",
  });
  const units = useQuery({
    queryKey: ["maintenance", "units", rpas],
    queryFn: async () => await apiFetch<IUnit[]>(`${API}/units/?rpas=${rpas}`),
    enabled: rpas !== "",
  });

  const mutation = useMutation({
    mutationFn: async (form: FormData) => await apiFetch(`${API}/records/`, { method: "POST", body: form }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["maintenance"] });
      await queryClient.invalidateQueries({ queryKey: ["inventory"] });
      onClose();
    },
  });

  return (
    <Modal title="New maintenance record" onClose={onClose} wide>
      <form
        className="space-y-4"
        onSubmit={(event) => {
          event.preventDefault();
          const form = new FormData(event.currentTarget);
          if ((form.get("report") as File | null)?.size === 0) form.delete("report");
          mutation.mutate(form);
        }}
      >
        <div className="grid gap-4 sm:grid-cols-3">
          <Field label="Drone">
            <select name="rpas" required className={inputClass} value={rpas} onChange={(e) => { setRpas(e.target.value); }}>
              <option value="">Select a drone</option>
              {drones.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name} ({d.rpas_serial})
                </option>
              ))}
            </select>
          </Field>
          <Field label="Date of work">
            <input type="date" name="date_performed" required defaultValue={today()} className={inputClass} />
          </Field>
          <Field label="Type of work">
            <select name="service_type" className={inputClass}>
              {Object.entries(SERVICE_TYPES).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </Field>
        </div>
        <Field label="Work carried out">
          <textarea name="description" required rows={3} className={inputClass} />
        </Field>

        {rpas !== "" && (
          <div className="grid gap-4 sm:grid-cols-2">
            <fieldset className="rounded-md border p-3">
              <legend className="px-1 text-sm font-medium text-gray-700">Components fitted</legend>
              <p className="mb-2 text-xs text-gray-500">Approved requests for this drone. They are marked as installed.</p>
              {installable.data?.length === 0 && (
                <p className="text-sm text-gray-500">No approved requests. Request parts from the Components page first.</p>
              )}
              {installable.data?.map((r) => (
                <label key={r.id} className="flex items-center gap-2 py-0.5 text-sm">
                  <input type="checkbox" name="component_requests" value={r.id} />
                  {r.quantity} × {r.component_name}
                  {r.serial_number !== null && <span className="text-gray-500">#{r.serial_number}</span>}
                </label>
              ))}
            </fieldset>
            <fieldset className="rounded-md border p-3">
              <legend className="px-1 text-sm font-medium text-gray-700">Units serviced</legend>
              <p className="mb-2 text-xs text-gray-500">Their last serviced date is set to the date of work.</p>
              {units.data?.length === 0 && <p className="text-sm text-gray-500">No tracked units.</p>}
              <div className="max-h-48 overflow-y-auto">
                {units.data?.map((u) => (
                  <label key={u.id} className="flex items-center gap-2 py-0.5 text-sm">
                    <input type="checkbox" name="serviced_units" value={u.id} />
                    {u.component_name} <span className="text-gray-500">#{u.serial_number}</span>
                  </label>
                ))}
              </div>
            </fieldset>
          </div>
        )}

        <Field label="Report (PDF)">
          <input type="file" name="report" accept="application/pdf,.pdf" className="text-sm" />
        </Field>
        <ErrorText error={mutation.error} />
        <div className="flex gap-2">
          <button type="submit" className={primaryButton} disabled={mutation.isPending}>
            Save record
          </button>
          <button type="button" className={secondaryButton} onClick={onClose}>
            Cancel
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default function MaintenancePage() {
  const { data: me } = useMe();
  const drones = useQuery({
    queryKey: ["maintenance", "drones"],
    queryFn: async () => await apiFetch<IDrone[]>(`${API}/rpas/`),
  });
  const records = useQuery({
    queryKey: ["maintenance", "records"],
    queryFn: async () => await apiFetch<IRecord[]>(`${API}/records/`),
  });
  const template = useQuery({
    queryKey: ["maintenance", "template"],
    queryFn: async () => await apiFetch<{ url: string }>(`${API}/report-template/`),
  });

  const [droneFilter, setDroneFilter] = useState<number | null>(null);
  const [creating, setCreating] = useState(false);

  const droneList = drones.data ?? [];
  const recordList = (records.data ?? []).filter((r) => droneFilter === null || r.rpas === droneFilter);

  return (
    <div className="mx-auto w-full max-w-7xl space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Maintenance</h1>
          <p className="text-sm text-gray-500">Service history for each drone, with the components fitted and the signed reports.</p>
        </div>
        <div className="flex gap-2">
          {template.data !== undefined && (
            <a href={template.data.url} download className={secondaryButton}>
              Download report template (.docx)
            </a>
          )}
          {me !== undefined && !me.read_only && (
            <button className={primaryButton} onClick={() => { setCreating(true); }}>
              New record
            </button>
          )}
        </div>
      </div>

      <ErrorText error={drones.error ?? records.error} />

      <section className="space-y-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">Drones</h2>
        <div className="overflow-x-auto rounded-lg border bg-white shadow-sm">
          <table className="min-w-full divide-y divide-gray-200 text-sm">
            <thead className="bg-gray-50 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
              <tr>
                <th className="px-4 py-3">Drone</th>
                <th className="px-4 py-3">Serial</th>
                <th className="px-4 py-3">Last serviced</th>
                <th className="px-4 py-3">Records</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {droneList.map((d) => (
                <tr
                  key={d.id}
                  onClick={() => { setDroneFilter(droneFilter === d.id ? null : d.id); }}
                  className={`cursor-pointer hover:bg-gray-50 ${droneFilter === d.id ? "bg-blue-50" : ""}`}
                >
                  <td className="px-4 py-2 font-medium text-gray-900">{d.name}</td>
                  <td className="px-4 py-2">{d.rpas_serial}</td>
                  <td className="px-4 py-2">{d.last_serviced ?? <span className="text-amber-700">Never</span>}</td>
                  <td className="px-4 py-2">{d.record_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="space-y-3">
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">Records</h2>
          <select
            className={controlClass}
            value={droneFilter ?? ""}
            onChange={(e) => { setDroneFilter(e.target.value === "" ? null : Number(e.target.value)); }}
          >
            <option value="">All drones</option>
            {droneList.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </select>
        </div>
        {recordList.length === 0 ? (
          <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-sm text-gray-500">
            No maintenance records yet.
          </div>
        ) : (
          <ul className="space-y-3">
            {recordList.map((r) => (
              <li key={r.id} className="rounded-lg border bg-white p-4 shadow-sm">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <div className="font-medium text-gray-900">
                      {SERVICE_TYPES[r.service_type]} · {r.rpas_name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {r.date_performed} by {r.performed_by_name}
                    </div>
                  </div>
                  {r.report !== null && (
                    <a href={r.report} target="_blank" rel="noreferrer" className="text-sm font-medium text-blue-600 hover:underline">
                      View report (PDF)
                    </a>
                  )}
                </div>
                <p className="mt-2 whitespace-pre-line text-sm text-gray-700">{r.description}</p>
                {(r.components_used.length > 0 || r.units_serviced.length > 0) && (
                  <div className="mt-3 flex flex-wrap gap-2 text-xs">
                    {r.components_used.map((c) => (
                      <span key={`c${c.id}`} className="rounded bg-blue-50 px-2 py-1 text-blue-800">
                        Fitted {c.quantity} × {c.component_name}
                        {c.serial_number != null && ` #${c.serial_number}`}
                      </span>
                    ))}
                    {r.units_serviced.map((u) => (
                      <span key={`u${u.id}`} className="rounded bg-gray-100 px-2 py-1 text-gray-700">
                        Serviced {u.component_name} #{u.serial_number}
                      </span>
                    ))}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>

      {creating && (
        <NewRecordDialog
          drones={droneList}
          initialDrone={droneFilter}
          onClose={() => { setCreating(false); }}
        />
      )}
    </div>
  );
}
