"use server";

import axios from "@/utils/axios";
import { cookies } from "next/headers";

export async function setOauthToken(code: string) {
  try {
    const res = await axios.get(`/auth/token?code=${code}`);
    const cookieStore = await cookies();
    cookieStore.set("refresh_token", res.data.refresh_token, {
      httpOnly: true,
      sameSite: "lax",
      secure: true,
      priority: "high",
    });
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
}
