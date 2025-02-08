"use client";

import { getSession } from "@/app/actions/auth/session";
import { useAuthStore } from "@/store/authStore";
import { redirect } from "next/navigation";
import React, { FC, useEffect, useRef } from "react";

const WithAuth: FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, accessToken, setSession } = useAuthStore();
  const hasFetched = useRef(false);

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    const newSession = async () => {
      const res = await getSession(null);
      if (res) setSession(res.user, res.accessToken);
      else redirect("/login");
    };

    if (!user && !accessToken) newSession();
  }, []);

  return <>{children}</>;
};

export default WithAuth;
