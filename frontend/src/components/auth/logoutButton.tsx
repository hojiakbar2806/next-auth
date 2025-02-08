"use client";

import { FC, ReactNode } from "react";
import toast from "react-hot-toast";
import { useRouter } from "next/navigation";
import { logoutAction } from "@/app/actions/auth/logout";
import { useAuthStore } from "@/store/authStore";

type Props = {
  children: ReactNode;
  className?: string;
  redirect?: string;
};

const LogoutButton: FC<Props> = ({ children, className, redirect }) => {
  const router = useRouter();
  const { logout } = useAuthStore();

  const logoutHandler = async () => {
    toast.promise(
      logoutAction().then((res) => {
        if (res) toast.success("Logout successful!");
        else toast.error("Logout failed!");
        logout();
        router.push(redirect || "/login");
      }),
      {
        loading: "Logging out...",
      }
    );
  };

  return (
    <button className={className} onClick={logoutHandler}>
      {children}
    </button>
  );
};

export default LogoutButton;
