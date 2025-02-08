import Link from "next/link";
import LogoutButton from "../components/auth/logoutButton";
import { cookies } from "next/headers";

export default async function Home() {
  const cookiStore = await cookies();
  return (
    <div className="w-full">
      <header className="w-full flex justify-between p-10">
        <Link href="/profile">Profile</Link>
        {!cookiStore.has("refresh_token") ? (
          <div className="flex gap-2">
            <Link href="/login">Login</Link>
            <Link href="/register">Register</Link>
          </div>
        ) : (
          <LogoutButton redirect="/">Logout</LogoutButton>
        )}
      </header>
    </div>
  );
}
