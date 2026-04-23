"use client";

type Props = {
  selectedCuisine: string | null;
  onSelect: (cuisine: string | null) => void;
};

const CUISINES = [
  { id: "Cafe", label: "Cafe", icon: "☕" },
  { id: "Italian", label: "Italian", icon: "🍕" },
  { id: "Japanese", label: "Japanese", icon: "🍣" },
  { id: "American", label: "American", icon: "🍔" },
  { id: "Indian", label: "Indian", icon: "🍛" },
];

export default function CuisineFilter({ selectedCuisine, onSelect }: Props) {
  return (
    <div
      style={{ display: "flex", gap: 12, marginBottom: 20, overflowX: "auto" }}
    >
      {CUISINES.map((c) => (
        <button
          key={c.id}
          onClick={() => onSelect(selectedCuisine === c.id ? null : c.id)}
          style={{
            padding: "8px 12px",
            borderRadius: 20,
            border:
              selectedCuisine === c.id ? "2px solid black" : "1px solid #ccc",
            background: "white",
            cursor: "pointer",
            whiteSpace: "nowrap",
          }}
        >
          <span style={{ fontSize: 18 }}>{c.icon}</span> {c.label}
        </button>
      ))}
    </div>
  );
}
