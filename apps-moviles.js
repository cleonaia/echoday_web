// Traducciones para la página de Apps Móviles
const appsMovilesTranslations = {
  es: {
    service_title: "Creación de Apps Móviles",
    service_desc: "Desarrollamos apps móviles para iOS y Android, personalizadas para tu negocio y clientes. Publicación en tiendas, notificaciones push y soporte post-lanzamiento.",
    service_features: [
      "Desarrollo iOS y Android",
      "Interfaz intuitiva y atractiva",
      "Notificaciones push",
      "Publicación en tiendas",
      "Sincronización en tiempo real"
    ],
    service_cta: "Solicita asesoría gratuita"
  },
  en: {
    service_title: "Mobile Apps Creation",
    service_desc: "We develop mobile apps for iOS and Android, customized for your business and clients. Store publishing, push notifications, and post-launch support.",
    service_features: [
      "iOS and Android development",
      "Intuitive and attractive interface",
      "Push notifications",
      "Store publishing",
      "Real-time synchronization"
    ],
    service_cta: "Request free advice"
  },
  pt: {
    service_title: "Criação de Apps Móveis",
    service_desc: "Desenvolvemos aplicativos móveis para iOS e Android, personalizados para seu negócio e clientes. Publicação nas lojas, notificações push e suporte pós-lançamento.",
    service_features: [
      "Desenvolvimento iOS e Android",
      "Interface intuitiva e atraente",
      "Notificações push",
      "Publicação nas lojas",
      "Sincronização em tempo real"
    ],
    service_cta: "Solicite consultoria gratuita"
  }
};

function setAppsMovilesLanguage(lang) {
  const t = appsMovilesTranslations[lang] || appsMovilesTranslations['es'];
  document.querySelector('[data-translate="service_title"]').textContent = t.service_title;
  document.querySelector('[data-translate="service_desc"]').textContent = t.service_desc;
  const features = document.querySelectorAll('[data-translate="service_feature"]');
  features.forEach((el, i) => {
    el.textContent = t.service_features[i] || '';
  });
  document.querySelector('[data-translate="service_cta"]').textContent = t.service_cta;
}

const globalLang = localStorage.getItem('lang') || document.documentElement.lang || 'es';
setAppsMovilesLanguage(globalLang);
window.addEventListener('languageChanged', function(e) {
  setAppsMovilesLanguage(e.detail.lang);
});
