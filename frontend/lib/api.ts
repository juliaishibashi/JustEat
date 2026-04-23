export async function fetchRestaurants(query: string) {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/login";
    return;
  }
  const res = await fetch(`http://localhost:8000/restaurants/?${query}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch restaurants");
  }

  return res.json();
}
