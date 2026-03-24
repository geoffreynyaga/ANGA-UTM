import { useState, useRef, useEffect, type ReactNode } from "react";
import { useCookies } from "react-cookie";

// ─── Types & Constants ────────────────────────────────────────────────
const TOP_LEVELS = ["Pre-Flight", "Post-Flight"];

const CATEGORY_SUGGESTIONS = [
  "Approvals", "Hazard Check", "Safety", "Ground Checks", "Flight Ops",
  "Post-Flight", "Admin", "Systems", "Navigation", "Comms"
];

const API_ENDPOINT = "/api/flight_plans/checklists/add/";

function uid() {
  return Math.random().toString(36).slice(2, 8).toUpperCase();
}

export interface IChecklistItem {
  id: string;
  item_title: string;
  description: string;
  is_optional: boolean;
  category: string;
}

export interface IRpasModel {
  id: number;
  model_name: string | null;
  manufacturer: string;
  rpas_model_type: string;
}

export interface IChecklistGroup {
  title: string;
  items: IChecklistItem[];
}

export const AGRAS_T50_PREFLIGHT_CHECKLIST: IChecklistGroup[] = [
  {
    title: "Approvals & Mission Authorization",
    items: [
      { id: "1.4", item_title: "Regulatory Approvals", description: "Confirm approvals from KCAA, Company, and Site Owner.", is_optional: false, category: "Approvals" },
      { id: "1.6", item_title: "KCAA Documentation", description: "Verify KCAA documentation and insurance onsite.", is_optional: false, category: "Approvals" }
    ]
  },
  {
    title: "Hazard Check & Safety",
    items: [
      { id: "2.1", item_title: "Job-Site Hazards", description: "Identify powerlines, obstacles, persons, public roads, and mitigation steps.", is_optional: false, category: "Hazard Check" },
      { id: "2.2", item_title: "Crew Briefing", description: "Conduct full briefing: objectives, hazards, emergency plan, roles.", is_optional: false, category: "Safety" },
      { id: "2.3", item_title: "PPE Verification", description: "Verify all Personal Protective Equipment for PIC and VO.", is_optional: false, category: "Safety" },
      { id: "2.4", item_title: "Weather Minimums", description: "Wind ≤18 mph, visibility ≥3 SM, ceiling ≥500 ft AGL.", is_optional: false, category: "Safety" },
      { id: "2.5", item_title: "Emergency Plan", description: "Confirm emergency response contacts and action plan.", is_optional: false, category: "Safety" },
      { id: "2.6", item_title: "Launch Area Clearance", description: "Area cleared of personnel, livestock, and vehicles.", is_optional: false, category: "Hazard Check" }
    ]
  },
  {
    title: "Ground Checks - Structure & Propellers",
    items: [
      { id: "3.1", item_title: "Airframe & Arms", description: "Check for cracks, corrosion, delamination, and loose bolts.", is_optional: false, category: "Ground Checks" },
      { id: "3.3", item_title: "Locking Mechanism", description: "Ensure all arms and frame components are securely locked.", is_optional: false, category: "Ground Checks" },
      { id: "3.4", item_title: "Propellers & Hubs", description: "Inspect for cracks, chips, imbalance, and verify correct mounting.", is_optional: false, category: "Ground Checks" },
      { id: "3.5", item_title: "Motors & ESCs", description: "Smooth rotation, no unusual friction or noise.", is_optional: false, category: "Ground Checks" }
    ]
  },
  {
    title: "Ground Checks - Batteries & RC",
    items: [
      { id: "4.1", item_title: "Battery Compartment", description: "Clean terminals, locked battery, no corrosion.", is_optional: false, category: "Ground Checks" },
      { id: "4.2", item_title: "Aircraft Batteries", description: "No swelling, cell terminals", is_optional: false, category: "Ground Checks" },
      { id: "4.3", item_title: "RC Batteries & Terminals", description: "Check remote controller battery level", is_optional: false, category: "Ground Checks" },
      { id: "4.4", item_title: "Generator Check", description: "Verify fuel levels, oil.", is_optional: true, category: "Ground Checks" }
    ]
  },
  {
    title: "Ground Checks - Spray System",
    items: [
      { id: "5.1", item_title: "Spray/spreading Tank", description: "No leaks, cracks, secure mount.", is_optional: false, category: "Ground Checks" },
      { id: "5.3", item_title: "Nozzles", description: "Firmly intact", is_optional: false, category: "Ground Checks" }
    ]
  },
  {
    title: "Ground Checks - Systems & Vision",
    items: [
      { id: "6.4", item_title: "Firmware & Software", description: "Confirm no warnings.", is_optional: false, category: "Ground Checks" },
      { id: "6.5", item_title: "Failsafe / RTH", description: "RTH altitude is correct (think about trees and obstacles)", is_optional: false, category: "Ground Checks" },
      { id: "6.6", item_title: "Battery Settings", description: "RTH on battery low (at 30%)", is_optional: false, category: "Ground Checks" }
    ]
  },
  {
    title: "Flight Operations",
    items: [
      { id: "7.5", item_title: "Separation and segmentation", description: "Ensure separation between aircraft and ground crew.", is_optional: false, category: "Flight Ops" }
    ]
  }
];

export const AGRAS_T50_POSTFLIGHT_CHECKLIST: IChecklistGroup[] = [
  {
    title: "Post-Flight Procedures",
    items: [
      { id: "8.2", item_title: "Battery Inspection", description: "Check for heat, swelling, damage", is_optional: false, category: "Post-Flight" },
      { id: "8.3", item_title: "System Flush", description: "Flush spray system with clean water until lines run clear.", is_optional: false, category: "Post-Flight" },
      { id: "8.4", item_title: "Cleaning", description: "Clean airframe and remove chemical residue.", is_optional: false, category: "Post-Flight" },
      { id: "8.7", item_title: "Crew Debrief", description: "Conduct post-mission crew debrief.", is_optional: false, category: "Post-Flight" }
    ]
  },
  {
    title: "Administrative Requirements",
    items: [
      { id: "9.1", item_title: "Performance Metrics", description: "Record key metrics: area treated, bags spread etc", is_optional: false, category: "Admin" },
      { id: "9.3", item_title: "Whatsapp updates", description: "Update any necessary Whatsapp groups", is_optional: false, category: "Admin" }
    ]
  }
];

const INITIAL_STATE = {
  "Pre-Flight": AGRAS_T50_PREFLIGHT_CHECKLIST.map(g => ({ ...g, id: uid() })),
  "Post-Flight": AGRAS_T50_POSTFLIGHT_CHECKLIST.map(g => ({ ...g, id: uid() })),
};

// ─── Sub-components ───────────────────────────────────────────────────

function Badge({ children, color = "amber" }) {
  const colors = {
    amber: { bg: "#fff7ed", text: "#b45309", border: "#fdba74" },
    green: { bg: "#ecfdf3", text: "#15803d", border: "#86efac" },
    red:   { bg: "#fef2f2", text: "#b91c1c", border: "#fca5a5" },
    slate: { bg: "#f1f5f9", text: "#475569", border: "#cbd5e1" },
  };
  const c = colors[color];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center",
      padding: "2px 8px", borderRadius: 3,
      fontSize: 10, fontFamily: "'IBM Plex Mono', monospace",
      fontWeight: 600, letterSpacing: "0.08em",
      textTransform: "uppercase",
      background: c.bg, color: c.text,
      border: `1px solid ${c.border}`,
    }}>{children}</span>
  );
}

function ItemCard({ item, onUpdate, onDelete, dragHandleProps }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState({ ...item });

  function save() {
    onUpdate(draft);
    setEditing(false);
  }
  function cancel() {
    setDraft({ ...item });
    setEditing(false);
  }

  return (
    <div style={{
      background: "#ffffff", border: "1px solid #e2e8f0",
      borderRadius: 6, padding: "14px 16px",
      display: "flex", gap: 12, alignItems: "flex-start",
      transition: "border-color 0.15s",
      position: "relative",
    }}
      onMouseEnter={e => e.currentTarget.style.borderColor = "#cbd5e1"}
      onMouseLeave={e => e.currentTarget.style.borderColor = "#e2e8f0"}
    >
      {/* Drag handle */}
      <div {...dragHandleProps} style={{
        cursor: "grab", color: "#94a3b8", paddingTop: 2,
        fontSize: 14, userSelect: "none", flexShrink: 0,
      }} title="Drag to reorder">⠿</div>

      <div style={{ flex: 1, minWidth: 0 }}>
        {editing ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <input
              value={draft.item_title}
              onChange={e => setDraft(d => ({ ...d, item_title: e.target.value }))}
              placeholder="Item title"
              style={inputStyle}
            />
            <textarea
              value={draft.description}
              onChange={e => setDraft(d => ({ ...d, description: e.target.value }))}
              placeholder="Description"
              rows={2}
              style={{ ...inputStyle, resize: "vertical" }}
            />
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <input
                value={draft.category}
                list="category-suggestions"
                onChange={e => setDraft(d => ({ ...d, category: e.target.value }))}
                placeholder="Category"
                style={{ ...inputStyle, flex: 1, minWidth: 100 }}
              />
              <datalist id="category-suggestions">
                {CATEGORY_SUGGESTIONS.map(s => <option key={s} value={s} />)}
              </datalist>
              <label style={{ display: "flex", alignItems: "center", gap: 6, color: "#64748b", fontSize: 12, fontFamily: "'IBM Plex Mono', monospace", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={draft.is_optional}
                  onChange={e => setDraft(d => ({ ...d, is_optional: e.target.checked }))}
                  style={{ accentColor: "#0f766e" }}
                />
                Optional
              </label>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={save} style={btnPrimary}>Save</button>
              <button onClick={cancel} style={btnGhost}>Cancel</button>
            </div>
          </div>
        ) : (
          <div>
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 8 }}>
              <div>
                <span style={{ fontSize: 13, fontWeight: 600, color: "#0f172a", fontFamily: "'IBM Plex Sans', sans-serif" }}>
                  {item.item_title || <span style={{ color: "#555" }}>Untitled</span>}
                </span>
                {item.is_optional && <span style={{ marginLeft: 8 }}><Badge color="slate">Optional</Badge></span>}
              </div>
              <div style={{ display: "flex", gap: 4, flexShrink: 0 }}>
                <IconBtn title="Edit" onClick={() => setEditing(true)}>✎</IconBtn>
                <IconBtn title="Delete" onClick={onDelete} danger>✕</IconBtn>
              </div>
            </div>
            {(item.description || item.category) && (
              <div style={{
                marginTop: 6,
                display: "flex",
                alignItems: "flex-start",
                justifyContent: "space-between",
                gap: 10,
              }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  {item.description && (
                    <p style={{ margin: 0, fontSize: 12, color: "#64748b", lineHeight: 1.5 }}>{item.description}</p>
                  )}
                </div>
                {item.category && (
                  <span style={{
                    display: "inline-flex",
                    alignItems: "center",
                    padding: "1px 6px",
                    borderRadius: 999,
                    fontSize: 9,
                    fontFamily: "'IBM Plex Mono', monospace",
                    fontWeight: 500,
                    color: "#64748b",
                    background: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    whiteSpace: "nowrap",
                    textTransform: "uppercase",
                    letterSpacing: "0.04em",
                    flexShrink: 0,
                  }}>
                    {item.category}
                  </span>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function SectionBlock({ section, onUpdateTitle, onDeleteSection, onAddItem, onUpdateItem, onDeleteItem, onReorderItems }) {
  const [editingTitle, setEditingTitle] = useState(false);
  const [titleDraft, setTitleDraft] = useState(section.title);
  const dragItem = useRef(null);
  const dragOver = useRef(null);

  function saveTitle() {
    onUpdateTitle(titleDraft);
    setEditingTitle(false);
  }

  function handleDragStart(idx) { dragItem.current = idx; }
  function handleDragEnter(idx) { dragOver.current = idx; }
  function handleDragEnd() {
    if (dragItem.current === null || dragOver.current === null || dragItem.current === dragOver.current) return;
    const items = [...section.items];
    const [moved] = items.splice(dragItem.current, 1);
    items.splice(dragOver.current, 0, moved);
    onReorderItems(items);
    dragItem.current = null;
    dragOver.current = null;
  }

  return (
    <div style={{
      background: "#f8fafc", border: "1px solid #e2e8f0",
      borderRadius: 8, overflow: "hidden",
    }}>
      {/* Section header */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "10px 16px", background: "#f8fafc",
        borderBottom: "1px solid #e2e8f0",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flex: 1 }}>
          <span style={{ color: "#0f766e", fontSize: 11, fontFamily: "'IBM Plex Mono', monospace" }}>§</span>
          {editingTitle ? (
            <input
              autoFocus value={titleDraft}
              onChange={e => setTitleDraft(e.target.value)}
              onBlur={saveTitle}
              onKeyDown={e => { if (e.key === "Enter") saveTitle(); if (e.key === "Escape") { setTitleDraft(section.title); setEditingTitle(false); } }}
              style={{ ...inputStyle, fontSize: 13, fontWeight: 600, padding: "3px 8px", flex: 1 }}
            />
          ) : (
            <span
              onClick={() => setEditingTitle(true)}
              style={{ fontSize: 13, fontWeight: 600, color: "#1e293b", cursor: "pointer", fontFamily: "'IBM Plex Sans', sans-serif" }}
              title="Click to rename"
            >{section.title}</span>
          )}
          <Badge color="slate">{section.items.length} item{section.items.length !== 1 ? "s" : ""}</Badge>
        </div>
        <IconBtn title="Delete section" onClick={onDeleteSection} danger>✕</IconBtn>
      </div>

      {/* Items */}
      <div style={{ display: "flex", flexDirection: "column", gap: 6, padding: 12 }}>
        {section.items.length === 0 && (
          <div style={{ textAlign: "center", color: "#94a3b8", fontSize: 12, padding: "16px 0", fontFamily: "'IBM Plex Mono', monospace" }}>
            No items yet — add one below
          </div>
        )}
        {section.items.map((item, idx) => (
          <div
            key={item.id}
            draggable
            onDragStart={() => handleDragStart(idx)}
            onDragEnter={() => handleDragEnter(idx)}
            onDragEnd={handleDragEnd}
            onDragOver={e => e.preventDefault()}
          >
            <ItemCard
              item={item}
              onUpdate={updated => onUpdateItem(idx, updated)}
              onDelete={() => onDeleteItem(idx)}
              dragHandleProps={{}}
            />
          </div>
        ))}
        <button onClick={onAddItem} style={{
          ...btnGhost, marginTop: 4, fontSize: 12, justifyContent: "center",
          border: "1px dashed #cbd5e1", borderRadius: 6, padding: "8px 0",
          fontFamily: "'IBM Plex Mono', monospace",
        }}>
          + Add Item
        </button>
      </div>
    </div>
  );
}

function TopLevelPane({ name, sections, onAddSection, onUpdateSectionTitle, onDeleteSection, onAddItem, onUpdateItem, onDeleteItem, onReorderItems, isActive }) {
  const accentColor = name === "Pre-Flight" ? "#0f766e" : "#0369a1";
  const totalItems = sections.reduce((a, s) => a + s.items.length, 0);

  return (
    <div style={{ display: isActive ? "flex" : "none", flexDirection: "column", gap: 12 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 2px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ width: 3, height: 18, background: accentColor, borderRadius: 2, display: "inline-block" }} />
          <span style={{ fontSize: 11, fontFamily: "'IBM Plex Mono', monospace", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            {sections.length} section{sections.length !== 1 ? "s" : ""} · {totalItems} item{totalItems !== 1 ? "s" : ""}
          </span>
        </div>
        <button onClick={onAddSection} style={btnPrimary}>+ Add Section</button>
      </div>

      {sections.length === 0 && (
        <div style={{
          border: "1px dashed #cbd5e1", borderRadius: 8, padding: "40px 0",
          textAlign: "center", color: "#94a3b8",
          fontFamily: "'IBM Plex Mono', monospace", fontSize: 12,
        }}>
          No sections yet.<br />Add a section to get started.
        </div>
      )}

      {sections.map((section, si) => (
        <SectionBlock
          key={section.id}
          section={section}
          onUpdateTitle={t => onUpdateSectionTitle(si, t)}
          onDeleteSection={() => onDeleteSection(si)}
          onAddItem={() => onAddItem(si)}
          onUpdateItem={(ii, updated) => onUpdateItem(si, ii, updated)}
          onDeleteItem={ii => onDeleteItem(si, ii)}
          onReorderItems={items => onReorderItems(si, items)}
        />
      ))}
    </div>
  );
}

// ─── Main App ─────────────────────────────────────────────────────────

export default function ChecklistBuilder() {
  const [data, setData] = useState(INITIAL_STATE);
  const [activeTab, setActiveTab] = useState("Pre-Flight");
  const [saveStatus, setSaveStatus] = useState<null | "saving" | "saved" | "error">(null);

  // Setup State
  const [step, setStep] = useState<"setup" | "builder">("setup");
  const [title, setTitle] = useState("");
  const [selectedRpas, setSelectedRpas] = useState("");
  const [rpasModels, setRpasModels] = useState<IRpasModel[]>([]);
  const [cookies] = useCookies(["csrftoken"]);

  useEffect(() => {
    fetch("/api/rpas/v1/rpas-models/list/")
      .then(res => res.json())
      .then(data => setRpasModels(data))
      .catch(console.error);
  }, []);

  // ── Mutation helpers ──
  function updateSections(tab, fn) {
    setData(d => ({ ...d, [tab]: fn(d[tab]) }));
  }

  function addSection(tab) {
    updateSections(tab, sections => [
      ...sections,
      { id: uid(), title: "New Section", items: [] }
    ]);
  }

  function updateSectionTitle(tab, si, title) {
    updateSections(tab, sections => sections.map((s, i) => i === si ? { ...s, title } : s));
  }

  function deleteSection(tab, si) {
    if (!confirm("Delete this section and all its items?")) return;
    updateSections(tab, sections => sections.filter((_, i) => i !== si));
  }

  function addItem(tab, si) {
    updateSections(tab, sections => sections.map((s, i) => i !== si ? s : {
      ...s,
      items: [...s.items, {
        id: uid(), item_title: "", description: "", is_optional: false, category: ""
      }]
    }));
  }

  function updateItem(tab, si, ii, updated) {
    updateSections(tab, sections => sections.map((s, i) => i !== si ? s : {
      ...s,
      items: s.items.map((item, j) => j === ii ? { ...item, ...updated } : item)
    }));
  }

  function deleteItem(tab, si, ii) {
    updateSections(tab, sections => sections.map((s, i) => i !== si ? s : {
      ...s,
      items: s.items.filter((_, j) => j !== ii)
    }));
  }

  function reorderItems(tab, si, items) {
    updateSections(tab, sections => sections.map((s, i) => i !== si ? s : { ...s, items }));
  }

  function proceedToPostFlight() {
    setActiveTab("Post-Flight");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function buildExportJson() {
    const result = {};
    for (const tab of TOP_LEVELS) {
      result[tab] = data[tab].map(section => ({
        title: section.title,
        items: section.items.map(({ id, ...rest }) => rest),
      }));
    }
    return result;
  }

  async function handleSaveChecklist() {
    setSaveStatus("saving");

    const payload = { 
      checklist: buildExportJson(),
      title,
      rpas_model_id: selectedRpas || null
    };

    console.log("Submitting checklist payload:", payload);

    try {
      const response = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-CSRFToken": cookies.csrftoken || "",
        },
        body: JSON.stringify(payload),
      });
      setSaveStatus(response.ok ? "saved" : "error");
    } catch {
      setSaveStatus("error");
    }

    setTimeout(() => setSaveStatus(null), 3000);
  }

  const totalItems = TOP_LEVELS.reduce((a, tab) =>
    a + data[tab].reduce((b, s) => b + s.items.length, 0), 0);

  if (step === "setup") {
    return (
      <div style={{ minHeight: "100vh", background: "#f1f5f9", fontFamily: "'IBM Plex Sans', sans-serif", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ background: "#fff", padding: 32, borderRadius: 8, width: "100%", maxWidth: 400, boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1)" }}>
          <h2 style={{ margin: "0 0 20px", fontSize: 20 }}>Create a new checklist template</h2>
          
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: "block", marginBottom: 6, fontSize: 13, fontWeight: 600 }}>Checklist Name</label>
            <input 
              style={inputStyle} 
              value={title} 
              onChange={e => setTitle(e.target.value)} 
              placeholder="e.g. Agras T50 Checklist" 
            />
          </div>

          <div style={{ marginBottom: 24 }}>
            <label style={{ display: "block", marginBottom: 6, fontSize: 13, fontWeight: 600 }}>Select RPAS Model</label>
            <select style={inputStyle} value={selectedRpas} onChange={e => setSelectedRpas(e.target.value)}>
              <option value="">-- Select RPAS Model --</option>
              {rpasModels.map(r => (
                <option key={r.id} value={r.id.toString()}>
                  {r.manufacturer} - {r.model_name || r.rpas_model_type}
                </option>
              ))}
            </select>
          </div>

          <button 
            style={{ 
              ...btnPrimary, 
              width: "100%", 
              justifyContent: "center", 
              padding: "10px",
              opacity: (!title || !selectedRpas) ? 0.5 : 1,
              cursor: (!title || !selectedRpas) ? "not-allowed" : "pointer"
            }}
            onClick={() => setStep("builder")}
            disabled={!title || !selectedRpas}
          >
            Start Building
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: "100vh", background: "#f1f5f9",
      fontFamily: "'IBM Plex Sans', sans-serif",
      color: "#0f172a",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600;700&family=Oswald:wght@500;700&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #e2e8f0; }
        ::-webkit-scrollbar-thumb { background: #94a3b8; border-radius: 3px; }
      `}</style>

      {/* Header */}
      <div style={{
        borderBottom: "1px solid #cbd5e1", background: "#ffffff",
        padding: "0 24px",
        position: "sticky", top: 0, zIndex: 100,
      }}>
        <div style={{ maxWidth: 860, margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between", height: 56 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <span style={{ fontFamily: "'IBM Plex Sans', sans-serif", fontWeight: 700, fontSize: 18, color: "#0f172a" }}>
              Flight Checklist
            </span>
            <span style={{ color: "#cbd5e1", fontSize: 16 }}>|</span>
            <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 11, color: "#556069" }}>
              {totalItems} total items
            </span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ borderBottom: "1px solid #cbd5e1", background: "#ffffff" }}>
        <div style={{ maxWidth: 860, margin: "0 auto", display: "flex", gap: 0, padding: "0 24px" }}>
          {TOP_LEVELS.map(tab => {
            const isActive = activeTab === tab;
            const count = data[tab].reduce((a, s) => a + s.items.length, 0);
            const accent = tab === "Pre-Flight" ? "#0f766e" : "#0369a1";
            return (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                style={{
                  background: "none", border: "none", cursor: "pointer",
                  padding: "12px 20px",
                  borderBottom: isActive ? `2px solid ${accent}` : "2px solid transparent",
                  color: isActive ? "#0f172a" : "#64748b",
                  fontFamily: "'IBM Plex Sans', sans-serif",
                  fontWeight: isActive ? 600 : 400,
                  fontSize: 13,
                  display: "flex", alignItems: "center", gap: 8,
                  transition: "color 0.15s",
                }}
              >
                <span style={{
                  width: 7, height: 7, borderRadius: "50%",
                  background: isActive ? accent : "#94a3b8",
                  flexShrink: 0,
                }} />
                {tab}
                <span style={{
                  fontFamily: "'IBM Plex Mono', monospace", fontSize: 10,
                  background: "#e2e8f0", color: "#475569",
                  padding: "1px 6px", borderRadius: 10,
                }}>{count}</span>
              </button>
            );
          })}
        </div>
      </div>

      {activeTab === "Pre-Flight" && (
        <div style={{ maxWidth: 860, margin: "0 auto", padding: "16px 24px 0" }}>
          <div style={{
            background: "#ecfeff",
            border: "1px solid #99f6e4",
            borderRadius: 8,
            padding: "12px 14px",
            display: "flex",
            gap: 10,
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
          }}>
            <span style={{ color: "#0f172a", fontSize: 13 }}>
              When pre-flight checks are done, continue with the post-flight checklist.
            </span>
            <button onClick={proceedToPostFlight} style={btnPrimary}>
              Proceed to Post-Flight
            </button>
          </div>
        </div>
      )}

      {activeTab === "Post-Flight" && (
        <div style={{ maxWidth: 860, margin: "0 auto", padding: "16px 24px 0" }}>
          <div style={{
            background: "#eff6ff",
            border: "1px solid #bfdbfe",
            borderRadius: 8,
            padding: "12px 14px",
            display: "flex",
            gap: 10,
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
          }}>
            <span style={{ color: "#0f172a", fontSize: 13 }}>
              Finalize and save your full checklist to the mock API server.
            </span>
            <button
              onClick={handleSaveChecklist}
              style={{
                ...btnPrimary,
                background: saveStatus === "saved" ? "#16a34a" : saveStatus === "error" ? "#b91c1c" : "#0369a1",
                borderColor: saveStatus === "saved" ? "#16a34a" : saveStatus === "error" ? "#b91c1c" : "#0369a1",
                opacity: saveStatus === "saving" ? 0.7 : 1,
              }}
              disabled={saveStatus === "saving"}
            >
              {saveStatus === "saving"
                ? "Saving..."
                : saveStatus === "saved"
                  ? "Saved"
                  : saveStatus === "error"
                    ? "Retry Save"
                    : "Save Checklist"}
            </button>
          </div>
        </div>
      )}

      {/* Content */}
      <div style={{ maxWidth: 860, margin: "0 auto", padding: "24px 24px 80px" }}>
        {TOP_LEVELS.map(tab => (
          <TopLevelPane
            key={tab}
            name={tab}
            sections={data[tab]}
            isActive={activeTab === tab}
            onAddSection={() => addSection(tab)}
            onUpdateSectionTitle={(si, t) => updateSectionTitle(tab, si, t)}
            onDeleteSection={si => deleteSection(tab, si)}
            onAddItem={si => addItem(tab, si)}
            onUpdateItem={(si, ii, u) => updateItem(tab, si, ii, u)}
            onDeleteItem={(si, ii) => deleteItem(tab, si, ii)}
            onReorderItems={(si, items) => reorderItems(tab, si, items)}
          />
        ))}
      </div>
    </div>
  );
}

// ─── Shared Styles ────────────────────────────────────────────────────

function IconBtn({ children, onClick, danger = false, title }: { children: ReactNode; onClick: () => void; danger?: boolean; title: string }) {
  const [hov, setHov] = useState(false);
  return (
    <button
      title={title}
      onClick={onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        background: hov ? (danger ? "#fef2f2" : "#f8fafc") : "none",
        border: "1px solid " + (hov ? (danger ? "#fecaca" : "#e2e8f0") : "transparent"),
        color: danger ? (hov ? "#b91c1c" : "#94a3b8") : (hov ? "#0f172a" : "#64748b"),
        borderRadius: 4, cursor: "pointer",
        width: 24, height: 24, padding: 0,
        fontSize: 13, display: "flex", alignItems: "center", justifyContent: "center",
        transition: "all 0.1s",
      }}
    >{children}</button>
  );
}

const inputStyle = {
  background: "#ffffff", border: "1px solid #cbd5e1",
  borderRadius: 4, padding: "6px 10px",
  color: "#0f172a", fontSize: 13,
  outline: "none", width: "100%",
  fontFamily: "'IBM Plex Sans', sans-serif",
};

const btnPrimary = {
  background: "#0f766e", color: "#ffffff",
  border: "1px solid #0f766e",
  borderRadius: 5, cursor: "pointer",
  padding: "6px 14px", fontSize: 12, fontWeight: 600,
  fontFamily: "'IBM Plex Mono', monospace",
  display: "flex", alignItems: "center", gap: 4,
  letterSpacing: "0.02em",
};

const btnGhost = {
  background: "#ffffff", color: "#475569",
  border: "1px solid #cbd5e1",
  borderRadius: 5, cursor: "pointer",
  padding: "6px 14px", fontSize: 12,
  fontFamily: "'IBM Plex Mono', monospace",
  display: "flex", alignItems: "center", gap: 4,
};