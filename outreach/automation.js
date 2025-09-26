// Mass Outreach Automation System
// Manages campaigns, lead generation, and email sequence automation

class OutreachAutomation {
  constructor(config) {
    this.config = config;
    this.campaigns = new Map();
    this.leads = new Map();
    this.analytics = {
      sent: 0,
      opened: 0,
      responded: 0,
      converted: 0
    };
  }

  // Initialize a new campaign
  createCampaign(campaignData) {
    const campaignId = this.generateCampaignId();
    const campaign = {
      id: campaignId,
      name: campaignData.name,
      sector: campaignData.sector,
      language: campaignData.language || this.config.defaultLanguage,
      location: campaignData.location || this.config.location.primary,
      status: 'active',
      created: new Date(),
      leads: [],
      analytics: {
        total_leads: 0,
        emails_sent: 0,
        open_rate: 0,
        response_rate: 0,
        conversion_rate: 0
      }
    };

    this.campaigns.set(campaignId, campaign);
    return campaignId;
  }

  // Add leads to a campaign
  addLeadsToCampaign(campaignId, leadsData) {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) {
      throw new Error('Campaign not found');
    }

    leadsData.forEach(leadData => {
      const leadId = this.generateLeadId();
      const lead = {
        id: leadId,
        campaignId: campaignId,
        business_name: leadData.business_name,
        owner_name: leadData.owner_name,
        email: leadData.email,
        phone: leadData.phone,
        sector: leadData.sector,
        location: leadData.location,
        status: 'new', // new, contacted, responded, converted, unsubscribed
        sequence_step: 0, // Current step in email sequence
        last_contact: null,
        next_contact: new Date(),
        custom_data: leadData.custom_data || {},
        history: []
      };

      this.leads.set(leadId, lead);
      campaign.leads.push(leadId);
      campaign.analytics.total_leads++;
    });

    return campaign.leads.length;
  }

  // Process scheduled emails
  async processScheduledEmails() {
    const now = new Date();
    const readyLeads = Array.from(this.leads.values())
      .filter(lead => lead.next_contact <= now && lead.status === 'new' || lead.status === 'contacted');

    console.log(`Processing ${readyLeads.length} scheduled emails...`);

    for (const lead of readyLeads) {
      try {
        await this.sendSequenceEmail(lead);
        await this.delay(1000); // 1 second delay between emails
      } catch (error) {
        console.error(`Error processing lead ${lead.id}:`, error);
      }
    }
  }

  // Send email based on sequence step
  async sendSequenceEmail(lead) {
    const templates = ['cold_outreach', 'follow_up_1', 'follow_up_2', 'case_study', 'offer'];
    const templateType = templates[lead.sequence_step] || templates[0];

    // Get campaign data
    const campaign = this.campaigns.get(lead.campaignId);
    
    // Prepare template variables
    const variables = {
      business_name: lead.business_name,
      owner_name: lead.owner_name,
      sector: this.getSectorName(lead.sector, campaign.language),
      location: lead.location,
      pain_points: this.getSectorPainPoints(lead.sector, campaign.language),
      case_study_results: this.getCaseStudyResults(lead.sector, campaign.language),
      expiry_date: this.getExpiryDate()
    };

    // Process template
    const emailContent = TemplateUtils.processTemplate(templateType, variables, campaign.language);
    
    if (!emailContent) {
      throw new Error(`Template ${templateType} not found for language ${campaign.language}`);
    }

    // Prepare Web3Forms data
    const formData = {
      access_key: this.config.web3forms.apiKey,
      name: this.config.company.name,
      email: this.config.company.email,
      subject: emailContent.subject,
      message: emailContent.body,
      // Add lead tracking data
      lead_id: lead.id,
      campaign_id: lead.campaignId,
      template_type: templateType,
      target_email: lead.email,
      target_business: lead.business_name
    };

    // Send email via Web3Forms
    const response = await this.sendViaWeb3Forms(formData);
    
    if (response.success) {
      // Update lead status
      lead.sequence_step++;
      lead.last_contact = new Date();
      lead.next_contact = this.calculateNextContact(lead.sequence_step);
      lead.status = 'contacted';
      
      // Add to history
      lead.history.push({
        type: 'email_sent',
        template: templateType,
        date: new Date(),
        subject: emailContent.subject
      });

      // Update analytics
      campaign.analytics.emails_sent++;
      this.analytics.sent++;

      console.log(`Email sent to ${lead.business_name} (${templateType})`);
    } else {
      throw new Error(`Failed to send email: ${response.message}`);
    }
  }

  // Send email via Web3Forms API
  async sendViaWeb3Forms(formData) {
    try {
      const response = await fetch(this.config.web3forms.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Web3Forms API Error:', error);
      return { success: false, message: error.message };
    }
  }

  // Calculate next contact date based on sequence step
  calculateNextContact(step) {
    const frequencies = this.config.automation.frequency;
    const templateTypes = ['cold_outreach', 'follow_up_1', 'follow_up_2', 'case_study', 'offer'];
    const currentTemplate = templateTypes[step - 1] || 'follow_up_2';
    
    const daysToWait = frequencies[currentTemplate] || 7;
    const nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + daysToWait);
    
    return nextDate;
  }

  // Get sector name in specified language
  getSectorName(sectorKey, language) {
    const sector = this.findSectorByKey(sectorKey);
    return sector ? sector[language] : sectorKey;
  }

  // Find sector configuration by key
  findSectorByKey(sectorKey) {
    const allSectors = [...this.config.sectors.high_priority, ...this.config.sectors.medium_priority];
    return allSectors.find(sector => sector.name === sectorKey);
  }

  // Get sector-specific pain points
  getSectorPainPoints(sectorKey, language) {
    const sector = this.findSectorByKey(sectorKey);
    if (sector && sector.pain_points) {
      return sector.pain_points.join(', ');
    }
    return TemplateUtils.getSectorPainPoints(sectorKey, language);
  }

  // Get case study results for sector
  getCaseStudyResults(sectorKey, language) {
    return TemplateUtils.getCaseStudyResults(sectorKey, language);
  }

  // Get expiry date for offers (2 weeks from now)
  getExpiryDate() {
    const date = new Date();
    date.setDate(date.getDate() + 14);
    return date.toLocaleDateString('ca-ES');
  }

  // Generate unique campaign ID
  generateCampaignId() {
    return 'camp_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Generate unique lead ID
  generateLeadId() {
    return 'lead_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // Utility delay function
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Get campaign analytics
  getCampaignAnalytics(campaignId) {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) return null;

    const leads = campaign.leads.map(leadId => this.leads.get(leadId));
    const totalLeads = leads.length;
    const contacted = leads.filter(lead => lead.status === 'contacted' || lead.status === 'responded').length;
    const responded = leads.filter(lead => lead.status === 'responded').length;
    const converted = leads.filter(lead => lead.status === 'converted').length;

    return {
      campaign_name: campaign.name,
      total_leads: totalLeads,
      emails_sent: campaign.analytics.emails_sent,
      contacted: contacted,
      responded: responded,
      converted: converted,
      open_rate: contacted > 0 ? (contacted / campaign.analytics.emails_sent * 100).toFixed(2) : 0,
      response_rate: campaign.analytics.emails_sent > 0 ? (responded / campaign.analytics.emails_sent * 100).toFixed(2) : 0,
      conversion_rate: totalLeads > 0 ? (converted / totalLeads * 100).toFixed(2) : 0
    };
  }

  // Export campaign data
  exportCampaignData(campaignId) {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) return null;

    const leads = campaign.leads.map(leadId => this.leads.get(leadId));
    
    return {
      campaign: campaign,
      leads: leads,
      analytics: this.getCampaignAnalytics(campaignId)
    };
  }

  // Import leads from CSV format
  importLeadsFromCSV(csvData, campaignId) {
    const lines = csvData.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const leads = [];

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.trim());
      if (values.length === headers.length) {
        const lead = {};
        headers.forEach((header, index) => {
          lead[header] = values[index];
        });
        leads.push(lead);
      }
    }

    return this.addLeadsToCampaign(campaignId, leads);
  }
}

// Lead Generation Helper Functions
const LeadGeneration = {
  // Generate sample leads for testing
  generateSampleLeads: function(sector, location, count = 10) {
    const sampleNames = [
      'Maria García', 'Joan Martínez', 'Anna López', 'Pau Rodríguez', 
      'Laura Sánchez', 'Marc González', 'Clara Fernández', 'David Pérez',
      'Marta Ruiz', 'Jordi Vila', 'Núria Moreno', 'Carles Jiménez'
    ];

    const businessPrefixes = {
      restaurants_bars: ['Restaurant', 'Bar', 'Cafeteria', 'Pizzeria'],
      beauty_wellness: ['Perruqueria', 'Estètica', 'Centre', 'Spa'],
      retail_shops: ['Botiga', 'Moda', 'Boutique', 'Tenda'],
      medical_health: ['Clínica', 'Consulta', 'Centre Mèdic', 'Farmàcia']
    };

    const leads = [];
    for (let i = 0; i < count; i++) {
      const name = sampleNames[Math.floor(Math.random() * sampleNames.length)];
      const businessPrefix = businessPrefixes[sector][Math.floor(Math.random() * businessPrefixes[sector].length)];
      const businessName = `${businessPrefix} ${name.split(' ')[1]}`;
      
      leads.push({
        business_name: businessName,
        owner_name: name,
        email: `info@${businessName.toLowerCase().replace(/\s+/g, '')}.com`,
        phone: `+34 ${Math.floor(Math.random() * 900) + 600} ${Math.floor(Math.random() * 900) + 100} ${Math.floor(Math.random() * 900) + 100}`,
        sector: sector,
        location: location,
        custom_data: {
          estimated_employees: Math.floor(Math.random() * 20) + 1,
          estimated_revenue: Math.floor(Math.random() * 500000) + 50000
        }
      });
    }

    return leads;
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { OutreachAutomation, LeadGeneration };
} else {
  window.OutreachAutomation = OutreachAutomation;
  window.LeadGeneration = LeadGeneration;
}