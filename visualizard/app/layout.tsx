import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { FavoritesProvider } from '@/contexts/FavoritesContext';
import AppHeader from '@/components/layout/AppHeader';
import MobileNav from '@/components/layout/MobileNav';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

export const metadata: Metadata = {
  title: 'VisualizaRD — Visualizador Inmobiliario Interactivo',
  description: 'Visualiza tu hogar ideal con productos reales de suplidores dominicanos.',
  themeColor: '#F9FAFB',
  appleWebApp: {
    capable: true,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${inter.variable}`}>
      <body className="font-sans bg-background text-text-primary antialiased min-h-screen pb-16 md:pb-0" suppressHydrationWarning>
        <FavoritesProvider>
          <AppHeader />
          <main className="pt-16 min-h-screen">
            {children}
          </main>
          <MobileNav />
        </FavoritesProvider>
      </body>
    </html>
  );
}
