import { IAuthUser } from "@/types/auth";
import { create } from "zustand";

interface AuthStore {
  user: IAuthUser | null;
  accessToken: string | null;
  setAccessToken: (token: string) => void;
  setUser: (user: IAuthUser) => void;
  setSession: (user: IAuthUser, accessToken: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  accessToken: null,
  setAccessToken: (token: string) => set({ accessToken: token }),
  setUser: (user: IAuthUser) => set({ user }),
  setSession: (user: IAuthUser, accessToken: string) => {
    set({ user, accessToken });
  },
  logout: () => set({ user: null, accessToken: null }),
}));
