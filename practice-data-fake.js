/**
 * Fake Practice Data for AI Insights Demo
 * Modify these values to test different scenarios and insights
 */

const PRACTICE_DATA_FAKE = {
  current_period: {
    total_patients: 248,
    new_patients: 42,
    appointments_scheduled: 156,
    appointments_completed: 142,
    appointments_cancelled: 14,
    total_revenue: 89420,
    patient_engagement: 85,
    average_wait_time: 12, // minutes
    provider_utilization: 78, // percentage
    no_show_rate: 5.2 // percentage
  },
  previous_period: {
    total_patients: 234,
    new_patients: 38,
    appointments_scheduled: 148,
    appointments_completed: 135,
    appointments_cancelled: 13,
    total_revenue: 82150,
    patient_engagement: 81,
    average_wait_time: 15,
    provider_utilization: 75,
    no_show_rate: 6.1
  },
  period_comparison: {
    total_patients_change: 6.0,
    new_patients_change: 10.5,
    revenue_change: 8.9,
    engagement_change: 4.9,
    wait_time_change: -20.0,
    utilization_change: 4.0,
    no_show_change: -14.8
  },
  top_services: [
    { name: "Annual Checkup", count: 45, revenue: 22500 },
    { name: "Lab Tests", count: 62, revenue: 18600 },
    { name: "Follow-up Visit", count: 38, revenue: 11400 }
  ],
  peak_hours: ["9:00 AM - 11:00 AM", "2:00 PM - 4:00 PM"],
  provider_performance: [
    { name: "Dr. Wilson", appointments: 78, satisfaction: 4.8 },
    { name: "Dr. Chen", appointments: 64, satisfaction: 4.9 }
  ]
};
