import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { API, type IAircraftModel, type IComponent, type IRpas, aircraftName, apiFetch, postJson } from "./api";
import { ComponentImage, ErrorText, Field, Modal, StockBadge, inputClass, primaryButton, secondaryButton } from "./ui";

function ProposeForm({
  initialName,
  aircraftModels,
  onCreated,
  onBack,
}: {
  initialName: string;
  aircraftModels: IAircraftModel[];
  onCreated: (component: IComponent) => void;
  onBack: () => void;
}) {
  const mutation = useMutation({
    mutationFn: async (form: FormData) =>
      await apiFetch<IComponent>(`${API}/components/`, { method: "POST", body: form }),
    onSuccess: onCreated,
  });

  return (
    <form
      className="space-y-4"
      onSubmit={(event) => {
        event.preventDefault();
        const form = new FormData(event.currentTarget);
        const tags = String(form.get("tag_text") ?? "")
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean);
        form.delete("tag_text");
        tags.forEach((tag) => { form.append("tags", tag); });
        if ((form.get("image") as File | null)?.size === 0) form.delete("image");
        mutation.mutate(form);
      }}
    >
      <p className="text-sm text-gray-600">
        New components are reviewed by an admin, who merges any duplicates. You can add stock straight away.
      </p>
      <Field label="Name">
        <input name="name" required defaultValue={initialName} className={inputClass} />
      </Field>
      <Field label="Part number">
        <input name="part_number" className={inputClass} placeholder="Optional" />
      </Field>
      <Field label="Description">
        <textarea name="description" rows={2} className={inputClass} />
      </Field>
      <Field label="Tags">
        <input name="tag_text" className={inputClass} placeholder="Comma separated, e.g. generator, fuel" />
      </Field>
      <fieldset>
        <legend className="mb-1 text-sm font-medium text-gray-700">Fits aircraft</legend>
        <div className="flex flex-wrap gap-x-4 gap-y-1">
          {aircraftModels.map((model) => (
            <label key={model.id} className="flex items-center gap-2 text-sm">
              <input type="checkbox" name="aircraft_models" value={model.id} />
              {aircraftName(model)}
            </label>
          ))}
        </div>
      </fieldset>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="is_serialized" value="true" />
        Track each item by serial number (batteries, controllers, tanks)
      </label>
      <Field label="Photo">
        <input type="file" name="image" accept="image/*" className="text-sm" />
      </Field>
      <ErrorText error={mutation.error} />
      <div className="flex gap-2">
        <button type="submit" className={primaryButton} disabled={mutation.isPending}>
          Add component
        </button>
        <button type="button" className={secondaryButton} onClick={onBack}>
          Back
        </button>
      </div>
    </form>
  );
}

function StockForm({
  component,
  rpasList,
  onDone,
  onBack,
}: {
  component: IComponent;
  rpasList: IRpas[];
  onDone: () => void;
  onBack: () => void;
}) {
  const queryClient = useQueryClient();
  const [origin, setOrigin] = useState("purchased");
  const mutation = useMutation({
    mutationFn: async (data: Record<string, unknown>) => await postJson(`${API}/stock/`, data),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["inventory"] });
      onDone();
    },
  });

  return (
    <form
      className="space-y-4"
      onSubmit={(event) => {
        event.preventDefault();
        const form = new FormData(event.currentTarget);
        const sourceRpas = form.get("source_rpas");
        mutation.mutate({
          component_type: component.id,
          condition: form.get("condition"),
          origin,
          source_rpas: origin === "salvaged" && sourceRpas !== "" ? Number(sourceRpas) : null,
          ...(component.is_serialized
            ? {
                serial_numbers: String(form.get("serial_numbers")).split("\n").filter((s) => s.trim() !== ""),
                last_serviced: form.get("last_serviced") !== "" ? form.get("last_serviced") : null,
              }
            : { quantity: Number(form.get("quantity")) }),
        });
      }}
    >
      <div className="flex items-center gap-3 rounded-md border p-3">
        <ComponentImage src={component.image} name={component.name} className="h-12 w-12 rounded" />
        <div className="flex-1">
          <div className="text-sm font-medium">{component.name}</div>
          <StockBadge available={component.available} />
        </div>
      </div>
      {component.is_serialized ? (
        <>
          <Field label="Serial numbers, one per line">
            <textarea name="serial_numbers" required rows={4} className={inputClass} />
          </Field>
          <Field label="Last serviced">
            <input type="date" name="last_serviced" className={inputClass} />
          </Field>
        </>
      ) : (
        <Field label="Quantity to add">
          <input type="number" name="quantity" min={1} defaultValue={1} required className={inputClass} />
        </Field>
      )}
      <div className="grid grid-cols-2 gap-3">
        <Field label="Condition">
          <select name="condition" className={inputClass}>
            <option value="new">New</option>
            <option value="used">Used</option>
          </select>
        </Field>
        <Field label="Origin">
          <select className={inputClass} value={origin} onChange={(e) => { setOrigin(e.target.value); }}>
            <option value="purchased">Purchased</option>
            <option value="salvaged">Salvaged from a drone</option>
          </select>
        </Field>
      </div>
      {origin === "salvaged" && (
        <Field label="Salvaged from">
          <select name="source_rpas" className={inputClass}>
            <option value="">Unknown drone</option>
            {rpasList.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} ({r.rpas_serial})
              </option>
            ))}
          </select>
        </Field>
      )}
      <ErrorText error={mutation.error} />
      <div className="flex gap-2">
        <button type="submit" className={primaryButton} disabled={mutation.isPending}>
          Add to stock
        </button>
        <button type="button" className={secondaryButton} onClick={onBack}>
          Back
        </button>
      </div>
    </form>
  );
}

export default function AddStockDialog({
  components,
  aircraftModels,
  rpasList,
  onClose,
}: {
  components: IComponent[];
  aircraftModels: IAircraftModel[];
  rpasList: IRpas[];
  onClose: () => void;
}) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<IComponent | null>(null);
  const [proposing, setProposing] = useState(false);

  const q = query.trim().toLowerCase();
  const matches =
    q === ""
      ? []
      : components
          .filter((c) => [c.name, c.part_number ?? "", ...c.tags].some((t) => t.toLowerCase().includes(q)))
          .slice(0, 8);

  if (proposing) {
    return (
      <Modal title="New component" onClose={onClose}>
        <ProposeForm
          initialName={query}
          aircraftModels={aircraftModels}
          onCreated={(component) => {
            setProposing(false);
            setSelected({ ...component, available: 0 });
          }}
          onBack={() => { setProposing(false); }}
        />
      </Modal>
    );
  }

  if (selected !== null) {
    return (
      <Modal title="Add stock" onClose={onClose}>
        <StockForm component={selected} rpasList={rpasList} onDone={onClose} onBack={() => { setSelected(null); }} />
      </Modal>
    );
  }

  return (
    <Modal title="Add stock" onClose={onClose}>
      <div className="space-y-3">
        <Field label="Find the component first, so it is not listed twice">
          <input
            autoFocus
            className={inputClass}
            value={query}
            onChange={(e) => { setQuery(e.target.value); }}
            placeholder="Name, part number or tag"
          />
        </Field>
        <ul className="divide-y rounded-md border empty:hidden">
          {matches.map((c) => (
            <li key={c.id}>
              <button
                className="flex w-full items-center gap-3 px-3 py-2 text-left hover:bg-gray-50"
                onClick={() => { setSelected(c); }}
              >
                <ComponentImage src={c.image} name={c.name} className="h-10 w-10 rounded" />
                <span className="flex-1">
                  <span className="block text-sm font-medium">{c.name}</span>
                  <span className="block text-xs text-gray-500">{c.part_number}</span>
                </span>
                <StockBadge available={c.available} />
              </button>
            </li>
          ))}
        </ul>
        {q !== "" && (
          <button className="text-sm text-blue-600 hover:underline" onClick={() => { setProposing(true); }}>
            {matches.length === 0 ? "No match. " : "Not in this list? "}Add &ldquo;{query.trim()}&rdquo; as a new component
          </button>
        )}
      </div>
    </Modal>
  );
}
