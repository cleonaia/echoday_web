// Example Usage of Echoday Mass Outreach Automation System
// This file demonstrates how to use the system for different business scenarios

// Example 1: Beauty/Wellness Campaign in Sabadell (Catalan)
function createBeautyCampaign() {
  console.log('=== Creating Beauty & Wellness Campaign ===');
  
  // Initialize the automation system
  const automation = new OutreachAutomation(OUTREACH_CONFIG);
  
  // Create campaign
  const campaignId = automation.createCampaign({
    name: 'Bellesa Sabadell 2024',
    sector: 'beauty_wellness',
    language: 'ca',
    location: 'Sabadell'
  });
  
  // Generate realistic leads for beauty sector
  const beautyLeads = [
    {
      business_name: 'Perruqueria Estil',
      owner_name: 'Maria Torrents',
      email: 'info@perruqueriaestil.com',
      phone: '+34 937 123 456',
      sector: 'beauty_wellness',
      location: 'Sabadell',
      custom_data: {
        services: ['tallat', 'tint', 'pentinat'],
        employees: 3,
        established: 2018
      }
    },
    {
      business_name: 'Spa Wellness Centre',
      owner_name: 'Anna Puig',
      email: 'contacte@spawellness.cat',
      phone: '+34 937 234 567',
      sector: 'beauty_wellness',
      location: 'Sabadell',
      custom_data: {
        services: ['massatges', 'tractaments facials', 'depilació'],
        employees: 5,
        established: 2015
      }
    },
    {
      business_name: 'Estètica Natural',
      owner_name: 'Carme Vidal',
      email: 'hola@esteticanatural.com',
      phone: '+34 937 345 678',
      sector: 'beauty_wellness',
      location: 'Sabadell',
      custom_data: {
        services: ['tractaments naturals', 'ungles', 'celles'],
        employees: 2,
        established: 2020
      }
    }
  ];
  
  // Add leads to campaign
  automation.addLeadsToCampaign(campaignId, beautyLeads);
  
  console.log(`Campaign created: ${campaignId}`);
  console.log(`Added ${beautyLeads.length} leads`);
  
  return { automation, campaignId };
}

// Example 2: Medical/Health Campaign in Barcelona (Spanish)
function createMedicalCampaign() {
  console.log('=== Creating Medical & Health Campaign ===');
  
  const automation = new OutreachAutomation(OUTREACH_CONFIG);
  
  const campaignId = automation.createCampaign({
    name: 'Salud Barcelona 2024',
    sector: 'medical_health',
    language: 'es',
    location: 'Barcelona'
  });
  
  const medicalLeads = [
    {
      business_name: 'Clínica Dental Sonrisas',
      owner_name: 'Dr. Luis García',
      email: 'info@clinicasonrisas.com',
      phone: '+34 934 123 456',
      sector: 'medical_health',
      location: 'Barcelona',
      custom_data: {
        specialties: ['odontología general', 'ortodoncia', 'implantes'],
        staff: 8,
        established: 2012
      }
    },
    {
      business_name: 'Centro Médico Integral',
      owner_name: 'Dra. Carmen López',
      email: 'contacto@centromedico.es',
      phone: '+34 934 234 567',
      sector: 'medical_health',
      location: 'Barcelona',
      custom_data: {
        specialties: ['medicina general', 'pediatría', 'ginecología'],
        staff: 12,
        established: 2008
      }
    }
  ];
  
  automation.addLeadsToCampaign(campaignId, medicalLeads);
  
  console.log(`Campaign created: ${campaignId}`);
  console.log(`Added ${medicalLeads.length} leads`);
  
  return { automation, campaignId };
}

// Example 3: Restaurant Campaign Multi-language
function createRestaurantCampaign() {
  console.log('=== Creating Restaurant Campaign ===');
  
  const automation = new OutreachAutomation(OUTREACH_CONFIG);
  
  // Catalan campaign for local restaurants
  const campaignCaId = automation.createCampaign({
    name: 'Restaurants Vallès 2024',
    sector: 'restaurants_bars',
    language: 'ca',
    location: 'Terrassa'
  });
  
  const restaurantLeads = [
    {
      business_name: 'Restaurant Can Pere',
      owner_name: 'Pere Martínez',
      email: 'canpere@gmail.com',
      phone: '+34 937 654 321',
      sector: 'restaurants_bars',
      location: 'Terrassa',
      custom_data: {
        cuisine: 'catalana tradicional',
        capacity: 80,
        established: 2005
      }
    },
    {
      business_name: 'Pizzeria Milano',
      owner_name: 'Giuseppe Rossi',
      email: 'info@pizzeriamilano.cat',
      phone: '+34 937 765 432',
      sector: 'restaurants_bars',
      location: 'Terrassa',
      custom_data: {
        cuisine: 'italiana',
        capacity: 45,
        established: 2018
      }
    }
  ];
  
  automation.addLeadsToCampaign(campaignCaId, restaurantLeads);
  
  return { automation, campaignId: campaignCaId };
}

// Example 4: Simulate email sequence processing
async function simulateEmailSequence() {
  console.log('=== Simulating Email Sequence Processing ===');
  
  // Create a test campaign
  const { automation, campaignId } = createBeautyCampaign();
  
  // Get campaign analytics before processing
  const beforeAnalytics = automation.getCampaignAnalytics(campaignId);
  console.log('Before processing:', beforeAnalytics);
  
  // Simulate processing scheduled emails
  // Note: In real usage, this would actually send emails via Web3Forms
  console.log('Processing scheduled emails (simulation mode)...');
  
  // Get all leads from campaign
  const campaign = automation.campaigns.get(campaignId);
  const leads = campaign.leads.map(leadId => automation.leads.get(leadId));
  
  // Simulate processing each lead
  for (const lead of leads) {
    console.log(`Processing lead: ${lead.business_name}`);
    
    // Simulate template processing
    const variables = {
      business_name: lead.business_name,
      owner_name: lead.owner_name,
      sector: 'Bellesa i Benestar',
      location: lead.location,
      pain_points: 'sistema de cites, gestió de clients i promocions',
      case_study_results: 'un 60% més de cites reservades online i 95% satisfacció dels clients'
    };
    
    const emailContent = TemplateUtils.processTemplate('cold_outreach', variables, 'ca');
    
    if (emailContent) {
      console.log(`  Subject: ${emailContent.subject}`);
      console.log(`  Language: ${emailContent.language}`);
      
      // Update lead status (simulation)
      lead.sequence_step = 1;
      lead.last_contact = new Date();
      lead.status = 'contacted';
      
      // Update campaign analytics
      campaign.analytics.emails_sent++;
      automation.analytics.sent++;
    }
  }
  
  // Get analytics after processing
  const afterAnalytics = automation.getCampaignAnalytics(campaignId);
  console.log('After processing:', afterAnalytics);
  
  return automation;
}

// Example 5: Export campaign data for external CRM
function exportCampaignData() {
  console.log('=== Exporting Campaign Data ===');
  
  const { automation, campaignId } = createMedicalCampaign();
  
  // Export all campaign data
  const exportData = automation.exportCampaignData(campaignId);
  
  console.log('Exported data structure:');
  console.log('- Campaign info:', exportData.campaign.name);
  console.log('- Total leads:', exportData.leads.length);
  console.log('- Analytics:', exportData.analytics);
  
  // Example: Convert to CSV format for external use
  const csvHeaders = ['Business Name', 'Owner', 'Email', 'Phone', 'Status', 'Last Contact'];
  const csvRows = exportData.leads.map(lead => [
    lead.business_name,
    lead.owner_name,
    lead.email,
    lead.phone,
    lead.status,
    lead.last_contact || 'Never'
  ]);
  
  const csvContent = [csvHeaders, ...csvRows]
    .map(row => row.join(','))
    .join('\n');
  
  console.log('CSV Export Preview:');
  console.log(csvContent);
  
  return csvContent;
}

// Example 6: Performance analytics and optimization
function analyzePerformance() {
  console.log('=== Analyzing Campaign Performance ===');
  
  // Create multiple campaigns for comparison
  const beautyResult = createBeautyCampaign();
  const medicalResult = createMedicalCampaign();
  const restaurantResult = createRestaurantCampaign();
  
  const campaigns = [
    { name: 'Beauty', automation: beautyResult.automation, id: beautyResult.campaignId },
    { name: 'Medical', automation: medicalResult.automation, id: medicalResult.campaignId },
    { name: 'Restaurant', automation: restaurantResult.automation, id: restaurantResult.campaignId }
  ];
  
  console.log('Campaign Performance Comparison:');
  console.log('=====================================');
  
  campaigns.forEach(({ name, automation, id }) => {
    const analytics = automation.getCampaignAnalytics(id);
    console.log(`${name} Campaign:`);
    console.log(`  - Total Leads: ${analytics.total_leads}`);
    console.log(`  - Emails Sent: ${analytics.emails_sent}`);
    console.log(`  - Expected Conversion Rate: ${getExpectedConversionRate(name)}%`);
    console.log('');
  });
}

function getExpectedConversionRate(sector) {
  const rates = {
    'Beauty': 22,
    'Medical': 25,
    'Restaurant': 18,
    'Professional': 12,
    'Retail': 15,
    'Fitness': 16
  };
  return rates[sector] || 15;
}

// Usage Examples Runner
function runExamples() {
  console.log('🚀 Echoday Mass Outreach Automation - Usage Examples');
  console.log('==================================================\n');
  
  try {
    // Run all examples
    createBeautyCampaign();
    console.log('');
    
    createMedicalCampaign();
    console.log('');
    
    createRestaurantCampaign();
    console.log('');
    
    // Note: Uncomment to run simulation (requires Web3Forms API key)
    // simulateEmailSequence();
    
    exportCampaignData();
    console.log('');
    
    analyzePerformance();
    
    console.log('✅ All examples completed successfully!');
    console.log('');
    console.log('Next Steps:');
    console.log('1. Configure your Web3Forms API key in dashboard.html');
    console.log('2. Customize templates in templates.js for your brand');
    console.log('3. Add real leads data and start your first campaign');
    console.log('4. Monitor performance and optimize based on analytics');
    
  } catch (error) {
    console.error('❌ Error running examples:', error);
  }
}

// Auto-run examples when loaded in browser
if (typeof window !== 'undefined') {
  // Browser environment
  document.addEventListener('DOMContentLoaded', function() {
    console.log('Loading Echoday Outreach Examples...');
    
    // Wait for dependencies to load
    setTimeout(() => {
      if (typeof OUTREACH_CONFIG !== 'undefined' && 
          typeof OutreachAutomation !== 'undefined' && 
          typeof TemplateUtils !== 'undefined') {
        runExamples();
      } else {
        console.error('Dependencies not loaded. Make sure to include config.js, templates.js, and automation.js');
      }
    }, 1000);
  });
}

// Export for Node.js environment
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    createBeautyCampaign,
    createMedicalCampaign,
    createRestaurantCampaign,
    simulateEmailSequence,
    exportCampaignData,
    analyzePerformance,
    runExamples
  };
}