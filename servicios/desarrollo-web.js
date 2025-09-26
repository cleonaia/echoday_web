// Traducciones para la página de Desarrollo Web
const webDevTranslations = {
  es: {
    service_title: "Desarrollo Web",
    service_desc: "Creamos webs, apps, chatbots y dashboards con tecnología de punta y diseño atractivo, listos para crecer contigo. Descubre cómo una web profesional puede impulsar tu negocio y mejorar tu presencia online.",
    service_features: [
      "Diseño responsive y moderno",
      "Optimización SEO avanzada",
      "Integración con APIs",
      "Panel de administración",
      "Velocidad de carga optimizada"
    ],
    service_cta: "Solicita asesoría gratuita"
  },
  en: {
    service_title: "Web Development",
    service_desc: "We create websites, apps, chatbots, and dashboards with cutting-edge technology and attractive design, ready to grow with you. Discover how a professional website can boost your business and improve your online presence.",
    service_features: [
      "Responsive and modern design",
      "Advanced SEO optimization",
      "API integration",
      "Admin panel",
      "Optimized loading speed"
    ],
    service_cta: "Request free advice"
  },
  pt: {
    service_title: "Desenvolvimento Web",
    service_desc: "Criamos sites, aplicativos, chatbots e dashboards com tecnologia de ponta e design atraente, prontos para crescer com você. Descubra como um site profissional pode impulsionar seu negócio e melhorar sua presença online.",
    service_features: [
      "Design responsivo e moderno",
      "Otimização avançada de SEO",
      "Integração com APIs",
      "Painel de administração",
      "Velocidade de carregamento otimizada"
    ],
    service_cta: "Solicite consultoria gratuita"
  }
};

function setWebDevLanguage(lang) {
  const t = webDevTranslations[lang] || webDevTranslations['es'];
  document.querySelector('[data-translate="service_title"]').textContent = t.service_title;
  document.querySelector('[data-translate="service_desc"]').textContent = t.service_desc;
  const features = document.querySelectorAll('[data-translate="service_feature"]');
  features.forEach((el, i) => {
    el.textContent = t.service_features[i] || '';
  });
  document.querySelector('[data-translate="service_cta"]').textContent = t.service_cta;
}

const globalLang = localStorage.getItem('lang') || document.documentElement.lang || 'es';
setWebDevLanguage(globalLang);
window.addEventListener('languageChanged', function(e) {
  setWebDevLanguage(e.detail.lang);
});
