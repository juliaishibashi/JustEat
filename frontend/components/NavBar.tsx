"use client";

import Link from "next/link";

export default function NavBar() {
  return (
    <nav
      style={{
        display: "flex",
        gap: 20,
        padding: 16,
        borderBottom: "1px solid #ddd",
        marginBottom: 24,
      }}
    >
      <Link href="/">Restaurants</Link>
      <Link href="/orders">My Orders</Link>
    </nav>
  );
}
