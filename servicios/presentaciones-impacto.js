// Traducciones para la página de Presentaciones de Impacto
const presentacionesTranslations = {
  es: {
    service_title: "Presentaciones de Impacto",
    service_desc: "Convierte tu pitch, demo o evento en una experiencia memorable. Sorprende a tu audiencia desde el primer minuto con diseño visual, animaciones y contenido persuasivo.",
    service_features: [
      "Diseño visual impactante",
      "Animaciones y transiciones",
      "Contenido persuasivo",
      "Interactividad avanzada",
      "Adaptado a tu audiencia"
    ],
    service_cta: "Solicita asesoría gratuita"
  },
  en: {
    service_title: "Impactful Presentations",
    service_desc: "Turn your pitch, demo, or event into a memorable experience. Impress your audience from the first minute with visual design, animations, and persuasive content.",
    service_features: [
      "Striking visual design",
      "Animations and transitions",
      "Persuasive content",
      "Advanced interactivity",
      "Tailored to your audience"
    ],
    service_cta: "Request free advice"
  },
  pt: {
    service_title: "Apresentações de Impacto",
    service_desc: "Transforme seu pitch, demo ou evento em uma experiência memorável. Surpreenda sua audiência desde o primeiro minuto com design visual, animações e conteúdo persuasivo.",
    service_features: [
      "Design visual marcante",
      "Animações e transições",
      "Conteúdo persuasivo",
      "Interatividade avançada",
      "Adaptado ao seu público"
    ],
    service_cta: "Solicite consultoria gratuita"
  }
};

function setPresentacionesLanguage(lang) {
  const t = presentacionesTranslations[lang] || presentacionesTranslations['es'];
  document.querySelector('[data-translate="service_title"]').textContent = t.service_title;
  document.querySelector('[data-translate="service_desc"]').textContent = t.service_desc;
  const features = document.querySelectorAll('[data-translate="service_feature"]');
  features.forEach((el, i) => {
    el.textContent = t.service_features[i] || '';
  });
  document.querySelector('[data-translate="service_cta"]').textContent = t.service_cta;
}

const globalLang = localStorage.getItem('lang') || document.documentElement.lang || 'es';
setPresentacionesLanguage(globalLang);
window.addEventListener('languageChanged', function(e) {
  setPresentacionesLanguage(e.detail.lang);
});
