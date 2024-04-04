// import "../../../globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sign In | Axon",
  description: "",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <section className="dark">{children}</section>;
}
