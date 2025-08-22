// Demo Patient Data for Variable Substitution
// This file contains dummy data to populate variables in the encounter notes composer

const demoPatientData = {
    patient: {
        name: "Sarah Johnson",
        dob: "March 15, 1985",
        age: "39 years old",
        gender: "Female",
        mrn: "MR123456",
        phone: "(555) 123-4567",
        email: "sarah.johnson@email.com",
        address: "123 Main Street, Anytown, CA 90210",
        insurance: "Blue Cross Blue Shield - PPO",
        emergency_contact: "Michael Johnson (Spouse) - (555) 987-6543"
    },
    vitals: {
        bp: "128/82 mmHg",
        hr: "72 bpm",
        temp: "98.6°F (37.0°C)",
        resp: "16 breaths/min",
        o2sat: "98% on room air",
        height: "5'6\" (167.6 cm)",
        weight: "145 lbs (65.8 kg)",
        bmi: "23.4 kg/m²",
        pain_scale: "2/10"
    },
    history: {
        allergies: "Penicillin (rash), Shellfish (anaphylaxis)",
        medications: "Lisinopril 10mg daily, Metformin 500mg BID, Vitamin D3 2000 IU daily",
        conditions: "Type 2 Diabetes Mellitus, Hypertension, Hypothyroidism",
        surgeries: "Appendectomy (2010), Cholecystectomy (2018)",
        family_history: "Father: CAD, Mother: Breast cancer, Maternal grandmother: Diabetes",
        social_history: "Non-smoker, Occasional alcohol use (1-2 drinks/week), Regular exercise",
        immunizations: "COVID-19 (up to date), Influenza (annual), Tdap (2021)",
        last_visit: "September 15, 2024 - Annual physical exam"
    },
    visit: {
        date: "December 20, 2024",
        time: "2:15 PM",
        type: "Follow-up Consultation",
        chief_complaint: "Follow-up for diabetes management and blood pressure control",
        hpi: "Patient reports good adherence to medications. Blood sugars have been stable, ranging 110-140 mg/dL. Occasional morning headaches.",
        ros: "Denies chest pain, shortness of breath, or palpitations. No visual changes or numbness/tingling.",
        assessment: "Type 2 DM with good glycemic control, HTN stable on current regimen",
        plan: "Continue current medications, recheck A1C in 3 months, home BP monitoring"
    },
    provider: {
        name: "Dr. Emily Rodriguez",
        title: "Internal Medicine Physician",
        npi: "1234567890",
        license: "CA12345",
        specialty: "Internal Medicine",
        practice: "Westside Medical Group"
    },
    date: {
        today: new Date().toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        }),
        now: new Date().toLocaleString('en-US', {
            year: 'numeric',
            month: 'long', 
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }),
        visit: "December 20, 2024"
    },
    time: {
        now: new Date().toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }),
        visit: "2:15 PM"
    }
};

// Function to resolve variable paths (e.g., "patient.name" -> "Sarah Johnson")
function resolveVariable(variablePath) {
    const parts = variablePath.split('.');
    let current = demoPatientData;
    
    for (const part of parts) {
        if (current && typeof current === 'object' && part in current) {
            current = current[part];
        } else {
            return `{{${variablePath}}}`;  // Return original if not found
        }
    }
    
    return current;
}

// Function to substitute all variables in a text string
function substituteVariables(text) {
    // Match {{variable.path}} patterns
    const variableRegex = /\{\{([^}]+)\}\}/g;
    
    return text.replace(variableRegex, (match, variablePath) => {
        const value = resolveVariable(variablePath);
        return value !== undefined ? value : match;
    });
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { demoPatientData, resolveVariable, substituteVariables };
}
