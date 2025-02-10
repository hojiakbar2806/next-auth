"use server";

import { cookies } from "next/headers";

export async function logoutAction() {
  try {
    const cookieStore = await cookies();
    cookieStore.delete("refresh_token");
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
}
