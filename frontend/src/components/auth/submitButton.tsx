import React, { FC } from "react";

interface SubmitButtonProps {
  isLoading: boolean;
  label?: string;
}

const SubmitButton: FC<SubmitButtonProps> = ({ isLoading, label }) => {
  return (
    <button
      type="submit"
      data-loading={isLoading}
      disabled={isLoading}
      className="flex-1 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition
      data-[loading=true]:opacity-50 
      data-[loading=true]:cursor-not-allowed"
    >
      {isLoading ? "Loading..." : label}
    </button>
  );
};

export default SubmitButton;
