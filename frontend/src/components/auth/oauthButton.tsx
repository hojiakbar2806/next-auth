import { BASE_URL } from "@/lib/const";
import Image from "next/image";
import { redirect } from "next/navigation";
import React, { FC } from "react";

type OauthButtonProps = {
  label: string;
  iconPath: string;
  oauth: string;
};

const OauthButton: FC<OauthButtonProps> = ({ label, iconPath, oauth }) => {
  return (
    <button
      type="button"
      onClick={() => redirect(`${BASE_URL}/auth/login/${oauth}`)}
      className="flex-1 flex items-center gap-5 bg-gray-100 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-200 transition"
    >
      <Image src={iconPath} alt={label} width={30} height={30} />
      {label}
    </button>
  );
};

export default OauthButton;
