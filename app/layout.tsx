import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'GitAgent - Code Generation That Ships',
  description: 'Multi-agent code generation system powered by Gemini and GitAgent',
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