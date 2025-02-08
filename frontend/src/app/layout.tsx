import TanstackQueryProvider from "@/components/providers/tanstackQueryProvider";
import "./globals.css";
import { Toaster } from "react-hot-toast";

interface Props {
  readonly children: React.ReactNode;
}

export default function RootLayout({ children }: Props) {
  return (
    <html lang="en">
      <body>
        <TanstackQueryProvider>
          {children}
          <Toaster position="top-center" reverseOrder={false} />
        </TanstackQueryProvider>
      </body>
    </html>
  );
}
