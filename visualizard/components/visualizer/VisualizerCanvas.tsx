'use client';

import { useState, useRef, useEffect } from 'react';
import { Product } from '@/types';
import { Undo2, Redo2, RotateCcw, Download, Share2, Sparkles, PenTool, Eraser } from 'lucide-react';

interface Point {
  x: number;
  y: number;
}

interface VisualizerCanvasProps {
  imageUrl: string;
  selectedProduct: Product | null;
}

export default function VisualizerCanvas({ imageUrl, selectedProduct }: VisualizerCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  
  const [isDrawingMode, setIsDrawingMode] = useState(false);
  const [isDrawing, setIsDrawing] = useState(false);
  const [maskPath, setMaskPath] = useState<Point[]>([]);
  const [baseImageObj, setBaseImageObj] = useState<HTMLImageElement | null>(null);

  // Load initial image
  useEffect(() => {
    const loadInitialImage = async () => {
      setIsProcessing(true);
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.src = imageUrl;
      
      await new Promise((resolve) => { img.onload = resolve; });
      setBaseImageObj(img);

      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);

      // Save initial state
      const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
      setHistory([dataUrl]);
      setHistoryIndex(0);
      setIsProcessing(false);
    };

    loadInitialImage();
  }, [imageUrl]);

  const renderCanvas = async (currentMask: Point[] = maskPath, product: Product | null = selectedProduct, showOutline: boolean = isDrawingMode) => {
    const canvas = canvasRef.current;
    if (!canvas || !baseImageObj) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Draw base image
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(baseImageObj, 0, 0, canvas.width, canvas.height);

    // Draw product texture if product and mask exist
    if (product && currentMask.length > 2) {
      const textureImg = new Image();
      textureImg.crossOrigin = 'anonymous';
      textureImg.src = product.images.texture;
      await new Promise((resolve) => { textureImg.onload = resolve; });

      const pattern = ctx.createPattern(textureImg, 'repeat');
      if (pattern) {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(currentMask[0].x, currentMask[0].y);
        for (let i = 1; i < currentMask.length; i++) {
          ctx.lineTo(currentMask[i].x, currentMask[i].y);
        }
        ctx.closePath();
        ctx.clip();

        ctx.fillStyle = pattern;
        ctx.globalCompositeOperation = product.category === 'furniture' ? 'source-over' : 'multiply';
        ctx.globalAlpha = product.category === 'furniture' ? 1.0 : 0.8;
        ctx.fill();
        ctx.restore();
      }
    }

    // Draw mask outline if in drawing mode
    if (showOutline && currentMask.length > 0) {
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(currentMask[0].x, currentMask[0].y);
      for (let i = 1; i < currentMask.length; i++) {
        ctx.lineTo(currentMask[i].x, currentMask[i].y);
      }
      if (!isDrawing && currentMask.length > 2) ctx.closePath();
      
      ctx.strokeStyle = '#F43F5E';
      ctx.lineWidth = 3;
      ctx.setLineDash([5, 5]);
      ctx.stroke();
      
      if (!isDrawing && currentMask.length > 2) {
        ctx.fillStyle = 'rgba(244, 63, 94, 0.2)';
        ctx.fill();
      }
      ctx.restore();
    }
  };

  const handleAIEnhance = async (product: Product) => {
    if (!canvasRef.current) return;
    setIsProcessing(true);
    try {
      // Force render WITHOUT drawing mode outline
      await renderCanvas(maskPath, product, false);
      
      const base64ImageData = canvasRef.current.toDataURL('image/jpeg', 0.8).split(',')[1];
      
      const { GoogleGenAI } = await import('@google/genai');
      const ai = new GoogleGenAI({ apiKey: process.env.NEXT_PUBLIC_GEMINI_API_KEY });
      
      let prompt = '';
      if (product.category === 'furniture') {
        prompt = `This is a room interior. I have marked an area by pasting a solid pattern over it. Please completely replace whatever is in that marked area with a photorealistic ${product.name}. Do NOT keep the shape, structure, or color of the original object underneath. The new ${product.name} must fit naturally into the space, with correct scale, perspective, lighting, and shadows. Do not change the rest of the room.`;
      } else {
        prompt = `This is a room interior. I have roughly pasted a new material (${product.name}) onto a specific area. Please refine this image to make the new material look completely photorealistic and naturally blended into the room. Ensure the lighting, shadows, reflections, and perspective of the new material perfectly match the surrounding environment, keeping the underlying shape intact. Do not change the rest of the room.`;
      }
      
      let aspectRatio = "1:1";
      const ratio = canvasRef.current.width / canvasRef.current.height;
      if (ratio > 1.5) aspectRatio = "16:9";
      else if (ratio > 1.1) aspectRatio = "4:3";
      else if (ratio < 0.6) aspectRatio = "9:16";
      else if (ratio < 0.9) aspectRatio = "3:4";
      
      const response = await ai.models.generateContent({
        model: 'gemini-3.1-flash-image-preview',
        contents: {
          parts: [
            {
              inlineData: {
                data: base64ImageData,
                mimeType: 'image/jpeg',
              },
            },
            {
              text: prompt,
            },
          ],
        },
        config: {
          imageConfig: {
            aspectRatio: aspectRatio as any,
          }
        }
      });
      
      let imageFound = false;
      for (const part of response.candidates?.[0]?.content?.parts || []) {
        if (part.inlineData) {
          const imageUrl = `data:${part.inlineData.mimeType};base64,${part.inlineData.data}`;
          
          // Add to history
          const newHistory = history.slice(0, historyIndex + 1);
          newHistory.push(imageUrl);
          setHistory(newHistory);
          setHistoryIndex(newHistory.length - 1);
          restoreCanvas(imageUrl);
          imageFound = true;
          
          // Turn off drawing mode after successful generation
          setIsDrawingMode(false);
          break;
        }
      }
      
      if (!imageFound) {
        console.error("No image in response:", response);
        alert('La IA no devolvió una imagen. Por favor, intenta de nuevo.');
        await renderCanvas(maskPath, product, isDrawingMode);
      }
    } catch (error) {
      console.error('AI Enhancement failed:', error);
      alert('Error al mejorar con IA. Por favor, intenta de nuevo.');
      await renderCanvas(maskPath, product, isDrawingMode);
    } finally {
      setIsProcessing(false);
    }
  };

  // Re-render when product changes
  useEffect(() => {
    const update = async () => {
      await renderCanvas(maskPath, selectedProduct, isDrawingMode);
      if (selectedProduct && maskPath.length > 2 && !isDrawing) {
         handleAIEnhance(selectedProduct);
      }
    };
    update();
  }, [selectedProduct]);

  const handlePointerDown = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingMode) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;
    
    setIsDrawing(true);
    setMaskPath([{ x, y }]);
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingMode || !isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;
    
    const newPath = [...maskPath, { x, y }];
    setMaskPath(newPath);
    renderCanvas(newPath, selectedProduct, isDrawingMode);
  };

  const handlePointerUp = async () => {
    if (!isDrawingMode || !isDrawing) return;
    setIsDrawing(false);
    await renderCanvas(maskPath, selectedProduct, isDrawingMode);
    if (selectedProduct && maskPath.length > 2) {
      handleAIEnhance(selectedProduct);
    }
  };

  const handleUndo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(prev => prev - 1);
      restoreCanvas(history[historyIndex - 1]);
    }
  };

  const handleRedo = () => {
    if (historyIndex < history.length - 1) {
      setHistoryIndex(prev => prev + 1);
      restoreCanvas(history[historyIndex + 1]);
    }
  };

  const handleReset = () => {
    if (history.length > 0) {
      setHistoryIndex(0);
      setMaskPath([]);
      restoreCanvas(history[0]);
    }
  };

  const restoreCanvas = (dataUrl: string) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.src = dataUrl;
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      setBaseImageObj(img);
    };
  };

  const handleDownload = () => {
    if (!canvasRef.current) return;
    const link = document.createElement('a');
    link.download = 'visualiza-rd-espacio.png';
    link.href = canvasRef.current.toDataURL('image/png');
    link.click();
  };

  const toggleDrawingMode = () => {
    setIsDrawingMode(!isDrawingMode);
    if (isDrawingMode) {
      // Exiting drawing mode, re-render to hide the dashed line
      renderCanvas(maskPath, selectedProduct, false);
    } else {
      renderCanvas(maskPath, selectedProduct, true);
    }
  };

  const clearMask = () => {
    setMaskPath([]);
    renderCanvas([], selectedProduct, isDrawingMode);
  };

  return (
    <div className="relative w-full h-full flex flex-col items-center justify-center bg-black/5 rounded-2xl overflow-hidden shadow-inner-soft">
      {isProcessing && (
        <div className="absolute inset-0 z-20 bg-white/50 backdrop-blur-md flex items-center justify-center transition-all duration-300">
          <div className="flex flex-col items-center gap-4 bg-white/80 p-6 rounded-2xl shadow-elevated">
            <Sparkles className="w-10 h-10 text-primary animate-pulse" />
            <span className="text-primary font-bold text-lg">Generando con IA...</span>
            <p className="text-sm text-text-secondary">Adaptando iluminación y perspectiva</p>
          </div>
        </div>
      )}

      <div className="relative w-full h-full max-h-[70vh] flex items-center justify-center p-4">
        <canvas
          ref={canvasRef}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerLeave={handlePointerUp}
          className={`max-w-full max-h-full object-contain rounded-xl shadow-card transition-all duration-300 ${
            isDrawingMode ? 'cursor-crosshair' : 'cursor-default'
          } touch-none ${isProcessing ? 'blur-md scale-[1.02]' : ''}`}
        />
      </div>

      {/* Bottom Toolbar */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 glass-panel px-6 py-3 rounded-full flex items-center gap-4 shadow-elevated z-10">
        <button
          onClick={toggleDrawingMode}
          className={`p-2 transition-colors ${
            isDrawingMode ? 'text-primary bg-primary/10 rounded-full' : 'text-text-secondary hover:text-primary'
          }`}
          title={isDrawingMode ? 'Dibujando Área' : 'Seleccionar Área'}
        >
          <PenTool className="w-5 h-5" />
        </button>
        {maskPath.length > 0 && (
          <button
            onClick={clearMask}
            className="p-2 text-text-secondary hover:text-primary transition-colors"
            title="Borrar Área"
          >
            <Eraser className="w-5 h-5" />
          </button>
        )}
        <div className="w-px h-6 bg-black/10 mx-2"></div>
        <button 
          onClick={handleUndo} 
          disabled={historyIndex <= 0 || isProcessing}
          className="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors"
          title="Deshacer"
        >
          <Undo2 className="w-5 h-5" />
        </button>
        <button 
          onClick={handleRedo}
          disabled={historyIndex >= history.length - 1 || isProcessing}
          className="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors"
          title="Rehacer"
        >
          <Redo2 className="w-5 h-5" />
        </button>
        <div className="w-px h-6 bg-black/10 mx-2"></div>
        <button 
          onClick={handleReset}
          disabled={(historyIndex === 0 && maskPath.length === 0) || isProcessing}
          className="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors"
          title="Reiniciar"
        >
          <RotateCcw className="w-5 h-5" />
        </button>
        <div className="w-px h-6 bg-black/10 mx-2"></div>
        <button 
          onClick={handleDownload}
          disabled={isProcessing}
          className="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors"
          title="Descargar"
        >
          <Download className="w-5 h-5" />
        </button>
        <button 
          disabled={isProcessing}
          className="p-2 text-text-secondary hover:text-primary disabled:opacity-30 transition-colors"
          title="Compartir"
        >
          <Share2 className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
