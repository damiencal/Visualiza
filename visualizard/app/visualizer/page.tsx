'use client';

import { Suspense, useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import VisualizerCanvas from '@/components/visualizer/VisualizerCanvas';
import VisualizerSidebar from '@/components/visualizer/VisualizerSidebar';
import { Product } from '@/types';
import { Upload, Image as ImageIcon, Key } from 'lucide-react';

declare global {
  interface Window {
    aistudio?: {
      hasSelectedApiKey: () => Promise<boolean>;
      openSelectKey: () => Promise<void>;
    };
  }
}

function VisualizerContent() {
  const searchParams = useSearchParams();
  const initialImage = searchParams.get('image');
  
  const [roomImage, setRoomImage] = useState<string | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [hasKey, setHasKey] = useState<boolean | null>(null);

  useEffect(() => {
    const checkKey = async () => {
      if (window.aistudio && window.aistudio.hasSelectedApiKey) {
        try {
          const has = await window.aistudio.hasSelectedApiKey();
          setHasKey(has);
        } catch (e) {
          setHasKey(false);
        }
      } else {
        setHasKey(true); // Fallback if not in AI Studio
      }
    };
    checkKey();
  }, []);

  const handleSelectKey = async () => {
    if (window.aistudio && window.aistudio.openSelectKey) {
      try {
        await window.aistudio.openSelectKey();
        setHasKey(true); // Assume success to mitigate race condition
      } catch (e) {
        console.error(e);
      }
    }
  };

  useEffect(() => {
    if (initialImage) {
      setTimeout(() => {
        setRoomImage(decodeURIComponent(initialImage));
      }, 0);
    }
  }, [initialImage]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setRoomImage(event.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  if (hasKey === null) {
    return <div className="p-20 text-center text-text-secondary">Verificando credenciales...</div>;
  }

  if (!hasKey) {
    return (
      <div className="max-w-md mx-auto mt-20 p-8 glass-card text-center">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner-soft">
          <Key className="w-8 h-8 text-primary" />
        </div>
        <h2 className="text-2xl font-bold mb-4">Se requiere API Key</h2>
        <p className="text-text-secondary mb-6">
          Para utilizar el modelo de generación de imágenes de alta calidad (Gemini 3.1 Flash Image), necesitas seleccionar una API Key de un proyecto de Google Cloud con facturación habilitada.
          <br/><br/>
          <a href="https://ai.google.dev/gemini-api/docs/billing" target="_blank" rel="noreferrer" className="text-primary hover:underline font-medium">Ver documentación de facturación</a>
        </p>
        <button onClick={handleSelectKey} className="btn-primary w-full">
          Seleccionar API Key
        </button>
      </div>
    );
  }

  if (!roomImage) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 min-h-[80vh] flex flex-col items-center justify-center">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-text-primary mb-4">Visualizador Interactivo</h1>
          <p className="text-lg text-text-secondary">Sube una foto de tu espacio para comenzar a visualizar productos.</p>
        </div>

        <div className="w-full max-w-2xl glass-card p-12 border-2 border-dashed border-primary/30 text-center relative group hover:border-primary/60 transition-colors">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileUpload}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
          />
          <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-inner-soft">
            <Upload className="w-10 h-10 text-primary" />
          </div>
          <h3 className="text-2xl font-bold text-text-primary mb-2">Arrastra una foto o toca para seleccionar</h3>
          <p className="text-text-secondary">Formatos soportados: JPG, PNG, WebP. Máx 10MB.</p>
        </div>

        <div className="mt-12 text-center">
          <p className="text-text-secondary mb-4">¿No tienes una foto a mano?</p>
          <button 
            onClick={() => setRoomImage('https://placehold.co/1200x800/e2e8f0/64748b?text=Habitacion+de+Muestra')}
            className="btn-soft flex items-center gap-2 mx-auto"
          >
            <ImageIcon className="w-5 h-5" />
            Usar habitación de muestra
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row h-[calc(100vh-4rem)] overflow-hidden bg-background">
      {/* Main Canvas Area */}
      <div className="flex-1 relative p-4 md:p-6 h-[60vh] md:h-full">
        <VisualizerCanvas 
          imageUrl={roomImage} 
          selectedProduct={selectedProduct} 
        />
      </div>

      {/* Sidebar */}
      <div className="w-full md:w-[400px] h-[40vh] md:h-full flex-shrink-0 z-20">
        <VisualizerSidebar 
          onSelectProduct={setSelectedProduct} 
          selectedProductId={selectedProduct?.id}
        />
      </div>
    </div>
  );
}

export default function VisualizerPage() {
  return (
    <Suspense fallback={<div className="p-20 text-center">Cargando visualizador...</div>}>
      <VisualizerContent />
    </Suspense>
  );
}
