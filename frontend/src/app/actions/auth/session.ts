"use server";

import { IAuthUser } from "@/types/auth";
import axios from "@/utils/axios";
import { cookies } from "next/headers";

export async function getSession(accessToken: string | null): Promise<{
  user: IAuthUser;
  accessToken: string;
} | null> {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get("refresh_token")?.value;
  try {
    if (!refreshToken) return null;
    if (accessToken) {
      const session = await axios.get("/auth/session", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      return { user: session.data, accessToken };
    }
    const res = await axios.post("/auth/refresh-token", null, {
      headers: { Cookie: cookieStore.toString() },
    });
    const session = await axios.get("/auth/session", {
      headers: { Authorization: `Bearer ${res.data.access_token}` },
    });
    return { user: session.data, accessToken: res.data.access_token };
  } catch (error) {
    console.log(error);
    return null;
  }
}
