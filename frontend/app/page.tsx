"use client";

import { useEffect, useState } from "react";
import { fetchRestaurants } from "@/lib/api";

import SearchBar from "@/components/SearchBar";
import CuisineFilter from "@/components/CuisineFilter";
import RestaurantCard from "@/components/RestaurantCard";
import Link from "next/link";

type Restaurant = {
  id: number;
  name: string;
  location: string;
  cuisine: string;
};

export default function HomePage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [favourites, setFavourites] = useState<number[]>([]); // ⭐
  const [orders, setOrders] = useState<any[]>([]);
  const [searchText, setSearchText] = useState("");
  const [selectedCuisine, setSelectedCuisine] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);

    // generates ?name=... query
    const params = new URLSearchParams();

    if (searchText) params.set("search", searchText);
    if (selectedCuisine) params.set("cuisine", selectedCuisine);

    console.log("API query: ", params.toString());

    // finally(() =>) do it anyways
    fetchRestaurants(params.toString())
      .then(setRestaurants)
      .finally(() => setLoading(false));
  }, [searchText, selectedCuisine]);

  //for sort the fav
  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("http://localhost:8000/favourites/restaurants/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        // data: [{ restaurant_id: 1 }, { restaurant_id: 3 }]
        setFavourites(data.map((f) => f.restaurant_id));
      });
  }, []);

  const toggleFavourite = async (restaurantId: number) => {
    const token = localStorage.getItem("token");
    const isFav = favourites.includes(restaurantId);

    if (isFav) {
      await fetch(
        `http://localhost:8000/favourites/restaurant/${restaurantId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      setFavourites(favourites.filter((id) => id !== restaurantId));
    } else {
      await fetch(
        `http://localhost:8000/favourites/restaurant/${restaurantId}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      setFavourites([...favourites, restaurantId]);
    }
  };

  // ⭐ Favourite のレストランを上に並べた配列（表示用）
  const sortedRestaurants = [...restaurants].sort((a, b) => {
    const aFav = favourites.includes(a.id);
    const bFav = favourites.includes(b.id);

    // true → 1, false → 0
    // ⭐（1）が ☆（0）より前に来る
    return Number(bFav) - Number(aFav);
  });

  // for recomendation
  useEffect(() => {
    const token = localStorage.getItem("token");

    fetch("http://localhost:8000/orders/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setOrders(data);
        }
      });
  }, []);

  // cuisine ごとの注文回数を入れる箱
  const cuisineCount: Record<string, number> = {};

  // 注文履歴を1件ずつ見る
  orders.forEach((order) => {
    const restaurant = restaurants.find(
      (r) => r.name === order.restaurant_name,
    );

    if (!restaurant) return;

    const cuisine = restaurant.cuisine;

    // まだなければ 0 から
    if (!cuisineCount[cuisine]) {
      cuisineCount[cuisine] = 0;
    }

    // 回数を +1
    cuisineCount[cuisine] += 1;
  });

  const recommendedRestaurants = [...restaurants].sort((a, b) => {
    const aScore = cuisineCount[a.cuisine] || 0;
    const bScore = cuisineCount[b.cuisine] || 0;

    return bScore - aScore;
  });

  return (
    <main style={{ padding: 20 }}>
      <h2>Recommended for you</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
          gap: 16,
          marginBottom: 32,
        }}
      >
        {recommendedRestaurants.slice(0, 3).map((r) => (
          <RestaurantCard
            key={r.id}
            name={r.name}
            location={r.location}
            cuisine={r.cuisine}
          />
        ))}
      </div>

      <SearchBar value={searchText} onChange={setSearchText} />
      <CuisineFilter
        selectedCuisine={selectedCuisine}
        onSelect={setSelectedCuisine}
      />
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
            gap: 16,
          }}
        >
          {sortedRestaurants.map((r) => {
            const isFavourite = favourites.includes(r.id);

            return (
              <div
                key={r.id}
                style={{
                  position: "relative",
                  marginBottom: 16,
                }}
              >
                {/* ⭐ Favourite ボタン */}
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    toggleFavourite(r.id);
                  }}
                  style={{
                    position: "absolute",
                    top: 8,
                    right: 8,
                    background: "none",
                    border: "none",
                    fontSize: 20,
                    cursor: "pointer",
                  }}
                >
                  {isFavourite ? "⭐" : "☆"}
                </button>

                {/* レストランカード */}
                <Link
                  href={`/restaurants/${r.id}`}
                  style={{ textDecoration: "none", color: "inherit" }}
                >
                  <RestaurantCard
                    name={r.name}
                    location={r.location}
                    cuisine={r.cuisine}
                  />
                </Link>
              </div>
            );
          })}
        </div>
      )}
    </main>
  );
}
