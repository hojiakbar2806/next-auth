import WithAuth from "@/components/auth/withAuth";
import React from "react";

type Props = {
  children: React.ReactNode;
};

export default function ProfileLayout({ children }: Props) {
  return <WithAuth>{children}</WithAuth>;
}
