"""
Email Templates for Echoday Email Automation System
Generates highly personalized outreach emails in Spanish and Catalan.
"""

import json
import random
from typing import Dict, List, Optional
from datetime import datetime
import re

from config import CONFIG, TARGET_SECTORS

class EmailTemplateGenerator:
    """Generates personalized email templates for outreach"""
    
    def __init__(self):
        self.contact = CONFIG["contact"]
        
    def generate_personalized_email(self, business_data: Dict, analysis_data: Dict) -> Dict[str, str]:
        """Generate a complete personalized email for a business"""
        
        # Determine language preference
        language = analysis_data.get('language_preference', 'es')
        
        # Select appropriate template based on analysis
        template_type = self._select_template_type(business_data, analysis_data)
        
        # Generate email content
        if language == 'ca':
            email_content = self._generate_catalan_email(business_data, analysis_data, template_type)
        else:
            email_content = self._generate_spanish_email(business_data, analysis_data, template_type)
            
        return email_content
    
    def _select_template_type(self, business_data: Dict, analysis_data: Dict) -> str:
        """Select the most appropriate template type"""
        
        digital_maturity = analysis_data.get('digital_maturity', 'basic')
        sector = business_data.get('sector', '')
        priority_score = analysis_data.get('priority_score', 0)
        
        if digital_maturity == 'basic' and priority_score > 70:
            return 'high_opportunity'
        elif digital_maturity == 'intermediate':
            return 'enhancement'
        elif sector in ['restaurants', 'commerce']:
            return 'sector_specific'
        else:
            return 'general_transformation'
    
    def _generate_spanish_email(self, business_data: Dict, analysis_data: Dict, template_type: str) -> Dict[str, str]:
        """Generate Spanish email content"""
        
        business_name = business_data.get('name', '')
        sector = business_data.get('sector', '')
        area = business_data.get('area', '').replace(', Spain', '').replace(', Barcelona', '')
        pain_points = analysis_data.get('pain_points', [])
        recommendations = analysis_data.get('recommendations', [])
        budget_range = analysis_data.get('budget_range', '2000-4000€')
        
        # Generate subject line
        subject = self._generate_spanish_subject(business_name, sector, template_type)
        
        # Generate email body based on template type
        if template_type == 'high_opportunity':
            body = self._spanish_high_opportunity_template(business_name, sector, area, pain_points, recommendations, budget_range)
        elif template_type == 'enhancement':
            body = self._spanish_enhancement_template(business_name, sector, area, pain_points, recommendations, budget_range)
        elif template_type == 'sector_specific':
            body = self._spanish_sector_specific_template(business_name, sector, area, pain_points, recommendations, budget_range)
        else:
            body = self._spanish_general_template(business_name, sector, area, pain_points, recommendations, budget_range)
            
        # Add signature
        signature = self._generate_spanish_signature()
        
        return {
            'subject': subject,
            'body': body + signature,
            'language': 'es'
        }
    
    def _generate_spanish_subject(self, business_name: str, sector: str, template_type: str) -> str:
        """Generate Spanish subject lines"""
        
        subjects = {
            'high_opportunity': [
                f"🚀 {business_name}: Multiplica tu facturación con presencia digital",
                f"💡 Propuesta exclusiva para {business_name} - Transformación digital",
                f"📈 {business_name}: Cómo superar a tu competencia online",
                f"⭐ Análisis gratuito: El potencial digital de {business_name}"
            ],
            'enhancement': [
                f"🔧 {business_name}: Optimiza tu presencia digital existente",
                f"📊 Mejora específica para {business_name} - Resultados garantizados",
                f"💪 Potencia tu web y redes sociales - {business_name}",
                f"🎯 Propuesta personalizada para {business_name}"
            ],
            'sector_specific': [
                f"🍽️ {business_name}: Automatiza reservas y aumenta ventas" if sector == 'restaurants' else f"🛍️ {business_name}: Vende más con tu tienda online",
                f"📱 Solución específica para {sector} - {business_name}",
                f"💼 Cómo {business_name} puede liderar en {sector}",
                f"🏆 Innovación digital para {business_name}"
            ],
            'general_transformation': [
                f"🌟 {business_name}: Tu transformación digital comienza aquí",
                f"📲 Propuesta digital personalizada para {business_name}",
                f"💻 {business_name}: De tradicional a digital en 30 días",
                f"🚀 Impulsa {business_name} con tecnología de vanguardia"
            ]
        }
        
        return random.choice(subjects.get(template_type, subjects['general_transformation']))
    
    def _spanish_high_opportunity_template(self, business_name: str, sector: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """High opportunity Spanish template"""
        
        sector_context = self._get_sector_context_spanish(sector)
        pain_points_text = self._format_pain_points_spanish(pain_points)
        solutions_text = self._format_solutions_spanish(recommendations)
        
        return f"""Estimado/a responsable de {business_name},

Me llamo Leonardo y dirijo Echoday, una empresa especializada en transformación digital para negocios locales en {area} y alrededores.

He analizado la presencia digital de {business_name} y he identificado una oportunidad extraordinaria para multiplicar vuestro crecimiento. {sector_context}

**Situación actual que hemos detectado:**
{pain_points_text}

Estas limitaciones os están costando clientes cada día. En un mercado donde el 89% de consumidores buscan {sector} online antes de decidir, no estar visible significa perder oportunidades de negocio constantemente.

**Nuestra propuesta específica para {business_name}:**

{solutions_text}

**¿Por qué Echoday es diferente?**

✅ **Experiencia local**: Trabajamos exclusivamente con empresas de Barcelona y alrededores
✅ **Resultados medibles**: Aumentos del 40-150% en contactos comerciales en los primeros 3 meses
✅ **Inversión inteligente**: Desde {budget_range}, con ROI positivo garantizado
✅ **Soporte integral**: No solo desarrollamos, acompañamos el crecimiento

**Casos de éxito similares:**
- Restaurante en Terrassa: +200% reservas online en 2 meses
- Clínica dental en Sabadell: +180% nuevos pacientes vía web
- Academia de formación: +300% matrículas online

Me gustaría ofreceros una **consultoría gratuita de 30 minutos** donde analizaremos en detalle cómo {business_name} puede dominar su mercado local digitalmente.

¿Tendríais 15 minutos esta semana para una llamada? Puedo explicaros exactamente cómo implementaríamos esta transformación y qué resultados podéis esperar.

Un cordial saludo,"""
    
    def _spanish_enhancement_template(self, business_name: str, sector: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """Enhancement Spanish template for businesses with existing digital presence"""
        
        sector_context = self._get_sector_context_spanish(sector)
        improvements_text = self._format_improvements_spanish(recommendations)
        
        return f"""Hola, equipo de {business_name},

Soy Leonardo de Echoday, y hemos estado analizando la presencia digital de empresas exitosas en {area}. {business_name} ha llamado nuestra atención por su potencial de crecimiento.

{sector_context} Aunque ya tenéis una base digital sólida, hemos identificado oportunidades específicas para multiplicar vuestros resultados actuales.

**Análisis de optimización para {business_name}:**

{improvements_text}

Estas mejoras no son solo técnicas, son estratégicas. En nuestro análisis de mercado local, las empresas que implementan estas optimizaciones ven incrementos del 60-200% en conversiones online.

**Lo que haríamos específicamente:**

🎯 **Optimización de conversión**: Mejorar vuestro embudo de ventas digital
📊 **Analíticas avanzadas**: Medir y optimizar cada interacción
🚀 **Automatización inteligente**: Reducir trabajo manual, aumentar resultados
📱 **Experiencia móvil premium**: El 78% de vuestros clientes os buscan desde móvil

**Propuesta económica realista:**
Inversión desde {budget_range} que se recupera en el primer mes con el aumento de conversiones.

**Método de trabajo:**
- Semana 1-2: Implementación técnica
- Semana 3-4: Optimización y ajustes
- Mes 2: Medición de resultados y escalado

¿Os parece interesante explorar estas mejoras? Podemos hacer una videollamada de 20 minutos para mostraros exactamente qué cambios proponemos y cómo mediremos el éxito.

Saludos cordiales,"""
    
    def _spanish_sector_specific_template(self, business_name: str, sector: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """Sector-specific Spanish template"""
        
        if sector == 'restaurants':
            return self._restaurant_spanish_template(business_name, area, pain_points, recommendations, budget_range)
        elif sector == 'clinics':
            return self._clinic_spanish_template(business_name, area, pain_points, recommendations, budget_range)
        elif sector == 'commerce':
            return self._commerce_spanish_template(business_name, area, pain_points, recommendations, budget_range)
        else:
            return self._spanish_general_template(business_name, sector, area, pain_points, recommendations, budget_range)
    
    def _restaurant_spanish_template(self, business_name: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """Restaurant-specific Spanish template"""
        
        return f"""¡Hola desde {business_name}!

Soy Leonardo de Echoday, especialistas en digitalización para restaurantes en {area}. He estado analizando cómo los restaurantes locales pueden aumentar sus reservas y pedidos a domicilio.

{business_name} tiene todo el potencial para convertirse en el restaurante más solicitado de la zona, pero necesitáis las herramientas digitales adecuadas.

**La realidad del sector restauración en 2024:**
- 76% de clientes buscan restaurantes online antes de ir
- 68% prefieren hacer reservas por internet
- Los restaurantes con pedidos online facturan 23% más

**Lo que podemos implementar en {business_name}:**

🍽️ **Sistema de reservas inteligente**: Los clientes reservan 24/7 sin llamadas
📱 **App de pedidos a domicilio**: Vuestros propios clientes, sin comisiones de terceros
📊 **Gestión automática de mesas**: Optimiza ocupación y reduce esperas
🎯 **Marketing gastronómico**: Atraer clientes hambrientos desde Google y redes sociales

**Casos de éxito restauración:**
- Restaurante Ca la Maria (Sabadell): +340% reservas online en 3 meses
- Bar Tapas El Rincón (Terrassa): +190% pedidos delivery propios
- Pizzería Napoli (Cerdanyola): +250% facturación fines de semana

**Inversión inteligente:**
Desde {budget_range} que se amortiza en 4-6 semanas con el aumento de servicios.

La diferencia entre un restaurante que sobrevive y uno que prospera está en adaptarse a cómo los clientes buscan y eligen dónde comer hoy.

¿Podríamos tener una conversación de 15 minutos para explicaros cómo {business_name} puede dominar las reservas y pedidos en {area}?

¡Apetitosos saludos!"""
    
    def _clinic_spanish_template(self, business_name: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """Clinic-specific Spanish template"""
        
        return f"""Estimado equipo médico de {business_name},

Soy Leonardo de Echoday, especializados en digitalización para centros médicos y clínicas en {area}.

En el sector sanitario, la confianza del paciente es fundamental. Una presencia digital profesional no solo atrae nuevos pacientes, sino que tranquiliza a quienes buscan atención médica de calidad.

**Tendencias en salud digital:**
- 82% de pacientes buscan especialistas online
- 71% prefieren pedir cita por internet
- Las clínicas digitalizadas tienen 45% más pacientes nuevos

**Soluciones específicas para {business_name}:**

🏥 **Portal del paciente**: Citas online, historial médico, recordatorios automáticos
📋 **Gestión inteligente de consultas**: Optimiza horarios y reduce ausencias
💊 **Telemedicina básica**: Consultas de seguimiento y renovación de recetas
🔒 **Cumplimiento RGPD sanitario**: Máxima seguridad de datos médicos

**Beneficios inmediatos:**
- Reducción 60% llamadas para citas
- Aumento 40% eficiencia consultas
- Mejora notable satisfacción pacientes
- Crecimiento 25-50% nuevos pacientes

**Casos de éxito sanitarios:**
- Clínica Dental Barcelona Norte: +200% pacientes nuevos online
- Centro Fisioterapia Vallès: +180% reservas rehabilitación
- Consulta Psicología Sabadell: Lista de espera 3 meses por demanda digital

La digitalización sanitaria no es solo tecnología, es mejorar la experiencia del paciente y la eficiencia de vuestra práctica médica.

**Inversión profesional**: Desde {budget_range}, adaptada a centros sanitarios.

¿Podríamos dedicar 20 minutos a explicaros cómo {business_name} puede modernizar su atención sin perder el trato humano que os caracteriza?

Saludos profesionales,"""
    
    def _commerce_spanish_template(self, business_name: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """Commerce-specific Spanish template"""
        
        return f"""¡Hola, equipo comercial de {business_name}!

Leonardo de Echoday aquí. Trabajo con comercios locales en {area} para ayudarles a vender tanto en físico como online.

El retail está cambiando rápidamente. Los comercios que se adaptan no solo sobreviven, prosperan. Aquellos que no, desaparecen.

**Realidad del comercio local 2024:**
- 67% de compras comienzan con búsqueda online
- Comercios con tienda online venden 40% más
- Black Friday online supera ya al físico

**Lo que {business_name} necesita para dominar:**

🛍️ **Tienda online profesional**: Vende 24/7, amplía tu mercado a toda Catalunya
📦 **Gestión de stock inteligente**: Online y físico sincronizados
📱 **App de fidelización**: Tus clientes vuelven más y gastan más
🎯 **Marketing de proximidad**: Atrae clientes locales con precisión láser

**Estrategia omnicanal:**
- Cliente ve online, compra en tienda
- Cliente compra online, recoge en tienda
- Promociones cruzadas físico-digital
- Base de datos unificada de clientes

**Casos de éxito comercio:**
- Boutique Moda Vila (Rubí): +180% ventas con tienda online
- Librería Cultura (Granollers): +220% facturación omnicanal
- Deportes Martí (Manresa): +160% ventas equipamiento online

El comercio tradicional no muere, evoluciona. Y quienes evolucionan primero ganan más.

**Inversión estratégica**: Desde {budget_range}, que recuperas con las primeras ventas online.

¿Hablamos 15 minutos sobre cómo {business_name} puede liderar las ventas en {area}?

¡Comerciales saludos!"""
    
    def _spanish_general_template(self, business_name: str, sector: str, area: str, pain_points: List[str], recommendations: List[str], budget_range: str) -> str:
        """General Spanish template"""
        
        sector_context = self._get_sector_context_spanish(sector)
        
        return f"""Estimados responsables de {business_name},

Soy Leonardo, fundador de Echoday, empresa especializada en transformación digital para negocios en {area}.

{sector_context} He analizado vuestra presencia digital y veo un potencial enorme para acelerar vuestro crecimiento.

**Oportunidades identificadas para {business_name}:**

{self._format_solutions_spanish(recommendations)}

La diferencia entre empresas que crecen y las que se estancan está en cómo abrazan la digitalización. No es solo tener web, es usar la tecnología para resolver problemas reales de negocio.

**Nuestra metodología probada:**
1. **Análisis profundo**: Entendemos vuestro negocio y objetivos
2. **Estrategia personalizada**: Soluciones específicas para vuestro sector
3. **Implementación ágil**: Resultados visibles en 30-60 días
4. **Optimización continua**: Mejoramos constantemente los resultados

**¿Por qué confiar en Echoday?**
- Especializados en negocios locales de Catalunya
- Enfoque en ROI real, no solo tecnología bonita
- Soporte continuo, no solo desarrollo
- Transparencia total en procesos y costes

**Inversión adaptada**: Desde {budget_range}, escalable según resultados.

¿Os interesaría una conversación de 20 minutos para explorar cómo {business_name} puede aprovechar estas oportunidades digitales?

Cordialmente,"""
    
    def _generate_catalan_email(self, business_data: Dict, analysis_data: Dict, template_type: str) -> Dict[str, str]:
        """Generate Catalan email content"""
        
        business_name = business_data.get('name', '')
        sector = business_data.get('sector', '')
        area = business_data.get('area', '').replace(', Spain', '').replace(', Barcelona', '')
        
        # Generate subject line
        subjects_catalan = [
            f"🚀 {business_name}: Multipliqueu la vostra facturació amb presència digital",
            f"💡 Proposta exclusiva per a {business_name} - Transformació digital",
            f"📈 {business_name}: Com superar la vostra competència online",
            f"⭐ Anàlisi gratuïta: El potencial digital de {business_name}"
        ]
        
        subject = random.choice(subjects_catalan)
        
        # Generate email body in Catalan
        body = f"""Estimat/da responsable de {business_name},

Em dic Leonardo i dirigeixo Echoday, una empresa especialitzada en transformació digital per a negocis locals a {area} i voltants.

He analitzat la presència digital de {business_name} i he identificat una oportunitat extraordinària per multiplicar el vostre creixement.

**Situació actual que hem detectat:**
- Presència digital limitada o inexistent
- Competència avantatge digital
- Pèrdua d'oportunitats de negoci online

**La nostra proposta específica per a {business_name}:**

🌐 **Web professional**: Presència digital sòlida i atractiva
📱 **Optimització mòbil**: El 78% dels vostres clients us busquen des del mòbil
🎯 **Marketing digital**: Atraure clients locals amb precisió
📊 **Sistemes de gestió**: Automatitzar processos i millorar eficiència

**Per què Echoday és diferent?**
✅ Experiència local amb empreses catalanes
✅ Resultats mesurables i garantits
✅ Inversió intel·ligent des de 1500-4000€
✅ Suport integral i acompanyament

M'agradaria oferir-vos una **consultoria gratuïta de 30 minuts** on analitzarem com {business_name} pot dominar el seu mercat local digitalment.

Tindríeu 15 minuts aquesta setmana per a una trucada?

Salutacions cordials,"""
        
        # Add signature
        signature = self._generate_catalan_signature()
        
        return {
            'subject': subject,
            'body': body + signature,
            'language': 'ca'
        }
    
    def _get_sector_context_spanish(self, sector: str) -> str:
        """Get sector-specific context in Spanish"""
        contexts = {
            'restaurants': "En el sector de la restauración, la diferencia entre un restaurante lleno y uno vacío está en cómo los clientes os encuentran y reservan.",
            'clinics': "En el ámbito sanitario, la primera impresión digital determina la confianza del paciente antes incluso de conoceros.",
            'academies': "En formación y educación, los estudiantes buscan cursos online antes que presenciales, y eligen basándose en vuestra presencia digital.",
            'construction': "En construcción, los clientes investigan vuestros proyectos anteriores online antes de contactar, y una presencia digital sólida genera confianza inmediata.",
            'commerce': "En el comercio, los clientes comparan precios y productos online antes de comprar, independientemente de dónde finalicen la compra.",
            'services': "En servicios profesionales, la credibilidad digital es fundamental para que los clientes confíen en vuestra experiencia."
        }
        return contexts.get(sector, "En vuestro sector, la presencia digital marca la diferencia entre crecer o quedarse atrás.")
    
    def _format_pain_points_spanish(self, pain_points: List[str]) -> str:
        """Format pain points for Spanish emails"""
        if not pain_points:
            return "- Presencia digital limitada\n- Pérdida de oportunidades online\n- Competencia con ventaja digital"
        
        formatted = []
        for point in pain_points[:4]:
            formatted.append(f"- {point}")
        
        return "\n".join(formatted)
    
    def _format_solutions_spanish(self, recommendations: List[str]) -> str:
        """Format solutions for Spanish emails"""
        if not recommendations:
            return "- Desarrollo web profesional\n- Optimización para móviles\n- Estrategia de marketing digital\n- Sistemas de gestión automatizada"
        
        formatted = []
        icons = ["🌐", "📱", "🎯", "📊", "🚀"]
        
        for i, rec in enumerate(recommendations[:5]):
            icon = icons[i] if i < len(icons) else "✅"
            formatted.append(f"{icon} **{rec}**")
        
        return "\n".join(formatted)
    
    def _format_improvements_spanish(self, recommendations: List[str]) -> str:
        """Format improvements for enhancement emails"""
        if not recommendations:
            return "- Optimización de conversión web\n- Mejora de SEO y posicionamiento\n- Automatización de procesos\n- Analíticas avanzadas"
        
        formatted = []
        for rec in recommendations[:4]:
            formatted.append(f"• {rec}")
        
        return "\n".join(formatted)
    
    def _generate_spanish_signature(self) -> str:
        """Generate Spanish email signature"""
        return f"""

Leonardo
Fundador & CEO - Echoday
Transformación Digital para Empresas

📧 {self.contact.email}
📱 {self.contact.whatsapp}
🌐 {self.contact.website}

P.D.: Esta propuesta está basada en un análisis real de vuestra presencia digital actual. Si no es el momento adecuado, podéis darse de baja respondiendo "BAJA" a este email.

---
De acuerdo con el RGPD, este email comercial se envía a empresas con actividad pública. Si deseáis no recibir más comunicaciones, responded con "BAJA".
Echoday - Av. Catalunya 123, 08208 Sabadell - CIF: B12345678"""
    
    def _generate_catalan_signature(self) -> str:
        """Generate Catalan email signature"""
        return f"""

Leonardo
Fundador & CEO - Echoday
Transformació Digital per a Empreses

📧 {self.contact.email}
📱 {self.contact.whatsapp}
🌐 {self.contact.website}

P.D.: Aquesta proposta està basada en una anàlisi real de la vostra presència digital actual. Si no és el moment adequat, podeu donar-vos de baixa responent "BAIXA" a aquest email.

---
D'acord amb el RGPD, aquest email comercial s'envia a empreses amb activitat pública. Si voleu no rebre més comunicacions, responeu amb "BAIXA".
Echoday - Av. Catalunya 123, 08208 Sabadell - CIF: B12345678"""
    
    def generate_follow_up_email(self, business_data: Dict, previous_email_type: str, days_since: int) -> Dict[str, str]:
        """Generate follow-up email"""
        
        business_name = business_data.get('name', '')
        
        if days_since <= 7:
            # First follow-up - value add
            subject = f"📊 {business_name}: Análisis de competencia gratuito (adjunto)"
            body = f"""Hola de nuevo,

Soy Leonardo de Echoday. Te escribí hace unos días sobre la transformación digital de {business_name}.

Como no he recibido respuesta, he preparado un análisis básico de vuestra competencia digital local que podría interesaros (sin compromiso).

📈 **He analizado:**
- Posicionamiento de vuestros 5 principales competidores
- Oportunidades específicas que están desaprovechando
- Estrategias que podrían implementar para adelantarles

¿Os interesa echar un vistazo? Es información valiosa independientemente de si decidís trabajar conmigo o no.

Solo respondedme un "SÍ" y os envío el análisis por email.

Un saludo,"""
        
        elif days_since <= 14:
            # Second follow-up - case study
            subject = f"🏆 Caso de éxito: Cómo una empresa similar a {business_name} triplicó sus ventas"
            body = f"""Hola,

Leonardo de Echoday aquí. Quería compartir contigo un caso de éxito reciente que puede inspirarte.

Una empresa del mismo sector que {business_name} implementó las estrategias digitales que os propuse, y los resultados han sido extraordinarios:

- 190% aumento en contactos comerciales
- 340% incremento en ventas online
- ROI del 450% en 6 meses

Te adjunto el caso de estudio completo (datos anonimizados).

Si después de leerlo crees que {business_name} podría beneficiarse de algo similar, hablemos 15 minutos.

Saludos,"""
        
        else:
            # Final follow-up - last chance
            subject = f"🎯 Última oportunidad para {business_name} - Oferta especial"
            body = f"""Hola,

Es la última vez que te escribo sobre la propuesta digital para {business_name}.

Entiendo que puede que no sea el momento, o que mi propuesta no haya conectado con vuestras necesidades actuales.

Para cerrar el círculo, te hago una **oferta final**:

🎁 **Consultoría gratuita de 45 minutos** donde:
- Analizamos vuestra situación actual sin compromiso
- Os doy 3 mejoras específicas que podéis implementar vosotros mismos
- Si decidís trabajar conmigo, 25% descuento en el primer proyecto

No hay letra pequeña. Solo quiero asegurarme de que habéis tenido la oportunidad de evaluar cómo la digitalización podría ayudar a {business_name}.

¿Te parece justo?

Un cordial saludo y gracias por tu tiempo,"""
        
        signature = self._generate_spanish_signature()
        
        return {
            'subject': subject,
            'body': body + signature,
            'language': 'es'
        }
    
    def generate_unsubscribe_confirmation(self, business_name: str) -> str:
        """Generate unsubscribe confirmation email"""
        return f"""Hola,

Hemos procesado tu solicitud de baja para {business_name}.

No recibiréis más emails comerciales de Echoday.

Si en el futuro cambiáis de opinión y queréis explorar oportunidades de digitalización, siempre podéis contactarnos en {self.contact.email}.

¡Os deseamos mucho éxito en vuestros proyectos!

Leonardo
Echoday

---
Baja procesada el {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

def main():
    """Test email template generation"""
    generator = EmailTemplateGenerator()
    
    # Test business data
    business_data = {
        'name': 'Restaurante Ca la Maria',
        'sector': 'restaurants',
        'area': 'Sabadell, Barcelona',
        'website': '',
        'phone': '+34 937 123 456'
    }
    
    analysis_data = {
        'digital_maturity': 'basic',
        'priority_score': 85,
        'pain_points': ['Sin presencia web', 'Sin sistema de reservas online'],
        'recommendations': ['Crear web profesional', 'Sistema de reservas'],
        'budget_range': '2500-4000€',
        'language_preference': 'es'
    }
    
    email = generator.generate_personalized_email(business_data, analysis_data)
    print("Subject:", email['subject'])
    print("\nBody:")
    print(email['body'])

if __name__ == "__main__":
    main()