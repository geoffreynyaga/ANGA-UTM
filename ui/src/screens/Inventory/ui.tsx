import { type ReactNode, useEffect } from "react";

export const controlClass =
  "rounded-md border-gray-300 text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500";

export const inputClass =
  "block w-full rounded-md border-gray-300 text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500";

export const primaryButton =
  "inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50";

export const secondaryButton =
  "inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50";

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-gray-700">{label}</span>
      {children}
    </label>
  );
}

export function Modal({
  title,
  onClose,
  children,
  wide = false,
}: {
  title: string;
  onClose: () => void;
  children: ReactNode;
  wide?: boolean;
}) {
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("keydown", onKey);
    };
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-gray-900/50 p-4 sm:p-8">
      <div className="absolute inset-0" onClick={onClose} />
      <div
        role="dialog"
        aria-label={title}
        className={`relative w-full rounded-lg bg-white shadow-xl ${wide ? "max-w-3xl" : "max-w-lg"}`}
      >
        <div className="flex items-center justify-between border-b px-5 py-3">
          <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
          <button onClick={onClose} className="rounded p-1 text-gray-400 hover:text-gray-600" aria-label="Close">
            ✕
          </button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}

export function ErrorText({ error }: { error: Error | null }) {
  if (error === null) return null;
  return <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error.message}</p>;
}

export function ComponentImage({ src, name, className }: { src: string | null; name: string; className: string }) {
  if (src === null || src === "") {
    return (
      <div className={`flex items-center justify-center bg-gray-100 text-xs text-gray-400 ${className}`}>
        No image
      </div>
    );
  }
  return <img src={src} alt={name} className={`bg-white object-contain ${className}`} />;
}

export function StockBadge({ available }: { available: number }) {
  if (available === 0) {
    return (
      <span className="inline-flex rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">
        Out of stock
      </span>
    );
  }
  return (
    <span className="inline-flex rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800">
      {available} available
    </span>
  );
}
