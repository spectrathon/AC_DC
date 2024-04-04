import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import ClientProvider from "@/components/clientProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Axon | The Learning App",
  description: "An app that can help you learn anything",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClientProvider>
      <html lang="en">
        <body className={`dark bg-neutral-900 text-white  ${inter.className}`}>


          {children}

        </body>
      </html>
    </ClientProvider>
  );
}
