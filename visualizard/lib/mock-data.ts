import { Property, Product } from '@/types';

export const mockProperties: Property[] = [
  {
    id: 'p1',
    title: 'Moderno Apartamento en Piantini',
    slug: 'moderno-apartamento-piantini',
    description: 'Espectacular apartamento a estrenar en el corazón de Piantini. Cuenta con terminaciones de primera, pisos de mármol, cocina modular italiana y balcón tipo terraza.',
    price: 15000000,
    priceUSD: 255000,
    currency: 'DOP',
    location: {
      address: 'Calle Federico Geraldino',
      city: 'Santo Domingo',
      province: 'Distrito Nacional',
      neighborhood: 'Piantini',
      coordinates: { lat: 18.4725, lng: -69.9389 }
    },
    specs: {
      bedrooms: 2,
      bathrooms: 2.5,
      area: 145,
      parking: 2,
      yearBuilt: 2024
    },
    images: [
      {
        id: 'img1',
        url: 'https://picsum.photos/seed/living1/1200/800',
        alt: 'Sala de estar moderna',
        room: 'living-room',
        isVisualizerReady: true,
        width: 1200,
        height: 800
      },
      {
        id: 'img2',
        url: 'https://picsum.photos/seed/bed1/1200/800',
        alt: 'Habitación principal',
        room: 'bedroom',
        isVisualizerReady: false,
        width: 1200,
        height: 800
      }
    ],
    features: ['Balcón', 'Gimnasio', 'Piscina', 'Seguridad 24/7', 'Planta Full'],
    type: 'apartment',
    status: 'available',
    agent: {
      name: 'Carlos Mendoza',
      phone: '+1 809-555-0123',
      avatar: 'https://picsum.photos/seed/agent1/150/150'
    },
    createdAt: '2024-03-01T10:00:00Z',
    isFeatured: true
  },
  {
    id: 'p2',
    title: 'Villa de Lujo en Cap Cana',
    slug: 'villa-lujo-cap-cana',
    description: 'Impresionante villa con vistas al campo de golf. Diseño contemporáneo, amplios espacios abiertos y piscina infinity.',
    price: 85000000,
    priceUSD: 1450000,
    currency: 'DOP',
    location: {
      address: 'Punta Espada',
      city: 'Punta Cana',
      province: 'La Altagracia',
      neighborhood: 'Cap Cana',
      coordinates: { lat: 18.4725, lng: -68.4189 }
    },
    specs: {
      bedrooms: 5,
      bathrooms: 6,
      area: 850,
      parking: 4,
      yearBuilt: 2022
    },
    images: [
      {
        id: 'img3',
        url: 'https://picsum.photos/seed/villa1/1200/800',
        alt: 'Exterior de la villa',
        room: 'exterior',
        isVisualizerReady: false,
        width: 1200,
        height: 800
      },
      {
        id: 'img4',
        url: 'https://picsum.photos/seed/villaliving/1200/800',
        alt: 'Sala con vista al golf',
        room: 'living-room',
        isVisualizerReady: true,
        width: 1200,
        height: 800
      }
    ],
    features: ['Piscina Infinity', 'Vista al Golf', 'Cine en casa', 'Domótica', 'Acceso a playa'],
    type: 'villa',
    status: 'available',
    agent: {
      name: 'Laura Castillo',
      phone: '+1 809-555-0456',
      avatar: 'https://picsum.photos/seed/agent2/150/150'
    },
    createdAt: '2024-02-15T10:00:00Z',
    isFeatured: true
  },
  {
    id: 'p3',
    title: 'Acogedor Estudio en Naco',
    slug: 'estudio-naco',
    description: 'Ideal para inversión o solteros. Excelente ubicación, cerca de centros comerciales y restaurantes.',
    price: 4500000,
    priceUSD: 76000,
    currency: 'DOP',
    location: {
      address: 'Calle Tiradentes',
      city: 'Santo Domingo',
      province: 'Distrito Nacional',
      neighborhood: 'Naco',
      coordinates: { lat: 18.4785, lng: -69.9289 }
    },
    specs: {
      bedrooms: 1,
      bathrooms: 1,
      area: 65,
      parking: 1,
      yearBuilt: 2018
    },
    images: [
      {
        id: 'img5',
        url: 'https://picsum.photos/seed/studio1/1200/800',
        alt: 'Espacio integrado',
        room: 'living-room',
        isVisualizerReady: true,
        width: 1200,
        height: 800
      }
    ],
    features: ['Amueblado', 'Lobby climatizado', 'Ascensor'],
    type: 'studio',
    status: 'available',
    agent: {
      name: 'Carlos Mendoza',
      phone: '+1 809-555-0123',
      avatar: 'https://picsum.photos/seed/agent1/150/150'
    },
    createdAt: '2024-03-10T10:00:00Z',
    isFeatured: false
  },
  {
    id: 'p4',
    title: 'Casa Familiar en Cerros de Gurabo',
    slug: 'casa-cerros-gurabo',
    description: 'Hermosa casa de dos niveles con amplio patio, ideal para familias. Ubicada en una de las zonas más exclusivas de Santiago.',
    price: 22000000,
    priceUSD: 375000,
    currency: 'DOP',
    location: {
      address: 'Calle Principal',
      city: 'Santiago de los Caballeros',
      province: 'Santiago',
      neighborhood: 'Cerros de Gurabo',
      coordinates: { lat: 19.45, lng: -70.68 }
    },
    specs: {
      bedrooms: 4,
      bathrooms: 3.5,
      area: 320,
      parking: 4,
      yearBuilt: 2015
    },
    images: [
      {
        id: 'img6',
        url: 'https://picsum.photos/seed/house1/1200/800',
        alt: 'Fachada',
        room: 'exterior',
        isVisualizerReady: false,
        width: 1200,
        height: 800
      },
      {
        id: 'img7',
        url: 'https://picsum.photos/seed/housekitchen/1200/800',
        alt: 'Cocina',
        room: 'kitchen',
        isVisualizerReady: true,
        width: 1200,
        height: 800
      }
    ],
    features: ['Patio', 'Terraza', 'Cuarto de servicio', 'Madera preciosa'],
    type: 'house',
    status: 'available',
    agent: {
      name: 'Miguel Torres',
      phone: '+1 809-555-0789',
      avatar: 'https://picsum.photos/seed/agent3/150/150'
    },
    createdAt: '2024-01-20T10:00:00Z',
    isFeatured: false
  }
];

export const mockProducts: Product[] = [
  {
    id: 'prod1',
    name: 'Porcelanato Maderado Roble',
    nameEs: 'Porcelanato Maderado Roble',
    slug: 'porcelanato-maderado-roble',
    brand: {
      id: 'b1',
      name: 'Ochoa',
      slug: 'ochoa',
      logo: 'https://picsum.photos/seed/ochoa/100/50',
      country: 'Dominican Republic',
      description: 'Ferretería y materiales de construcción'
    },
    category: 'flooring',
    subcategory: 'porcelain',
    description: 'Porcelanato formato tablón imitación madera roble natural.',
    descriptionEs: 'Porcelanato formato tablón imitación madera roble natural.',
    price: 1250,
    currency: 'DOP',
    unit: 'm²',
    sku: 'OCH-POR-001',
    images: {
      thumbnail: 'https://placehold.co/200x200/8B5A2B/FFFFFF?text=Roble',
      full: 'https://placehold.co/800x800/8B5A2B/FFFFFF?text=Roble',
      texture: 'https://placehold.co/512x512/8B5A2B/FFFFFF?text=Texture',
      textureScale: 1.5
    },
    specs: {
      'Formato': '20x120 cm',
      'Acabado': 'Mate',
      'Tráfico': 'Alto'
    },
    colors: ['#8B5A2B'],
    inStock: true,
    rating: 4.8,
    reviewCount: 124,
    tags: ['madera', 'porcelanato', 'piso'],
    visualizerCompatible: true,
    surfaceTypes: ['floor', 'wall']
  },
  {
    id: 'prod2',
    name: 'Pintura Acrílica Blanco Hueso',
    nameEs: 'Pintura Acrílica Blanco Hueso',
    slug: 'pintura-blanco-hueso',
    brand: {
      id: 'b2',
      name: 'Pinturas Popular',
      slug: 'pinturas-popular',
      logo: 'https://picsum.photos/seed/popular/100/50',
      country: 'Dominican Republic',
      description: 'Pinturas de alta calidad'
    },
    category: 'paint',
    subcategory: 'interior',
    description: 'Pintura acrílica premium para interiores, acabado mate.',
    descriptionEs: 'Pintura acrílica premium para interiores, acabado mate.',
    price: 1800,
    currency: 'DOP',
    unit: 'galón',
    sku: 'POP-INT-001',
    images: {
      thumbnail: 'https://placehold.co/200x200/FDF5E6/000000?text=Blanco+Hueso',
      full: 'https://placehold.co/800x800/FDF5E6/000000?text=Blanco+Hueso',
      texture: 'https://placehold.co/512x512/FDF5E6/FDF5E6',
      textureScale: 1.0
    },
    specs: {
      'Rendimiento': '40 m²/galón',
      'Acabado': 'Mate',
      'Lavable': 'Sí'
    },
    colors: ['#FDF5E6'],
    inStock: true,
    rating: 4.5,
    reviewCount: 89,
    tags: ['pintura', 'interior', 'blanco'],
    visualizerCompatible: true,
    surfaceTypes: ['wall', 'ceiling']
  },
  {
    id: 'prod3',
    name: 'Sofá KIVIK 3 Plazas',
    nameEs: 'Sofá KIVIK 3 Plazas',
    slug: 'sofa-kivik-3-plazas',
    brand: {
      id: 'b3',
      name: 'IKEA',
      slug: 'ikea',
      logo: 'https://picsum.photos/seed/ikea/100/50',
      country: 'Sweden',
      description: 'Muebles y decoración'
    },
    category: 'furniture',
    subcategory: 'sofas',
    description: 'Sofá amplio y cómodo con asientos profundos.',
    descriptionEs: 'Sofá amplio y cómodo con asientos profundos.',
    price: 35000,
    currency: 'DOP',
    unit: 'unit',
    sku: 'IKE-SOF-001',
    images: {
      thumbnail: 'https://placehold.co/200x200/708090/FFFFFF?text=KIVIK',
      full: 'https://placehold.co/800x800/708090/FFFFFF?text=KIVIK',
      texture: 'https://placehold.co/512x512/708090/FFFFFF?text=Texture',
      textureScale: 1.0
    },
    specs: {
      'Ancho': '228 cm',
      'Fondo': '95 cm',
      'Altura': '83 cm'
    },
    colors: ['#708090', '#F5F5DC'],
    inStock: true,
    rating: 4.7,
    reviewCount: 210,
    tags: ['sofa', 'sala', 'mueble'],
    visualizerCompatible: false,
    surfaceTypes: []
  }
];
