window.WORKFLOW_TEMPLATE_DATA = {
  "schema": {
    "version": "1.0",
    "description": "Healthcare workflow template schema",
    "structure": {
      "templates": {
        "id": "string - unique identifier for the template",
        "name": "string - display name for the template",
        "description": "string - brief description of what the workflow does",
        "type": "string - 'patient' or 'practice' workflow type",
        "rating": "number - star rating from 1-5",
        "category": "string - workflow category",
        "tags": "array - searchable tags",
        "blocks": "array - workflow blocks with configuration",
        "connections": "array - connections between blocks",
        "metadata": "object - additional template information"
      }
    }
  },
  "templates": [
    {
      "id": "test-reminder-90day",
      "name": "90-Day Test Reminder",
      "description": "Automated reminder workflow for follow-up testing after order placement",
      "type": "patient",
      "rating": 4.8,
      "category": "Follow-up Care",
      "tags": ["testing", "reminders", "follow-up", "orders"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-order-events",
          "config": {
            "title": "Order Placed",
            "description": "Triggered when a new order is created",
            "icon": "ri-shopping-cart-line",
            "color": "teal"
          },
          "data": {
            "triggerEvents": ["order-created"],
            "conditions": {
              "orderType": "lab-test",
              "status": "active"
            }
          }
        },
        {
          "id": "block-2",
          "type": "wait",
          "config": {
            "title": "Wait 90 Days",
            "description": "Delay workflow execution for 90 days",
            "icon": "ri-timer-line",
            "color": "gray"
          },
          "data": {
            "duration": 90,
            "unit": "days",
            "businessDaysOnly": false
          }
        },
        {
          "id": "block-3",
          "type": "condition",
          "config": {
            "title": "Check Order Status",
            "description": "Verify if follow-up testing is still needed",
            "icon": "ri-git-branch-line",
            "color": "purple"
          },
          "data": {
            "prompt": "Check if the original order has been completed or if follow-up testing is still required",
            "paths": [
              {
                "prompt": "Continue if follow-up testing is still needed",
                "nextBlockId": "block-4"
              }
            ]
          }
        },
        {
          "id": "block-4",
          "type": "send-message",
          "config": {
            "title": "Send Test Reminder",
            "description": "Send reminder message to patient",
            "icon": "ri-message-line",
            "color": "blue"
          },
          "data": {
            "messageType": "sms",
            "template": "Hello! This is a friendly reminder that your follow-up testing is due. Please contact our office to schedule your appointment.",
            "channels": ["sms", "email"],
            "priority": "normal"
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        },
        {
          "from": "block-2",
          "to": "block-3",
          "type": "direct"
        },
        {
          "from": "block-3",
          "to": "block-4",
          "type": "conditional",
          "condition": "follow-up-needed"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "90+ days",
        "complexity": "medium",
        "useCase": "Patient follow-up and care coordination"
      }
    },
    {
      "id": "annual-wellness-visit",
      "name": "Annual Wellness Visit",
      "description": "Standard wellness check workflow with pre-visit prep and follow-up",
      "type": "patient",
      "rating": 4.8,
      "category": "Preventive Care",
      "tags": ["wellness", "annual", "preventive", "screening"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-appointment-events",
          "config": {
            "title": "Wellness Visit Scheduled",
            "description": "Triggered when annual wellness visit is scheduled",
            "icon": "ri-calendar-event-line",
            "color": "green"
          },
          "data": {
            "triggerEvents": ["appointment-created"],
            "conditions": {
              "appointmentType": "annual-wellness",
              "status": "scheduled"
            }
          }
        },
        {
          "id": "block-2",
          "type": "wait",
          "config": {
            "title": "Wait 7 Days Before",
            "description": "Send prep materials one week before visit",
            "icon": "ri-timer-line",
            "color": "gray"
          },
          "data": {
            "duration": -7,
            "unit": "days",
            "relativeTo": "appointment-date"
          }
        },
        {
          "id": "block-3",
          "type": "document",
          "config": {
            "title": "Send Prep Materials",
            "description": "Send pre-visit questionnaire and instructions",
            "icon": "ri-file-text-line",
            "color": "green"
          },
          "data": {
            "documents": ["wellness-questionnaire", "prep-instructions"],
            "deliveryMethod": "patient-portal"
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        },
        {
          "from": "block-2",
          "to": "block-3",
          "type": "direct"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "7-14 days",
        "complexity": "simple",
        "useCase": "Preventive care coordination"
      }
    },
    {
      "id": "diabetes-management",
      "name": "Diabetes Management",
      "description": "Comprehensive diabetes care plan with monitoring and follow-up",
      "type": "patient",
      "rating": 4.7,
      "category": "Chronic Care",
      "tags": ["diabetes", "monitoring", "medication", "chronic-care"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-patient-events",
          "config": {
            "title": "Diabetes Diagnosis",
            "description": "Triggered when patient is diagnosed with diabetes",
            "icon": "ri-user-heart-line",
            "color": "blue"
          },
          "data": {
            "triggerEvents": ["diagnosis-added"],
            "conditions": {
              "diagnosisCode": "E11",
              "status": "active"
            }
          }
        },
        {
          "id": "block-2",
          "type": "task",
          "config": {
            "title": "Schedule Education Session",
            "description": "Create task to schedule diabetes education",
            "icon": "ri-task-line",
            "color": "orange"
          },
          "data": {
            "taskType": "scheduling",
            "assignee": "care-coordinator",
            "priority": "high",
            "dueDate": "+3 days"
          }
        },
        {
          "id": "block-3",
          "type": "wait",
          "config": {
            "title": "Wait 30 Days",
            "description": "Wait for initial adjustment period",
            "icon": "ri-timer-line",
            "color": "gray"
          },
          "data": {
            "duration": 30,
            "unit": "days"
          }
        },
        {
          "id": "block-4",
          "type": "send-message",
          "config": {
            "title": "Follow-up Check",
            "description": "Send follow-up message for monitoring",
            "icon": "ri-message-line",
            "color": "blue"
          },
          "data": {
            "messageType": "automated-call",
            "template": "This is a follow-up call to check on your diabetes management. Please contact us if you have any concerns.",
            "channels": ["phone", "sms"]
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        },
        {
          "from": "block-2",
          "to": "block-3",
          "type": "status-based",
          "condition": "task-completed"
        },
        {
          "from": "block-3",
          "to": "block-4",
          "type": "direct"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "30+ days",
        "complexity": "high",
        "useCase": "Chronic disease management"
      }
    },
    {
      "id": "new-patient-onboarding",
      "name": "New Patient Onboarding",
      "description": "Patient onboarding workflow with welcome messages and first appointment scheduling",
      "type": "patient",
      "rating": 4.9,
      "category": "Patient Engagement",
      "tags": ["onboarding", "welcome", "appointment", "patient-engagement"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-new-patient",
          "config": {
            "title": "New Patient Created",
            "description": "Triggered when new patient profile is created",
            "icon": "ri-user-add-line",
            "color": "purple"
          },
          "data": {
            "triggerEvents": ["patient-created"]
          }
        },
        {
          "id": "block-2",
          "type": "send-message",
          "config": {
            "title": "Welcome Message",
            "description": "Send welcome message to new patient",
            "icon": "ri-message-3-line",
            "color": "green"
          },
          "data": {
            "messageType": "email",
            "template": "Welcome to our practice! Here are some resources to get started.",
            "channels": ["email", "sms"],
            "priority": "normal"
          }
        },
        {
          "id": "block-3",
          "type": "task",
          "config": {
            "title": "Schedule First Appointment",
            "description": "Follow-up task to schedule initial appointment",
            "icon": "ri-calendar-line",
            "color": "blue"
          },
          "data": {
            "taskType": "scheduling",
            "assignee": "front-desk",
            "priority": "high",
            "dueDate": "+2 days"
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        },
        {
          "from": "block-2",
          "to": "block-3",
          "type": "direct"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "1-3 days",
        "complexity": "simple",
        "useCase": "Patient onboarding"
      }
    },
    {
      "id": "lab-follow-up",
      "name": "Lab Results Follow-up",
      "description": "Workflow to monitor lab results and trigger follow-ups for abnormal findings",
      "type": "patient",
      "rating": 4.6,
      "category": "Clinical Care",
      "tags": ["lab", "results", "follow-up", "alerts"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-report-events",
          "config": {
            "title": "Lab Result Posted",
            "description": "Triggered when new lab result is posted",
            "icon": "ri-flask-line",
            "color": "red"
          },
          "data": {
            "triggerEvents": ["report-created"],
            "conditions": {
              "reportType": "lab-result"
            }
          }
        },
        {
          "id": "block-2",
          "type": "condition",
          "config": {
            "title": "Check Result Flag",
            "description": "Check if result flagged as abnormal",
            "icon": "ri-alert-line",
            "color": "red"
          },
          "data": {
            "prompt": "Check if the lab result is outside normal ranges",
            "paths": [
              {
                "prompt": "If critical flag is true",
                "nextBlockId": "block-3"
              },
              {
                "prompt": "If result needs provider review",
                "nextBlockId": "block-4"
              }
            ]
          }
        },
        {
          "id": "block-3",
          "type": "send-message",
          "config": {
            "title": "Notify Provider",
            "description": "Send urgent alert to provider",
            "icon": "ri-alert-fill",
            "color": "red"
          },
          "data": {
            "messageType": "sms",
            "template": "Critical lab result flagged. Immediate review required.",
            "channels": ["sms", "email"],
            "priority": "high"
          }
        },
        {
          "id": "block-4",
          "type": "task",
          "config": {
            "title": "Schedule Follow-up Appointment",
            "description": "Schedule follow-up based on lab result",
            "icon": "ri-calendar-check-line",
            "color": "orange"
          },
          "data": {
            "taskType": "scheduling",
            "assignee": "care-coordinator",
            "priority": "high",
            "dueDate": "+1 days"
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        },
        {
          "from": "block-2",
          "to": "block-3",
          "type": "conditional",
          "condition": "critical-flag-true"
        },
        {
          "from": "block-3",
          "to": "block-4",
          "type": "direct"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "Immediate",
        "complexity": "medium",
        "useCase": "Critical result management"
      }
    },
    {
      "id": "overdue-payment-escalation",
      "name": "Overdue Payment Escalation",
      "description": "Automated escalation workflow for failed payments with reminder and billing follow-up",
      "type": "practice",
      "rating": 4.5,
      "category": "Billing Management",
      "tags": ["payment", "billing", "escalation", "reminders"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-order-events",
          "config": {
            "title": "Payment Failed",
            "description": "Triggered when order payment fails",
            "icon": "ri-error-warning-line",
            "color": "red"
          },
          "data": {
            "triggerEvents": ["order-updated"],
            "conditions": {
              "paymentStatus": "failed",
              "orderStatus": "active"
            }
          }
        },
        {
          "id": "block-2",
          "type": "wait",
          "config": {
            "title": "Wait 24 Hours",
            "description": "Allow 24-hour grace period",
            "icon": "ri-timer-line",
            "color": "gray"
          },
          "data": {
            "duration": 24,
            "unit": "hours"
          }
        },
        {
          "id": "block-3",
          "type": "send-message",
          "config": {
            "title": "Payment Reminder",
            "description": "Send payment reminder to patient",
            "icon": "ri-money-dollar-circle-line",
            "color": "orange"
          },
          "data": {
            "messageType": "email",
            "template": "Your recent payment was unsuccessful. Please update your payment method or contact our billing department to resolve this issue.",
            "channels": ["email", "sms"],
            "priority": "normal"
          }
        },
        {
          "id": "block-4",
          "type": "task",
          "config": {
            "title": "Billing Follow-up",
            "description": "Assign billing follow-up if still unpaid",
            "icon": "ri-task-line",
            "color": "blue"
          },
          "data": {
            "taskType": "billing-follow-up",
            "assignee": "billing-department",
            "priority": "normal",
            "dueDate": "+2 days"
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        },
        {
          "from": "block-2",
          "to": "block-3",
          "type": "direct"
        },
        {
          "from": "block-3",
          "to": "block-4",
          "type": "status-based",
          "condition": "payment-still-failed"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "1-3 days",
        "complexity": "medium",
        "useCase": "Payment and billing management"
      }
    },
    {
      "id": "patient-birthday-greeting",
      "name": "Patient Birthday Greeting",
      "description": "Send a celebratory message on the patient's birthday",
      "type": "patient",
      "rating": 4.9,
      "category": "Patient Engagement",
      "tags": ["birthday", "celebration", "patient-engagement", "automations"],
      "blocks": [
        {
          "id": "block-1",
          "type": "trigger-patient-events",
          "config": {
            "title": "Patient Birthday",
            "description": "Triggered on the patient's birthday",
            "icon": "ri-cake-2-line",
            "color": "pink"
          },
          "data": {
            "triggerEvents": ["patient-birthday"],
            "conditions": {
              "status": "active"
            }
          }
        },
        {
          "id": "block-2",
          "type": "send-message",
          "config": {
            "title": "Send Birthday Message",
            "description": "Deliver a personalized birthday greeting",
            "icon": "ri-mail-send-line",
            "color": "purple"
          },
          "data": {
            "messageType": "email",
            "template": "Happy Birthday, {{patient.first_name}}! We hope you have a wonderful day. Please reach out if there is anything we can do to support your health goals this year.",
            "channels": ["email", "sms"],
            "priority": "normal"
          }
        }
      ],
      "connections": [
        {
          "from": "block-1",
          "to": "block-2",
          "type": "direct"
        }
      ],
      "metadata": {
        "created": "2024-12-20",
        "author": "Healthcare Templates",
        "version": "1.0",
        "estimatedRuntime": "Same day",
        "complexity": "simple",
        "useCase": "Celebrate patient birthdays automatically"
      }
    }
  ]
};
