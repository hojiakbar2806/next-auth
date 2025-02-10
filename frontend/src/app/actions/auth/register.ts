"use server";

import axios from "@/lib/axios";
import { RegisterFormData } from "../../(auth)/register/page";

export async function registerAction(data: RegisterFormData) {
  try {
    const res = await axios.post("/auth/register", data);
    return { ok: true, msg: res.data.message };
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      return { ok: false, msg: error.response?.data.detail };
    }
    return { ok: false, msg: "Something went wrong" };
  }
}
