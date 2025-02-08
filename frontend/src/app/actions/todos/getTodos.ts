"use server";

import axios from "@/utils/axios";

export default async function getTodos() {
  try {
    return await axios.get("https://jsonplaceholder.typicode.com/photos");
  } catch {}
}
