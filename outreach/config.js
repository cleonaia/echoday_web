// Mass Outreach Automation Configuration for Echoday
// Location: Sabadell, Barcelona, Vallès Occidental, Pare Rodés 13

const OUTREACH_CONFIG = {
  // Web3Forms Configuration
  web3forms: {
    // Replace with your actual Web3Forms API key
    apiKey: 'YOUR_WEB3FORMS_API_KEY_HERE',
    endpoint: 'https://api.web3forms.com/submit',
    // Form will redirect to your main website after submission
    redirectUrl: 'https://www.echoday.tech',
    // Subject line for received emails
    subject: 'Nova consulta des de campanya Echoday'
  },

  // Company Information
  company: {
    name: 'Echoday',
    email: 'contacto@echoday.tech',
    phone: '+34 643 032 807',
    website: 'https://www.echoday.tech',
    whatsapp: 'https://wa.me/34643032807',
    address: {
      street: 'Pare Rodés 13',
      city: 'Sabadell',
      province: 'Barcelona',
      region: 'Vallès Occidental',
      postalCode: '08208',
      country: 'España'
    }
  },

  // Supported Languages
  languages: ['ca', 'es'],
  defaultLanguage: 'ca', // Catalan as default for local market

  // Location Targeting
  location: {
    primary: 'Sabadell',
    secondary: ['Barcelona', 'Terrassa', 'Rubí', 'Cerdanyola del Vallès', 'Barberà del Vallès'],
    region: 'Vallès Occidental',
    province: 'Barcelona',
    radius_km: 25 // Target businesses within 25km radius
  },

  // Flexible Business Sectors with High Conversion Potential
  sectors: {
    // High-priority sectors for local businesses
    high_priority: [
      {
        name: 'restaurants_bars',
        ca: 'Restaurants i Bars',
        es: 'Restaurantes y Bares',
        keywords: ['restaurant', 'bar', 'cafeteria', 'pizzeria', 'tapas', 'menjar', 'comer'],
        pain_points: ['gestió comandes', 'reservas online', 'carta digital', 'delivery'],
        conversion_rate: 0.18
      },
      {
        name: 'beauty_wellness',
        ca: 'Bellesa i Benestar',
        es: 'Belleza y Bienestar',
        keywords: ['perruqueria', 'peluqueria', 'estètica', 'spa', 'massatge', 'fisio'],
        pain_points: ['sistema de cites', 'gestió clients', 'promocions', 'fidelització'],
        conversion_rate: 0.22
      },
      {
        name: 'retail_shops',
        ca: 'Botigues i Comerç Local',
        es: 'Tiendas y Comercio Local',
        keywords: ['botiga', 'tienda', 'roba', 'moda', 'calçat', 'complements'],
        pain_points: ['venda online', 'inventari', 'presència digital', 'competència'],
        conversion_rate: 0.15
      },
      {
        name: 'medical_health',
        ca: 'Salut i Serveis Mèdics',
        es: 'Salud y Servicios Médicos',
        keywords: ['clínica', 'consulta', 'metge', 'dentista', 'farmàcia', 'òptica'],
        pain_points: ['cites online', 'gestió pacients', 'expedients digitals', 'comunicació'],
        conversion_rate: 0.25
      }
    ],
    
    // Medium-priority sectors
    medium_priority: [
      {
        name: 'professional_services',
        ca: 'Serveis Professionals',
        es: 'Servicios Profesionales',
        keywords: ['advocat', 'assessoria', 'consultoria', 'gestoria', 'comptable'],
        pain_points: ['automatització', 'gestió documents', 'agenda', 'facturació'],
        conversion_rate: 0.12
      },
      {
        name: 'fitness_sports',
        ca: 'Fitness i Esports',
        es: 'Fitness y Deportes',
        keywords: ['gimnàs', 'pilates', 'crossfit', 'pàdel', 'entrenament', 'esport'],
        pain_points: ['reserves classes', 'seguiment clients', 'app mòbil', 'comunitat'],
        conversion_rate: 0.16
      },
      {
        name: 'automotive',
        ca: 'Automòbil i Mecànica',
        es: 'Automóvil y Mecánica',
        keywords: ['taller', 'cotxe', 'mecànic', 'reparació', 'manteniment', 'ITV'],
        pain_points: ['cites online', 'pressupostos', 'seguiment reparacions', 'comunicació client'],
        conversion_rate: 0.14
      },
      {
        name: 'education_training',
        ca: 'Educació i Formació',
        es: 'Educación y Formación',
        keywords: ['academia', 'idiomes', 'reforç', 'música', 'dansa', 'formació'],
        pain_points: ['gestió alumnes', 'classes online', 'pagaments', 'seguiment progrés'],
        conversion_rate: 0.13
      }
    ]
  },

  // Campaign Templates Configuration
  templates: {
    email: {
      // Template types for different campaign stages
      types: ['cold_outreach', 'follow_up_1', 'follow_up_2', 'case_study', 'offer'],
      
      // Common variables for personalization
      variables: [
        'business_name',
        'owner_name', 
        'sector',
        'location',
        'pain_points',
        'solutions',
        'case_study',
        'offer_details'
      ]
    }
  },

  // Automation Settings
  automation: {
    // Email frequency settings
    frequency: {
      cold_outreach: 1, // days between cold outreach emails
      follow_up_1: 3,   // days after cold outreach
      follow_up_2: 7,   // days after follow_up_1
      case_study: 14,   // days after follow_up_2
      offer: 21         // days after case_study
    },
    
    // Campaign limits per day/week
    limits: {
      emails_per_day: 50,
      emails_per_week: 250,
      max_concurrent_campaigns: 5
    },

    // Tracking and analytics
    tracking: {
      open_rate_target: 0.25,
      response_rate_target: 0.05,
      conversion_rate_target: 0.02
    }
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OUTREACH_CONFIG;
} else {
  window.OUTREACH_CONFIG = OUTREACH_CONFIG;
}