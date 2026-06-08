"use client";

import { useState } from "react";
import { Cormorant_Garamond } from "next/font/google";

const font = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["300", "400", "600"],
});
export default function Home() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState<string[]>([]);

  const sendMessage = async () => {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();

    setChat((prev) => [...prev, "You: " + message, "AI: " + data.response]);
    setMessage("");
  };

  return (
    <main className={`${font.className} min-h-screen bg-black text-red-700 flex items-center justify-center`}>
      <div className="w-full max-w-2xl p-10">

        <div className="mb-6 space-y-2">
          {chat.map((msg, i) => (
            <div key={i}>{msg}</div>
          ))}
        </div>

        <input
          className="w-full p-3 bg-black border border-red-900 text-red-500 placeholder-red-900 outline-none"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="type something..."
        />

        <button
          className="mt-3 px-4 py-2 border border-red-800 text-red-600 hover:bg-red-950 transition"
          onClick={sendMessage}
        >
          Send
        </button>

      </div>
    </main>
  );
}