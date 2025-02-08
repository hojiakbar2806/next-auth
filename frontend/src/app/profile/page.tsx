"use client";

import { useAuthStore } from "@/store/authStore";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import Link from "next/link";
import { Copy } from "lucide-react";
import toast from "react-hot-toast";

export default function ProfilePage() {
  const { accessToken, user } = useAuthStore();

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100 p-6">
      <Card className="w-full max-w-md bg-white shadow-lg rounded-lg p-6">
        <CardHeader className="flex flex-col items-center">
          {user == null ? (
            <Skeleton className="w-24 h-24 rounded-full" />
          ) : (
            <Avatar className="w-24 h-24 flex">
              <AvatarImage />
              <AvatarFallback className="text-2xl uppercase">
                {user?.username?.charAt(0)}
              </AvatarFallback>
            </Avatar>
          )}
          <CardTitle className="w-full text-center mt-4 text-lg font-semibold">
            {user == null ? (
              <Skeleton className="h-8" />
            ) : (
              user?.username || "Unknown User"
            )}
          </CardTitle>
        </CardHeader>

        <CardContent className="text-center">
          <div className="text-gray-500 text-sm">
            {user == null ? (
              <Skeleton className=" h-4" />
            ) : (
              <p>{user?.email || "No Email"}</p>
            )}
          </div>

          <div className="mt-6 space-y-4">
            <Button asChild variant="outline">
              <Link href="/">Back to Home</Link>
            </Button>
          </div>

          <div className="mt-6 text-sm text-gray-500">
            <div className="w-full flex items-center p-2 gap-4 rounded-sm bg-gray-200">
              <pre className="w-full text-xs rounded-md line-clamp-1">
                {!accessToken ? <Skeleton className="h-4" /> : accessToken}
              </pre>
              <Copy
                className="ml-2 cursor-pointer"
                onClick={async () =>
                  toast.promise(
                    navigator.clipboard.writeText(accessToken || ""),
                    {
                      loading: "Copying...",
                      success: "Copied to clipboard!",
                      error: "Failed to copy",
                    }
                  )
                }
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
