import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const protectedRoutes = [, "/profile"];
const authRoutes = ["/login", "/register"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("refresh_token");

  if (protectedRoutes.includes(pathname) && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (authRoutes.includes(pathname) && token) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/profile", "/login", "/register"],
};
