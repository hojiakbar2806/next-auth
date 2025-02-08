"use client";

import { z } from "zod";
import Link from "next/link";
import toast from "react-hot-toast";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import FormInput from "@/components/auth/formInput";
import OauthButton from "@/components/auth/oauthButton";
import SubmitButton from "@/components/auth/submitButton";
import { loginAction } from "@/app/actions/auth/login";

const schema = z.object({
  username: z.string().min(4, "Username must be at least 4 characters long"),
  password: z.string().min(8, "Password must be at least 6 characters long"),
});

export type LoginFormData = z.infer<typeof schema>;

export default function SignIn() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({ resolver: zodResolver(schema) });

  const router = useRouter();

  const onSubmit = async (data: LoginFormData) => {
    toast.promise(
      loginAction(data).then((res) => {
        if (res.ok) {
          router.replace("/");
          toast.success(res.msg);
        } else toast.error(res.msg);
      }),
      {
        loading: "Signing in...",
      }
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-4 bg-white p-6 rounded-lg shadow-lg w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Sign In</h2>

        <FormInput
          label="Username"
          register={register("username")}
          error={errors.username?.message}
          placeholder="Username"
        />

        <FormInput
          label="Password"
          register={register("password")}
          error={errors.password?.message}
          placeholder="Password"
          type="password"
        />
        <SubmitButton isLoading={isSubmitting} label="Sign In" />
        <p className="flex gap-2">
          Don&apos;t have an account?
          <Link className="text-blue-500" href="/register">
            Sign Up
          </Link>
        </p>
        <div className="w-full flex gap-4 pt-5 border-t ">
          <OauthButton
            label="Google"
            iconPath="/icons/google.svg"
            oauth="google"
          />
          <OauthButton
            label="Github"
            iconPath="/icons/github.svg"
            oauth="github"
          />
        </div>
      </form>
    </div>
  );
}
