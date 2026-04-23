"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import MenuItem from "@/components/MenuItem";
import Cart from "@/components/Cart";

type Menu = {
  id: number;
  name: string;
  price: number;
  detail: string | null;
};

type CartItem = {
  menu: Menu;
  quantity: number;
};

export default function RestaurantPage() {
  const params = useParams();
  const restaurantId = Number(params.id);

  const [menus, setMenus] = useState<Menu[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);

  // ✅ メニュー取得（完全に正しい形）
  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch(`http://localhost:8000/menus/${restaurantId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("=== menus API response:", data);
        setMenus(Array.isArray(data) ? data : []);
      });
  }, [restaurantId]);

  // ✅ カートに追加
  const addToCart = (menu: Menu, quantity: number) => {
    setCart((prev) => {
      const existing = prev.find((i) => i.menu.id === menu.id);
      if (existing) {
        return prev.map((i) =>
          i.menu.id === menu.id ? { ...i, quantity: i.quantity + quantity } : i,
        );
      }
      return [...prev, { menu, quantity }];
    });
  };

  // ✅ 注文確定
  const placeOrder = async () => {
    const token = localStorage.getItem("token");

    const payload = {
      restaurant_id: restaurantId,
      items: cart.map((item) => ({
        menu_id: item.menu.id,
        quantity: item.quantity,
      })),
    };

    console.log("order payload:", payload);

    const res = await fetch("http://localhost:8000/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      alert("Failed to place order");
      return;
    }

    alert("Order placed successfully");
    setCart([]);
  };

  return (
    <main style={{ padding: 20 }}>
      <h2>Menus</h2>

      {menus.map((menu) => (
        <MenuItem key={menu.id} menu={menu} onAdd={addToCart} />
      ))}

      <Cart cart={cart} onPlaceOrder={placeOrder} />
    </main>
  );
}
