import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "每日電影新聞 | Daily Movie News",
  description: "自動化的每日電影新聞部落格 - 來自好萊塢的最新消息",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-TW">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
