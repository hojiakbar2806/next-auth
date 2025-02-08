"use client";

import { z } from "zod";
import Link from "next/link";
import toast from "react-hot-toast";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import FormInput from "@/components/auth/formInput";
import SubmitButton from "@/components/auth/submitButton";
import { registerAction } from "@/app/actions/auth/register";

const schema = z.object({
  username: z.string().min(4, "Username must be at least 4 characters long"),
  email: z.string().email("Invalid email address"),
  phone_number: z.string().regex(/^\+998\d{9}/, "Invalid phone number"),
  password: z.string().min(8, "Password must be at least 6 characters long"),
});

export type RegisterFormData = z.infer<typeof schema>;

export default function SignUp() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({ resolver: zodResolver(schema) });

  const router = useRouter();

  const onSubmit = async (data: RegisterFormData) => {
    toast.promise(
      registerAction(data).then((res) => {
        if (res.ok) {
          router.replace("/login");
          toast.success(res.msg);
        } else {
          toast.error(res.msg);
        }
      }),
      {
        loading: "Signing up...",
      }
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-4 bg-white p-6 rounded-lg shadow-lg w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Sign Up</h2>

        <FormInput
          label="Username"
          register={register("username")}
          error={errors.username?.message}
          placeholder="Username"
        />

        <FormInput
          label="Email"
          register={register("email")}
          error={errors.email?.message}
          placeholder="Email"
        />

        <FormInput
          label="Phone Number"
          register={register("phone_number")}
          error={errors.phone_number?.message}
          placeholder="Phone Number"
        />

        <FormInput
          label="Password"
          register={register("password")}
          error={errors.password?.message}
          placeholder="Password"
          type="password"
        />
        <SubmitButton isLoading={isSubmitting} label="Sign Up" />

        <p className="flex gap-2">
          Already have an account?
          <Link className="text-blue-500" href="/login">
            Sign In
          </Link>
        </p>
      </form>
    </div>
  );
}
