"use client";

import { useEffect, useTransition } from "react";
import { redirect } from "next/navigation";
import { setOauthToken } from "@/app/actions/setOauthToken";
import toast from "react-hot-toast";
import { Loader2Icon } from "lucide-react";

export default function HolderPage() {
  const [isProcessing, startProcess] = useTransition();

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const code = searchParams.get("code");
    if (!code) redirect("/");
    const processSession = async () => {
      const res = await setOauthToken(code);
      if (res) toast.success("Login successful!");
      else toast.error("Something went wrong");
      redirect("/");
    };
    startProcess(processSession);
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      {isProcessing && <Loader2Icon className="size-20 animate-spin" />}
    </div>
  );
}
