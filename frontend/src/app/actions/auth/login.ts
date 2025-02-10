"use server";

import axios from "@/lib/axios";
import { cookies } from "next/headers";
import { LoginFormData } from "@/app/(auth)/login/page";

export async function loginAction(data: LoginFormData) {
  try {
    const res = await axios.post("/auth/login", data);
    const { access_token, refresh_token } = res.data;
    const cookieStore = await cookies();
    cookieStore.set("refresh_token", refresh_token, {
      httpOnly: true,
      sameSite: "lax",
      secure: true,
    });
    return { ok: true, token: access_token, msg: res.data.message };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return { ok: false, msg: error.response?.data.detail };
    }
    return { ok: false, msg: "Something went wrong" };
  }
}
