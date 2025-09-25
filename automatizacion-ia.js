// Traducciones para la página de Automatización IA
const autoIaTranslations = {
  es: {
    service_title: "Automatización IA",
    service_desc: "Automatiza procesos con inteligencia artificial, bots avanzados y sistemas inteligentes para transformar tu empresa. Descubre cómo los chatbots, la integración con WhatsApp Business y el análisis de datos pueden revolucionar tu negocio.",
    service_features: [
      "Chatbots inteligentes con IA",
      "Integración WhatsApp Business",
      "Automatización de tareas repetitivas",
      "Análisis de datos en tiempo real",
      "Workflows personalizados"
    ],
    service_cta: "Solicita asesoría gratuita"
  },
  en: {
    service_title: "AI Automation",
    service_desc: "Automate processes with artificial intelligence, advanced bots, and smart systems to transform your business. Discover how chatbots, WhatsApp Business integration, and data analysis can revolutionize your company.",
    service_features: [
      "Intelligent AI chatbots",
      "WhatsApp Business integration",
      "Repetitive task automation",
      "Real-time data analysis",
      "Custom workflows"
    ],
    service_cta: "Request free advice"
  },
  pt: {
    service_title: "Automação IA",
    service_desc: "Automatize processos com inteligência artificial, bots avançados e sistemas inteligentes para transformar sua empresa. Descubra como chatbots, integração com WhatsApp Business e análise de dados podem revolucionar seu negócio.",
    service_features: [
      "Chatbots inteligentes com IA",
      "Integração WhatsApp Business",
      "Automatização de tarefas repetitivas",
      "Análise de dados em tempo real",
      "Workflows personalizados"
    ],
    service_cta: "Solicite consultoria gratuita"
  }
};

function setAutoIaLanguage(lang) {
  const t = autoIaTranslations[lang] || autoIaTranslations['es'];
  document.querySelector('[data-translate="service_title"]').textContent = t.service_title;
  document.querySelector('[data-translate="service_desc"]').textContent = t.service_desc;
  const features = document.querySelectorAll('[data-translate="service_feature"]');
  features.forEach((el, i) => {
    el.textContent = t.service_features[i] || '';
  });
  document.querySelector('[data-translate="service_cta"]').textContent = t.service_cta;
}

// Detectar idioma global
const globalLang = localStorage.getItem('lang') || document.documentElement.lang || 'es';
setAutoIaLanguage(globalLang);

// Escuchar cambios de idioma global
window.addEventListener('languageChanged', function(e) {
  setAutoIaLanguage(e.detail.lang);
});
