"use client";

type Props = {
  value: string;
  onChange: (v: string) => void;
};

export default function SearchBar({ value, onChange }: Props) {
  return (
    <div style={{ marginBottom: "20px " }}>
      <input
        type="text"
        placeholder="Serch Just Eat"
        value={value}
        onChange={(e) => {
          console.log("SearchBar input:", e.target.value);
          onChange(e.target.value);
        }}
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "16px",
        }}
      />
    </div>
  );
}
