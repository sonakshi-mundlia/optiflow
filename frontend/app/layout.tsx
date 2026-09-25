import type { Metadata } from "next";

import "./globals.css";


export const metadata: Metadata = {

  title: "OptiFlow",

  description:
    "Intelligent AI query routing with semantic caching and cost-aware inference.",

};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="en">

      <body>
        {children}
      </body>

    </html>
  );
}