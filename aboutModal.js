// Modal About para Echoday
// Este archivo se puede importar en tu HTML para mostrar el modal About
function showAboutModal() {
  let modal = document.getElementById('aboutModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'aboutModal';
    modal.style = `
      display:flex;position:fixed;top:0;left:0;right:0;bottom:0;z-index:9999;
      background:rgba(24,29,36,0.82);backdrop-filter:blur(2px);justify-content:center;align-items:center;`;
    modal.innerHTML = `
      <div style="background:rgba(26,29,38,0.98);border-radius:28px;box-shadow:0 8px 48px #23ffe355,0 2px 16px #60a8ff22;padding:44px 38px 38px 38px;max-width:520px;width:92vw;text-align:left;color:#fff;font-family:'Montserrat',Arial,sans-serif;font-size:1.13rem;position:relative;animation:fadeup 0.7s cubic-bezier(.23,1.05,.32,1);overflow:hidden;line-height:1.7;letter-spacing:0.01em;margin:0 auto;box-sizing:border-box;">
        <div style='font-size:2.1rem;margin-bottom:18px;color:#23ffe3;font-weight:900;letter-spacing:1.1px;text-align:center;'>Sobre mí <span style='font-size:1.2rem;vertical-align:middle;margin-left:7px;'><i class='fa-solid fa-user-graduate fa-bounce'></i></span></div>
        <div id='aboutText' style='color:#a8e3e0;font-size:1.13rem;font-family:"Poppins",Arial,sans-serif;font-weight:500;line-height:1.7;letter-spacing:0.01em;max-width:440px;margin:0 auto;text-align:left;'></div>
        <button id='closeAboutBtn' style='background:linear-gradient(90deg,#23ffe3,#60a8ff 80%);color:#181d24;border:none;border-radius:22px;padding:10px 28px;font-size:1.07rem;font-weight:700;cursor:pointer;font-family:"Montserrat",Arial,sans-serif;margin-top:28px;box-shadow:0 0 8px 1px #42fa7a33;transition:background 0.18s, color 0.15s, transform 0.13s, box-shadow 0.2s;display:block;margin-left:auto;margin-right:auto;'>Cerrar</button>
      </div>
    `;
    document.body.appendChild(modal);
    document.getElementById('closeAboutBtn').onclick = function() {
      modal.style.display = 'none';
    };
    modal.addEventListener('click', function(e){
      if(e.target === modal) modal.style.display = 'none';
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape') modal.style.display = 'none';
    });
  } else {
    modal.style.display = 'flex';
  }
  // Texto profesional y motivador
  const aboutText = `¡Hola! Soy un estudiante de Ingeniería de Datos con una profunda pasión por la innovación y el desarrollo tecnológico. Mi objetivo es aportar soluciones creativas y eficientes que impulsen la transformación digital, especialmente en Sudamérica, una región llena de potencial y oportunidades para abrir nuevos horizontes de conocimiento.\n\nMe motiva crear herramientas y plataformas que faciliten la vida de las personas y las empresas, utilizando datos, inteligencia artificial y automatización para resolver desafíos reales. Creo firmemente que la tecnología es un motor de cambio positivo, y por eso busco estar siempre a la vanguardia, aprendiendo y aplicando las mejores prácticas del sector.\n\nMi visión es contribuir al desarrollo de una región más competitiva, conectada y preparada para el futuro, colaborando con equipos multidisciplinarios y compartiendo el conocimiento adquirido. Si compartes esta pasión por innovar y transformar, ¡conversemos y creemos juntos el próximo gran proyecto!`;
  const el = document.getElementById('aboutText');
  if (el) {
    el.innerHTML = '';
    let i = 0;
    function typeWriter() {
      if (i < aboutText.length) {
        el.innerHTML += aboutText.charAt(i) === '\n' ? '<br>' : aboutText.charAt(i);
        i++;
        setTimeout(typeWriter, aboutText.charAt(i-1) === '.' ? 32 : 13);
      }
    }
    typeWriter();
  }
}
// Puedes llamar a showAboutModal() desde cualquier parte de tu HTML para mostrar el modal
