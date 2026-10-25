import { useMutation, useQueryClient } from "@tanstack/react-query";

import { API, type IComponentRequest, type IMe, postJson } from "./api";
import { ErrorText } from "./ui";

const statusStyle: Record<IComponentRequest["status"], string> = {
  pending: "bg-amber-100 text-amber-800",
  approved: "bg-blue-100 text-blue-800",
  installed: "bg-green-100 text-green-800",
  rejected: "bg-red-100 text-red-700",
  cancelled: "bg-gray-100 text-gray-600",
};

export default function RequestsList({ requests, me }: { requests: IComponentRequest[]; me: IMe | undefined }) {
  const queryClient = useQueryClient();
  const action = useMutation({
    mutationFn: async ({ id, name }: { id: number; name: "approve" | "reject" | "cancel" }) =>
      await postJson(`${API}/requests/${id}/${name}/`, {}),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["inventory"] });
    },
  });

  if (requests.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-sm text-gray-500">
        No requests yet. Open a component and choose Request to ask for it.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <ErrorText error={action.error} />
      <div className="overflow-x-auto rounded-lg border bg-white shadow-sm">
        <table className="min-w-full divide-y divide-gray-200 text-sm">
          <thead className="bg-gray-50 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
            <tr>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3">Component</th>
              <th className="px-4 py-3">Qty</th>
              <th className="px-4 py-3">Drone</th>
              <th className="px-4 py-3">Requested by</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {requests.map((r) => {
              const pending = r.status === "pending";
              const own = me?.id === r.requested_by;
              return (
                <tr key={r.id}>
                  <td className="whitespace-nowrap px-4 py-2 text-gray-500">
                    {new Date(r.date_created).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-2">
                    <div className="font-medium text-gray-900">{r.component_name}</div>
                    {r.serial_number != null && <div className="text-xs text-gray-500">#{r.serial_number}</div>}
                    {r.note !== "" && <div className="text-xs text-gray-500">{r.note}</div>}
                  </td>
                  <td className="px-4 py-2">{r.quantity}</td>
                  <td className="px-4 py-2">{r.rpas_name}</td>
                  <td className="px-4 py-2">{r.requested_by_name}</td>
                  <td className="px-4 py-2">
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusStyle[r.status]}`}>
                      {r.status}
                    </span>
                    {r.decided_by_name != null && (
                      <div className="text-xs text-gray-500">by {r.decided_by_name}</div>
                    )}
                  </td>
                  <td className="space-x-3 whitespace-nowrap px-4 py-2 text-right">
                    {pending && me?.can_approve === true && !own && (
                      <>
                        <button
                          className="font-medium text-green-700 hover:underline"
                          disabled={action.isPending}
                          onClick={() => { action.mutate({ id: r.id, name: "approve" }); }}
                        >
                          Approve
                        </button>
                        <button
                          className="font-medium text-red-600 hover:underline"
                          disabled={action.isPending}
                          onClick={() => { action.mutate({ id: r.id, name: "reject" }); }}
                        >
                          Reject
                        </button>
                      </>
                    )}
                    {pending && own && (
                      <button
                        className="text-gray-600 hover:underline"
                        disabled={action.isPending}
                        onClick={() => { action.mutate({ id: r.id, name: "cancel" }); }}
                      >
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
