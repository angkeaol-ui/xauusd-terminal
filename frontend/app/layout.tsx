import "./globals.css";

export const metadata = {
  title: "XAUUSD Terminal",
  description: "Real-time XAUUSD AI market dashboard"
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
