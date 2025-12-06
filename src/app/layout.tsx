import type { Metadata } from "next";
import { Roboto_Serif } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";
import Header from "@/components/Header";

const robotoSerif = Roboto_Serif({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  variable: "--font-roboto-serif",
});

export const metadata: Metadata = {
  title: "Patrick Huie - Software Engineer",
  description: "Building software for people - open, accessible, reliable, and seamlessly integrated.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body
        className={`${robotoSerif.variable} antialiased bg-black text-gray-100 min-h-screen font-serif`}
      >
        <Header />
        <main>
          {children}
        </main>
        <Analytics />
      </body>
    </html>
  );
}
