export const NODE_ENV = process.env.NODE_ENV;

export const BASE_URL =
  NODE_ENV === "production"
    ? "https://next-auth.hojiakbar.me/api"
    : "http://127.0.0.1:8000/api";
