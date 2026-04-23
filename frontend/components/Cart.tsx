"use client";

type CartItem = {
  menu: {
    id: number;
    name: string;
    price: number;
  };
  quantity: number;
};

export default function Cart({
  cart,
  onPlaceOrder,
}: {
  cart: CartItem[];
  onPlaceOrder: () => void;
}) {
  if (cart.length === 0) return null;

  const total = cart.reduce(
    (sum, item) => sum + item.menu.price * item.quantity,
    0,
  );

  return (
    <aside style={{ marginTop: 24, padding: 16, border: "1px solid #ddd" }}>
      <h3>Cart</h3>

      {cart.map((item) => (
        <div key={item.menu.id}>
          {item.menu.name} × {item.quantity}
        </div>
      ))}

      <p>Total: ¥{total}</p>

      <button onClick={onPlaceOrder}>Place Order</button>
    </aside>
  );
}
