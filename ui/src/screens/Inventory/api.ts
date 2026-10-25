import { useQuery } from "@tanstack/react-query";

export const API = "/api/inventory/v1";

export interface IAircraftModel {
  id: number;
  manufacturer: string;
  name: string;
}

export interface IRpas {
  id: number;
  name: string;
  rpas_serial: string;
  aircraft_model: number | null;
}

export interface IComponent {
  id: number;
  name: string;
  part_number: string | null;
  description: string;
  image: string | null;
  diagram_name: string;
  diagram_number: string;
  aircraft_models: number[];
  tags: string[];
  is_serialized: boolean;
  parent: number | null;
  parent_name?: string | null;
  status: "approved" | "pending";
  available: number;
  lot_quantity: number;
  available_units: number;
  unserviceable_units: number;
  has_stock_history: boolean;
}

export interface IStockLot {
  id: number;
  quantity: number;
  condition: "new" | "used";
  origin: "purchased" | "salvaged";
  source_rpas_name: string | null;
}

export interface IUnit {
  id: number;
  serial_number: string;
  condition: "new" | "used";
  origin: "purchased" | "salvaged";
  source_rpas_name: string | null;
  serviceable: boolean;
  lifecycle: "available" | "reserved" | "issued" | "installed" | "scrapped";
  rpas_name: string | null;
  last_serviced: string | null;
}

export interface IComponentDetail extends IComponent {
  lots: IStockLot[];
  units: IUnit[];
}

export interface IComponentRequest {
  id: number;
  component_type: number;
  component_name: string;
  rpas: number;
  rpas_name: string;
  serial_number?: string | null;
  quantity: number;
  note: string;
  status: "pending" | "approved" | "rejected" | "cancelled" | "installed";
  requested_by: number;
  requested_by_name: string;
  decided_by_name?: string | null;
  date_created: string;
}

export interface IMe {
  id: number;
  can_approve: boolean;
  read_only: boolean;
}

function csrfToken(): string {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match !== null ? match[1] : "";
}

function errorMessage(body: unknown): string {
  if (typeof body === "string") return body;
  if (Array.isArray(body)) return body.map(errorMessage).join(" ");
  if (body !== null && typeof body === "object") {
    return Object.values(body).map(errorMessage).join(" ");
  }
  return "Something went wrong.";
}

export async function apiFetch<T>(url: string, options: RequestInit = {}): Promise<T> {
  const isForm = options.body instanceof FormData;
  const response = await fetch(url, {
    credentials: "same-origin",
    ...options,
    headers: {
      ...(isForm ? {} : { "Content-Type": "application/json" }),
      "X-CSRFToken": csrfToken(),
      ...options.headers,
    },
  });
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) throw new Error(errorMessage(body));
  return body as T;
}

export const postJson = async <T>(url: string, data: unknown, method = "POST"): Promise<T> =>
  await apiFetch<T>(url, { method, body: JSON.stringify(data) });

export const useMe = () =>
  useQuery({ queryKey: ["inventory", "me"], queryFn: async () => await apiFetch<IMe>(`${API}/me/`) });

export const useComponents = () =>
  useQuery({
    queryKey: ["inventory", "components"],
    queryFn: async () => await apiFetch<IComponent[]>(`${API}/components/`),
  });

export const useComponentDetail = (id: number) =>
  useQuery({
    queryKey: ["inventory", "components", id],
    queryFn: async () => await apiFetch<IComponentDetail>(`${API}/components/${id}/`),
  });

export const useRequests = () =>
  useQuery({
    queryKey: ["inventory", "requests"],
    queryFn: async () => await apiFetch<IComponentRequest[]>(`${API}/requests/`),
  });

export const useAircraftModels = () =>
  useQuery({
    queryKey: ["inventory", "aircraft-models"],
    queryFn: async () => await apiFetch<IAircraftModel[]>(`${API}/aircraft-models/`),
  });

export const useRpas = () =>
  useQuery({
    queryKey: ["inventory", "rpas"],
    queryFn: async () => await apiFetch<IRpas[]>(`${API}/rpas/`),
  });

export const aircraftName = (model: IAircraftModel) => `${model.manufacturer} ${model.name}`;
