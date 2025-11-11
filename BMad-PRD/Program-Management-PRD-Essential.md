# Program Management - Essential PRD

## Overview
Program Management transforms active workflows into billable care programs with enrollment tracking, milestone monitoring, and payment management. A program is essentially a workflow enhanced with business and clinical tracking capabilities.

## Core Requirements

### 1. Program Settings Tab (Workflow Composer)
- **Location**: New tab "Program Settings" parallel to Log tab
- **Activation**:
  - Tab only enabled when workflow status is "Active"
  - "Convert to Program" toggle only functional when:
    - Workflow is active AND
    - No patients are currently assigned to the workflow
- **Conversion Behavior**:
  - Modifies existing workflow (does not create copy)
  - Adds program configuration layer to workflow
  - Can be reverted only when no patients are enrolled in program

### 2. Program Configuration Fields

#### Basic Information
- **Program Name**: Shares the same field as workflow name - editing one automatically updates the other
- **Program Description**: Shares the same field as workflow description - editing one automatically updates the other
- **Note**: When converted to program, program name/description and workflow name/description are synchronized

#### Program Type & Duration
- **Type Selection**: Rolling or Fixed
  - **Fixed Type**: Requires Start Date and End Date
  - **Rolling Type**: Requires Program Length (number + unit: days/weeks/months)

#### Enrollment Control
- **Max Enrollment**: Optional capacity limit
- **No waitlist functionality**

#### Program Pricing
- **Payment Models**:
  - **One-Time**: Single payment amount
  - **Recurring**:
    - Payment amount per cycle
    - Payment frequency (weekly/monthly/quarterly)
    - End after X number of payments (not end date)
- **Total Transaction Value Reference**: Auto-calculated sum of all transaction amounts in workflow blocks (display only as suggested program cost, user can override)

### 3. Program Monitor Settings

#### Milestone Configuration
- **Milestone Interaction Model**:
  - **Insert Milestones**: User inserts milestone markers between workflow steps (not selecting steps themselves)
  - **Default Milestones**: "Program Start" and "Program End" milestones automatically created at beginning and end
  - **Rename Capability**: All milestones (including defaults) can be renamed inline
  - **Visual Workflow Canvas**: Embedded simplified workflow view showing blocks with "Insert Milestone" buttons between blocks
- **Milestone Data Structure**: `{milestones: [{name: string, position: number}]}`
  - `position`: Indicates where in the workflow timeline the milestone sits (e.g., between block 2 and 3)

#### Progress Chart (Preview)
- **Chart Design**: Match the Medical History chart from My Patient page (see reference screenshot)
- **Structure**:
  - Horizontal timeline showing milestone phases as colored semi-circular sections
  - Y-axis label: "PATIENT INTERACTIONS" (rotated vertical text)
  - Each milestone section displays:
    - Milestone name (e.g., "Baseline Testing", "Results Debrief", "Training Sprint")
    - Touchpoint count and date range (e.g., "5 touchpoints • Apr 1 – Apr 7")
    - Date marker below (e.g., "APR 1")
  - Current progress indicator: Vertical line showing "Today • Week 8"
  - Progress completion text at top (e.g., "66% complete • Next check-in Jun 18, 2025")
- **Colors**: Different colors for each milestone phase (gray, blue, green, orange, etc.)
- **Display Mode**: Preview only in composer; live version appears in My Patient > Medical Record tab

#### Progress Calculation
- Track completed steps vs total steps within each milestone timeframe
- No alerts/notifications for milestone delays (MVP)

### 4. Program Assignment Management

#### Enhanced Assignment Modal
- **Reuse**: Existing assignment modal from workflow composer
- **Visual Enhancement**: Program-specific header/badge to distinguish from regular workflow assignments
- **Display Fields**:
  - Program metadata: name, type, start/end dates, length, price
  - Per-patient enrollment data: enrollment date, current progress
  - Payment status: paid/pending/overdue for each assigned patient
- **Sorting**: Column header sorting (triangle icons) - no filters needed
- **Bulk Operations**: Not supported in MVP

### 5. Integration Points

#### Patient Profile (My Patients - Medical Tab)
- Program progress chart displays in existing Medical Record tab
- Use existing quick action button for enrollment actions
- No additional UI changes needed

#### eZ-Bill (Healthcare Provider Workbench)
- Programs appear in eZ-Bill tab under "Signature Program" section
- Listed as sellable items with program pricing
- Visual integration only (no real payment processing in MVP)

#### Data Architecture
- **Storage**: Programs stored separately from workflows
- **Structure**: `Program = Workflow Reference + Program Configuration`
- **Enrollment Tracking**: Per-patient enrollment records with progress/milestone history
- **Data Model**:
```javascript
Program {
  id: string
  workflowId: string // reference to base workflow
  isProgram: boolean
  programConfig: {
    name: string
    description: string
    type: 'rolling' | 'fixed'
    duration: {
      startDate?: date // for fixed
      endDate?: date // for fixed
      length?: number // for rolling
      unit?: 'days' | 'weeks' | 'months' // for rolling
    }
    enrollment: {
      maxCapacity?: number
    }
    pricing: {
      model: 'one-time' | 'recurring'
      amount: number
      recurring?: {
        frequency: 'weekly' | 'monthly' | 'quarterly'
        paymentCount: number // end after X payments
      }
      totalTransactionValue: number // auto-calculated from workflow transaction blocks
    }
    milestones: Array<{
      name: string
      stepIds: string[] // workflow block IDs
    }>
  }
  enrollments: Array<{
    patientId: string
    enrolledDate: date
    status: 'active' | 'completed' | 'discontinued'
    progress: {
      completedSteps: string[]
      currentMilestone: number
    }
    payment: {
      status: 'paid' | 'pending' | 'overdue'
      lastPaymentDate?: date
      nextPaymentDate?: date
    }
  }>
}
```

## Implementation Decisions Summary

### 1. Program Conversion
- ✅ Convert workflow to program modifies original (no copy)
- ✅ Only active workflows with zero patient assignments can be converted
- ✅ Programs can revert to workflows only when enrollment count = 0

### 2. Pricing Models
- ✅ One-time payment supported
- ✅ Recurring payment with frequency (weekly/monthly/quarterly) and payment count (end after X payments)
- ❌ Milestone-based payment (out of scope)

### 3. Enrollment & Capacity
- ✅ Max enrollment capacity setting
- ❌ Waitlist functionality (out of scope)
- ❌ Bulk enrollment (out of scope)

### 4. Milestone Tracking
- ✅ Manual selection via embedded workflow canvas
- ❌ AI-suggested milestones (out of scope)
- ❌ Automated alerts for delays (out of scope)

### 5. UI Enhancements
- ✅ Assignment modal with sorting (column headers)
- ❌ Filters for payment/enrollment status (out of scope)
- ✅ Program progress chart in Patient Medical Tab (already exists as demo)

### 6. Integration Scope (MVP)
- ✅ Workflow Composer: Full program settings implementation
- ✅ Patient Profile: Use existing Medical Tab chart demo
- ❌ My Practice Dashboard: Program overview (future consideration for My Workbench)
- ❌ Program Templates: (out of scope for MVP)
- ❌ Workflow Block Enhancements: Program-aware conditional blocks (too complex)
- ✅ eZ-Bill Integration: Visual only, programs listed under Signature Program section

### 7. Technical Architecture
- ✅ Programs stored separately as `Program = Workflow Reference + Program Config`
- ✅ Enrollment tracking with progress and payment status per patient
- ✅ Milestone completion history

## Out of Scope for MVP
- Waitlist functionality
- Bulk patient enrollment
- Advanced filters (only column sorting supported)
- AI-suggested milestones
- Automated milestone delay alerts/notifications
- Program templates library
- My Practice Dashboard program overview (future: My Workbench)
- Program-aware workflow blocks and conditional logic
- Real billing system integration (visual only)
- Milestone-based payment models

## Implementation Plan

### Phase 1: Workflow Composer - Program Settings Tab
1. Add "Program Settings" tab next to Log tab
2. Implement program conversion toggle with validation (active + zero assignments)
3. Build program configuration form:
   - Basic info fields (name, description)
   - Type selector (Rolling/Fixed) with conditional date/length fields
   - Enrollment control (max capacity input)
   - Pricing section with payment model selector
   - System-suggested amount calculator

### Phase 2: Milestone Configuration
1. Create embedded workflow canvas component for milestone selection
2. Implement click-to-add milestone interaction
3. Build milestone list manager (add/remove/rename)
4. Create progress chart preview using existing Signature Program chart

### Phase 3: Enhanced Assignment Modal
1. Extend existing assignment modal with program detection
2. Add program-specific header/badge
3. Display program metadata section
4. Add enrollment data columns (enrollment date, progress %)
5. Add payment status columns with sorting
6. Implement column header sorting for all columns

### Phase 4: Data Layer
1. Create program data structure in localStorage/sessionStorage
2. Implement program CRUD operations
3. Build enrollment tracking system
4. Create progress calculation logic (completedSteps/totalSteps)

### Phase 5: Integration (Visual Only)
1. Link program to existing Medical Tab chart in Patient Profile
2. Add programs to eZ-Bill Signature Program section
3. Update quick action buttons to support program enrollment

## Success Criteria
- ✅ Active workflows can be converted to programs
- ✅ Program settings persist and load correctly
- ✅ Milestones can be selected via workflow canvas
- ✅ Progress chart displays correctly in preview and patient profile
- ✅ Assignment modal shows program data with sortable columns
- ✅ Programs appear in eZ-Bill section
- ✅ No console errors, responsive design maintained