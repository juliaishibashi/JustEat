"use client";

import { useState } from "react";

type Props = {
  menu: {
    id: number;
    name: string;
    price: number;
    detail: string | null;
  };
  onAdd: (menu: any, quantity: number) => void;
};

export default function MenuItem({ menu, onAdd }: Props) {
  const [qty, setQty] = useState(1);

  return (
    <div
      style={{
        borderBottom: "1px solid #eee",
        padding: "12px 0",
      }}
    >
      <h4>{menu.name}</h4>
      <p>{menu.detail}</p>
      <p>¥{menu.price}</p>

      <div>
        <input
          type="number"
          min={1}
          value={qty}
          onChange={(e) => setQty(Number(e.target.value))}
          style={{ width: 60 }}
        />
        <button onClick={() => onAdd(menu, qty)}>Add to cart</button>
      </div>
    </div>
  );
}
