"use client";

type Props = {
  name: string;
  location: string;
  cuisine: string;
};

export default function RestaurantCard({ name, location, cuisine }: Props) {
  return (
    <div
      style={{
        border: "1px solid #e5e5e5",
        borderRadius: 12,
        padding: 16,
        boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
        background: "white",
      }}
    >
      <h3 style={{ margin: "0 0 8px 0" }}>{name}</h3>
      <p style={{ margin: 0, color: "#666" }}>
        {location} · {cuisine}
      </p>
    </div>
  );
}
``;
