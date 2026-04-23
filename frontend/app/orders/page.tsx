"use client";

import { useEffect, useState } from "react";

export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchText, setSearchText] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");

  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("http://localhost:8000/orders/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        // ✅ ここが一番大事
        if (Array.isArray(data)) {
          setOrders(data);
        } else {
          setOrders([]);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  const filteredOrders = orders.filter((order) => {
    const matchesSearch =
      order.restaurant_name.toLowerCase().includes(searchText.toLowerCase()) ||
      order.items.some((item) =>
        item.menu_name.toLowerCase().includes(searchText.toLowerCase()),
      );

    const matchesStatus =
      statusFilter === "ALL" || order.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <main style={{ padding: 16 }}>
      <h2>My Orders</h2>

      <input
        type="text"
        placeholder="Search orders…"
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        style={{ marginBottom: 16 }}
      />

      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setStatusFilter("ALL")}>All</button>
        <button onClick={() => setStatusFilter("PLACED")}>Placed</button>
        <button onClick={() => setStatusFilter("CONFIRMED")}>Confirmed</button>
      </div>

      {filteredOrders.length === 0 && <p>No matching orders</p>}

      {filteredOrders.map((order) => (
        <div
          key={order.id}
          style={{
            border: "1px solid #ddd",
            padding: 16,
            marginBottom: 16,
            borderRadius: 8,
          }}
        >
          <h4>{order.restaurant_name}</h4>

          <p>Status: {order.status}</p>
          <p>Ordered at: {new Date(order.created_at).toLocaleString()}</p>

          <ul>
            {order.items.map((item, idx) => (
              <li key={idx}>
                {item.menu_name} × {item.quantity} (¥{item.price})
              </li>
            ))}
          </ul>
        </div>
      ))}
    </main>
  );
}
