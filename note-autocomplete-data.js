window.NOTE_AUTOCOMPLETE_SUGGESTIONS = [
  {
    id: 'hpi-followup',
    trigger: 'history of present illness:',
    completion: '\nPatient reports adherence to medications without adverse effects. Symptoms remain stable with no new concerns.',
    description: 'Adds a natural follow-up sentence for the HPI section.'
  },
  {
    id: 'ros-denies',
    trigger: 'patient denies',
    completion: ' chest pain, shortness of breath, palpitations, dizziness, or syncope.',
    description: 'Common negative ROS statement to finish the sentence.'
  },
  {
    id: 'assessment-plan',
    trigger: 'assessment & plan:',
    completion: '\n- Reinforce lifestyle modifications including low-sodium diet and daily walking.\n- Continue current diabetic regimen and recheck HbA1c in 3 months.\n- Schedule blood pressure follow-up in 4 weeks.',
    description: 'Structured bullet outline for the Assessment & Plan section.'
  },
  {
    id: 'follow-up',
    trigger: 'follow-up in',
    completion: ' 4 weeks with home blood pressure log and symptom review.',
    description: 'Finishes a follow-up sentence with clear instructions.'
  }
];
