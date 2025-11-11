# Workflow Frontend Product Requirements Document (PRD)

## Goals and Background Context

### Goals

- Enable healthcare providers to create and manage patient-specific automated workflows without coding
- Provide visual workflow composition with drag-and-drop interface for building automation logic
- Allow testing and validation of workflows before deploying to live patients
- Support AI-assisted workflow creation to accelerate workflow design
- Enable monitoring and tracking of workflow execution with detailed logs
- Provide template library for common healthcare workflows to jumpstart provider productivity
- Ensure workflow integrity with validation before activation and assignment to patients

### Background Context

Healthcare providers spend significant time on repetitive patient communication and care coordination tasks. Manual patient engagement workflows (appointment reminders, lab result notifications, questionnaire follow-ups, care plan adjustments) consume valuable clinical time and can lead to inconsistent patient experiences.

This Workflow Frontend enables providers to automate patient-specific workflows through a visual composer interface. Providers can create custom automation that triggers based on patient events (order status changes, report availability, calendar events, etc.) and executes actions (send messages, assign tasks, update notes, etc.) with conditional logic and AI-assisted decision-making. This automation reduces administrative burden while ensuring consistent, timely patient engagement aligned with each patient's care journey.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-10-06 | v1.0 | Initial PRD draft | John (PM Agent) |

## Requirements

### Functional

**FR1: Workflow Management**
- FR1.1: Users can create new workflows from scratch
- FR1.2: Users can edit existing draft workflows
- FR1.3: Users can duplicate existing workflows with unique naming (auto-append -1, -2, -3, etc.)
- FR1.4: Users can archive workflows that are not assigned and active
- FR1.5: Workflow name is required and must be unique across the practice (auto-append suffix if duplicate)
- FR1.6: Workflow description is optional and supports inline editing with auto-save
- FR1.7: All workflow edits auto-save with 2-second debounce and display save status with timestamp

**FR2: Workflow Entry Points and Navigation**
- FR2.1: Users access workflow composer from MyWorkbench page
- FR2.2: MyWorkbench displays list of existing workflows with status (draft/active)
- FR2.3: MyWorkbench provides archived workflows in separate Archive tab
- FR2.4: MyWorkbench provides "Create New Workflow" action button
- FR2.5: MyWorkbench provides access to Vibrant Intelligence library containing workflow templates
- FR2.6: Workflow composer opens in dedicated view when creating or editing workflows

**FR3: Workflow Composer Interface - Three-Panel Layout**
- FR3.1: Compose tab must display three-panel layout: Block Palette | Canvas | AI Assistant
- FR3.2: Block Palette must provide organized access to all workflow building blocks categorized as TRIGGERS, ACTIONS, and LOGIC
- FR3.3: Block Palette must display blocks with identifying information
- FR3.4: Block Palette must support drag-and-drop of blocks to canvas
- FR3.5: Users must be able to drag and drop multiple blocks to canvas without triggering configuration for each block
- FR3.6: Canvas must provide visual workspace for block placement and connections
- FR3.7: Canvas must support zoom controls with configurable zoom levels
- FR3.8: Canvas must provide auto-layout functionality for organizing blocks
- FR3.9: Canvas must display helpful empty state when no blocks are present
- FR3.10: AI Assistant panel must provide chat interface for workflow creation assistance
- FR3.11: AI Assistant must support message history and text input with keyboard shortcuts
- FR3.12: AI Assistant must support attachment of images and files

**FR4: Block Configuration and States**
- FR4.1: Blocks placed on canvas must be configurable via configuration interface
- FR4.2: Unconfigured blocks must be visually distinct from configured blocks
- FR4.3: Configured blocks must display clear visual confirmation of configuration status
- FR4.4: Blocks must support selection state with visual feedback
- FR4.5: Orphaned blocks (disconnected from workflow) must be clearly identified
- FR4.6: System must provide visual feedback during block drag operations
- FR4.7: Standard blocks and condition blocks must be visually distinguishable
- FR4.8: Blocks must support connections to other blocks through visual connection mechanism
- FR4.9: Connection lines must clearly show direction of workflow flow

**FR5: Block Type Requirements**

_[PLACEHOLDER: This section will contain detailed functional requirements for each block type including Triggers, Actions, and Logic blocks. Requirements will specify the configuration parameters, behavior, and integration points for each block type.]_

**FR6: Trigger Block Restrictions**
- FR6.1: After first trigger block is added to workflow, all other trigger blocks must be disabled
- FR6.2: Users can only configure one trigger per workflow

**FR7: Workflow Activation and Validation**
- FR7.1: Draft workflows must provide activation mechanism
- FR7.2: Activation must trigger validation of entire workflow
- FR7.3: If no successful test run has been executed, system must prompt user to test workflow before activation
- FR7.4: Validation errors must be clearly displayed with identification of problematic blocks
- FR7.5: Successfully validated workflows transition from "Draft" to "Active" status
- FR7.6: Activated workflows must provide update mechanism for modifications
- FR7.7: Workflow errors must be accessible via error reporting interface

**FR8: Patient Assignment and Usage Management**
- FR8.1: System must provide patient assignment interface for workflows
- FR8.2: Users must be able to switch workflow status between "Active" and "Draft"
- FR8.3: Only unassigned workflows can be switched from "Active" to "Draft"
- FR8.4: Users must be able to view list of patients assigned to workflow
- FR8.5: System must support single and batch patient assignment to workflows
- FR8.6: Users must be able to deassign patients from workflows
- FR8.7: Users must be able to pause and resume workflow execution for individual patients
- FR8.8: System must display patient assignment count for workflows
- FR8.9: Active and assigned workflows cannot be switched to draft, updated, or archived until all patients are unassigned

**FR9: Assigned Workflow Monitoring**
- FR9.1: Blocks in assigned workflows must display current patient count in each block
- FR9.2: Users must be able to view list of patients currently in each block

**FR10: Test & Log Interface**
- FR10.1: System must provide test execution interface with dummy patient data
- FR10.2: Test runs must validate trigger conditions
- FR10.3: Test runs must override wait times for faster execution (10 seconds)
- FR10.4: Test execution must display real-time progress and current block status
- FR10.5: Test execution must show block-by-block trace with success/error indicators
- FR10.6: Test runs must support interactive approval actions where applicable
- FR10.7: Test results must display summary with duration, blocks executed, and outcome
- FR10.8: System must provide log viewing interface with separate test and live run logs
- FR10.9: Log interface must support filtering by status, date range, and patient
- FR10.10: Log entries must display timestamp, patient, status, duration, and actions
- FR10.11: Users must be able to view detailed execution trace for each log entry

**FR11: Template Library and Template View Mode**
- FR11.1: Users must be able to access workflow template library
- FR11.2: Templates must be viewable in read-only preview mode
- FR11.3: Template preview must display template metadata (introduction, usage count, ratings)
- FR11.4: Template preview must clearly indicate read-only status
- FR11.5: Users must be able to create editable copy of template to their workbench
- FR11.6: Template blocks must be viewable in read-only configuration mode
- FR11.7: Template preview must support zoom and navigation controls

### Non Functional

**NFR1: Auto-save Performance**
- All workflow edits must auto-save within 2 seconds of last user input to prevent data loss

**NFR2: Validation Response Time**
- Workflow validation must complete within 5 seconds for workflows with up to 50 blocks

**NFR3: Canvas Performance**
- Canvas must support smooth drag-and-drop and zoom operations for workflows with up to 100 blocks without lag

**NFR4: Test Run Execution**
- Test runs must complete within 30 seconds for workflows with up to 20 blocks (with 10-second wait time overrides)

**NFR5: Template Library Load Time**
- Template library must load and display all available templates within 3 seconds

**NFR6: Accessibility**
- Interface must support keyboard navigation for all workflow composition actions

**NFR7: Data Persistence**
- All workflow configurations must persist reliably with no data loss between sessions

## User Interface Design Goals

### Overall UX Vision

The Workflow Composer should feel like a modern visual workflow builder that empowers healthcare providers to create automation without technical expertise. The interface should prioritize clarity, discoverability, and confidence-building through clear visual feedback at every step. Users should feel guided through the workflow creation process with AI assistance available but not intrusive.

The experience should balance powerful functionality with simplicity—making complex automation accessible while preventing configuration errors through smart validation and clear status indicators. The interface should minimize cognitive load by organizing tools logically, providing contextual help, and maintaining visual consistency throughout.

### Key Interaction Paradigms

**Drag-and-Drop Workflow Construction**: Users build workflows by dragging blocks from a library onto a visual canvas and connecting them to define logic flow. This spatial, visual approach makes abstract automation concepts concrete and manipulable.

**Progressive Configuration**: Blocks start in an unconfigured state. Users can rapidly place multiple blocks on canvas without immediate configuration requirement, then configure blocks individually when ready. Visual states guide users through completion, preventing incomplete workflows from being activated.

**Validate-Then-Activate**: Workflows remain in draft mode until explicitly activated, with validation occurring before activation to catch errors early and build user confidence. If no successful test has been run, users are prompted to test before activating.

**Test-First Development**: Users can test workflows with dummy data before assigning to real patients, providing a safe experimentation environment.

**AI-Assisted Creation**: An always-available AI assistant helps users design workflows, suggest blocks, and troubleshoot issues without leaving the composition interface.

**Template-Based Acceleration**: Users can preview and copy proven workflow templates, learning by example and accelerating common use cases.

### Core Screens and Views

**MyWorkbench - Workflow List**: Entry point showing all workflows with status, assignment counts, and quick actions (create, edit, archive). Provides access to template library.

**Workflow Composer - Compose Tab**: Primary creation interface with three-panel layout (Block Palette | Canvas | AI Assistant) for building and editing workflows.

**Workflow Composer - Test & Log Tab**: Testing and monitoring interface with test execution controls and log viewing capabilities.

**Template Preview**: Read-only view of workflow templates with metadata and copy functionality.

**Configuration Modals**: Block-specific configuration interfaces for defining block behavior and parameters.

**Patient Assignment Modal**: Interface for managing workflow-to-patient assignments, status changes, and monitoring.

### Accessibility

WCAG AA compliance for core workflow composition functionality. Keyboard navigation support for all workflow building actions.

### Branding

Healthcare-focused design with clean, professional aesthetic. Interface should convey trustworthiness and clarity appropriate for clinical workflow automation. Visual design should minimize clutter and emphasize workflow logic clarity.

### Target Device and Platforms

Web Responsive - primary focus on desktop/laptop usage for workflow creation (complex workflow design benefits from larger screens), with responsive support for tablet-based monitoring and minor edits.

## Technical Assumptions

### Repository Structure

This is a brownfield project adding workflow frontend capabilities to an existing healthcare communication platform. The workflow composer will integrate into the existing multi-page HTML application structure.

### Service Architecture

Frontend-focused enhancement to existing application. Workflow execution logic, patient data management, and backend integration points are out of scope for this frontend PRD. The frontend will integrate with existing or future backend services for workflow persistence, execution, and patient assignment.

### Testing Requirements

- Unit testing for workflow validation logic and configuration state management
- Integration testing for workflow composer UI interactions (drag-and-drop, block configuration, canvas operations)
- End-to-end testing for complete workflow creation, testing, and activation flows
- Manual testing for AI assistant integration and complex workflow scenarios

### Additional Technical Assumptions and Requests

**Integration Points**:
- Frontend must integrate with existing MyWorkbench/Healthcare Provider Workbench navigation
- Workflow data persistence requires backend API (assumed to be developed separately or as part of architecture phase)
- Patient assignment functionality requires integration with existing patient management system
- Workflow execution engine integration required for test runs and live execution (backend scope)

**Performance Considerations**:
- Canvas rendering must handle workflows with up to 100 blocks efficiently
- Auto-save mechanism must debounce user input appropriately to avoid excessive API calls
- Template library should support lazy loading for large template collections

**Data Model Requirements**:
- Workflow definitions must be serializable for persistence and sharing
- Block configurations must support validation rules to ensure data integrity
- Workflow execution state must be trackable for monitoring and logging

**AI Assistant Integration**:
- AI assistant requires integration with appropriate AI service (specific service selection deferred to technical team)
- Chat interface must handle async responses and error states
- File/image attachment support requires appropriate backend handling

**Browser Compatibility**:
- Target modern browsers (specific version requirements to be defined by technical team)
- Drag-and-drop functionality must work across supported browsers

## Epic List

**Epic 1: Workflow Management Foundation**
Goal: Enable users to create, view, edit, and manage workflow metadata with auto-save, providing the foundational workflow CRUD operations needed for all subsequent workflow composition features.

**Epic 2: Visual Workflow Composer - Block Palette and Canvas**
Goal: Implement the core visual workflow building interface with drag-and-drop block placement, canvas operations, and block connection capabilities, allowing users to spatially construct workflow logic.

**Epic 3: Block Configuration System**
Goal: Enable configuration of workflow blocks through modal interfaces, visual state management for configured/unconfigured blocks, and validation of block configurations.

**Epic 4: Workflow Validation and Activation**
Goal: Implement workflow validation, activation workflow with test-first prompts, status management, and error reporting to ensure workflows are complete before going live.

**Epic 5: Test Execution and Log Viewing**
Goal: Provide workflow testing capabilities with dummy patient data, real-time execution monitoring, and comprehensive log viewing for both test and live workflow runs.

**Epic 6: Patient Assignment and Monitoring**
Goal: Enable assignment of activated workflows to patients, management of patient-workflow relationships, and monitoring of patient progress through workflow blocks.

**Epic 7: Template Library and Preview**
Goal: Provide access to workflow template library, read-only template preview with metadata, and template copying functionality to accelerate workflow creation.

**Epic 8: AI Assistant Integration**
Goal: Integrate AI-powered chat assistant into workflow composer for workflow creation guidance, suggestions, and troubleshooting support.

## Epic 1: Workflow Management Foundation

Enable users to create, view, edit, and manage workflow metadata with auto-save, providing the foundational workflow CRUD operations needed for all subsequent workflow composition features.

### Story 1.1: Workflow List View in MyWorkbench

As a healthcare provider,
I want to view all my workflows in a list with their status and assignment information,
so that I can quickly see what workflows I have and access them for editing or management.

**Acceptance Criteria:**

1. MyWorkbench displays a list of all workflows for the current user/practice
2. Each workflow in the list shows: name, description preview, status (Draft/Active), and assignment count if applicable
3. Workflows are sortable by name, status, and last modified date
4. List provides quick actions: Edit, Duplicate, Archive
5. "Create New Workflow" button is prominently displayed
6. Archived workflows are shown in separate "Archive" tab
7. Clicking a workflow opens it in Workflow Composer
8. Empty state displayed when no workflows exist with helpful guidance to create first workflow

### Story 1.2: Create New Workflow

As a healthcare provider,
I want to create a new workflow from scratch,
so that I can start building custom automation for my patients.

**Acceptance Criteria:**

1. "Create New Workflow" button opens Workflow Composer in new workflow mode
2. New workflow is created with default "Draft" status
3. New workflow has auto-generated unique name (e.g., "Untitled Workflow")
4. New workflow is immediately persisted to backend
5. User is navigated to Workflow Composer with empty canvas
6. Workflow appears in MyWorkbench workflow list after creation

### Story 1.3: Workflow Metadata Editing with Auto-Save

As a healthcare provider,
I want to edit workflow name and description with automatic saving,
so that my changes are preserved without manual save actions.

**Acceptance Criteria:**

1. Workflow name field supports inline editing in Workflow Composer header
2. Workflow description field supports inline editing in Workflow Composer header
3. Name field is required; system prevents empty names
4. Description field is optional
5. Changes auto-save with 2-second debounce after last user input
6. Auto-save indicator displays "Saving..." during save and "Saved" with timestamp after success
7. If name conflicts with existing workflow, system auto-appends suffix (-1, -2, -3, etc.)
8. Auto-save errors are displayed to user with retry option

### Story 1.4: Duplicate Workflow

As a healthcare provider,
I want to duplicate an existing workflow,
so that I can create variations without starting from scratch.

**Acceptance Criteria:**

1. Duplicate action available from workflow list and from within Workflow Composer
2. Duplicating a workflow creates new workflow with all blocks and configurations copied
3. Duplicated workflow has new unique ID
4. Duplicated workflow name is original name with auto-appended suffix (-1, -2, -3, etc.)
5. Duplicated workflow starts in "Draft" status regardless of source workflow status
6. Duplicated workflow has no patient assignments
7. User is notified of successful duplication
8. User can immediately edit duplicated workflow

### Story 1.5: Archive and Restore Workflows

As a healthcare provider,
I want to archive workflows I'm no longer using,
so that my active workflow list stays focused on current workflows.

**Acceptance Criteria:**

1. Archive action available for workflows that are not active and assigned
2. Archived workflows move to "Archive" tab in MyWorkbench
3. Archived workflows are not displayed in main workflow list
4. User can restore archived workflows from Archive tab
5. Restored workflows return to main workflow list with same status they had before archiving
6. System prevents archiving of active and assigned workflows with clear error message
7. Archive action requires confirmation to prevent accidental archiving

## Epic 2: Visual Workflow Composer - Block Palette and Canvas

Implement the core visual workflow building interface with drag-and-drop block placement, canvas operations, and block connection capabilities, allowing users to spatially construct workflow logic.

### Story 2.1: Block Palette Display

As a healthcare provider,
I want to see all available workflow blocks organized by category,
so that I can discover and select blocks to add to my workflow.

**Acceptance Criteria:**

1. Block Palette displays in left panel of Workflow Composer Compose tab
2. Blocks organized in collapsible categories: TRIGGERS, ACTIONS, LOGIC
3. Each block shows: icon, block name, and brief description on hover
4. Categories can be collapsed/expanded independently
5. Block Palette is scrollable when content exceeds panel height
6. Block icons are color-coded by category for visual distinction
7. Palette displays placeholder message if no blocks available in category

### Story 2.2: Drag-and-Drop Block Placement

As a healthcare provider,
I want to drag blocks from the palette onto the canvas,
so that I can build my workflow visually.

**Acceptance Criteria:**

1. Users can click and drag blocks from Block Palette to Canvas
2. During drag, block appears elevated with visual feedback (shadow, rotation, scale)
3. Canvas highlights valid drop zones during drag operation
4. Dropping block on canvas places block at drop location
5. Multiple blocks can be placed without triggering configuration modals
6. Newly placed blocks appear in unconfigured state
7. Block placement is immediately persisted via auto-save
8. Invalid drop locations (outside canvas) cancel the drag operation

### Story 2.3: Canvas with Grid and Empty State

As a healthcare provider,
I want a clear visual workspace for building workflows,
so that I can organize my workflow blocks spatially.

**Acceptance Criteria:**

1. Canvas displays in center panel with grid pattern background
2. Empty canvas shows helpful message: "Start building your workflow. Drag blocks from the left panel to begin. Or open a template from the template library."
3. Canvas is scrollable when workflow extends beyond visible area
4. Canvas provides sufficient space for large workflows (supports 100+ blocks)
5. Grid provides visual reference for block placement
6. Canvas background and grid are visually subtle to not compete with workflow content

### Story 2.4: Canvas Zoom Controls

As a healthcare provider,
I want to zoom in and out of the workflow canvas,
so that I can view details or see the entire workflow at once.

**Acceptance Criteria:**

1. Zoom controls displayed in top-right corner of canvas: Zoom Out (-), Zoom % display, Zoom In (+)
2. Zoom range: 25% to 200%
3. Zoom In button increases zoom by 25% increments up to 200%
4. Zoom Out button decreases zoom by 25% increments down to 25%
5. Clicking zoom percentage resets to 100%
6. Zoom level persists during session but resets to 100% on reload
7. All canvas elements (blocks, connections) scale appropriately with zoom
8. Zoom controls are always visible regardless of scroll position

### Story 2.5: Block Connection System

As a healthcare provider,
I want to connect workflow blocks to define the flow of automation,
so that I can create multi-step workflows.

**Acceptance Criteria:**

1. Each block displays connection handle (red circular "+" button) at bottom
2. Clicking connection handle initiates connection mode
3. In connection mode, user can click target block to create connection
4. Connection lines render as curved Bézier paths with directional arrows
5. Connection lines clearly show direction of workflow flow
6. Users can delete connections by clicking connection line and selecting delete
7. Connections are validated to prevent cycles in workflow logic
8. Block connections are immediately persisted via auto-save
9. Visual feedback indicates valid vs invalid connection targets during connection mode

### Story 2.6: Auto-Layout for Workflow Organization

As a healthcare provider,
I want to automatically organize my workflow blocks in a clean layout,
so that complex workflows remain readable without manual positioning.

**Acceptance Criteria:**

1. Auto-Layout button displayed in top-right of canvas
2. Clicking Auto-Layout applies hierarchical tree layout to all blocks
3. Layout algorithm positions blocks based on connections (trigger at top, flowing downward)
4. Condition blocks and branches are positioned appropriately
5. Auto-Layout preserves all connections and block configurations
6. Layout operation completes within 2 seconds for workflows with up to 100 blocks
7. User can undo auto-layout if desired
8. Auto-Layout respects block groupings and logical flow

## Epic 3: Block Configuration System

Enable configuration of workflow blocks through modal interfaces, visual state management for configured/unconfigured blocks, and validation of block configurations.

### Story 3.1: Block Configuration Modal Trigger

As a healthcare provider,
I want to configure blocks I've placed on the canvas,
so that I can define their specific behavior and parameters.

**Acceptance Criteria:**

1. Unconfigured blocks display "Configure" button when hovered or selected
2. Clicking "Configure" button opens configuration modal for that block type
3. Modal displays centered on screen with overlay dimming background
4. Modal shows block icon, block type name, and configuration form
5. Modal provides "Cancel" and "Save Configuration" buttons
6. Clicking Cancel closes modal without saving changes
7. Clicking outside modal closes without saving (with confirmation if changes made)
8. Modal is keyboard accessible (Tab navigation, Esc to close)

### Story 3.2: Block Visual States

As a healthcare provider,
I want to see which blocks are configured and which need setup,
so that I know what work remains to complete my workflow.

**Acceptance Criteria:**

1. Unconfigured blocks display orange indicator with pulsing glow effect
2. Unconfigured blocks show "⚙️ Needs Setup" badge
3. Configured blocks display green checkmark "✓ Configured" badge
4. Block selection state shows highlighted border and elevated appearance
5. Orphaned blocks (disconnected from workflow) show reduced opacity and "⚠️ DISCONNECTED" warning
6. Visual states are mutually exclusive except orphaned state which can combine with others
7. State changes are immediately reflected on canvas
8. State indicators are visible at all zoom levels

### Story 3.3: Block Configuration Persistence

As a healthcare provider,
I want my block configurations to be saved automatically,
so that I don't lose my work if I navigate away.

**Acceptance Criteria:**

1. Saving block configuration via modal triggers auto-save of entire workflow
2. Configuration changes are persisted to backend within 2 seconds
3. Configuration is preserved when workflow is closed and reopened
4. Auto-save indicator updates after configuration save
5. Failed saves display error message with retry option
6. Block state updates from unconfigured to configured after successful save
7. Configuration data is validated before persisting

### Story 3.4: Block Deletion

As a healthcare provider,
I want to delete blocks from my workflow,
so that I can remove blocks I no longer need.

**Acceptance Criteria:**

1. Selected blocks provide "Delete" action button or context menu option
2. Deleting block requires confirmation to prevent accidental deletion
3. Deleting block removes it from canvas and all its connections
4. Connected blocks show orphaned state if deletion breaks workflow continuity
5. Block deletion is immediately persisted via auto-save
6. Deleted blocks can be restored via undo action (session-only)
7. Deleting trigger block re-enables all trigger blocks in Block Palette

## Epic 4: Workflow Validation and Activation

Implement workflow validation, activation workflow with test-first prompts, status management, and error reporting to ensure workflows are complete before going live.

### Story 4.1: Trigger Block Restriction

As a healthcare provider,
I want to be limited to one trigger per workflow,
so that my workflows have a single clear starting point.

**Acceptance Criteria:**

1. After first trigger block is placed on canvas, all other trigger blocks in Block Palette are disabled
2. Disabled trigger blocks display lock icon overlay
3. Hovering over disabled trigger shows tooltip: "Only one trigger allowed per workflow"
4. Deleting the trigger block re-enables all trigger blocks in Block Palette
5. Attempting to drag disabled trigger block shows not-allowed cursor
6. Trigger restriction is enforced even if user attempts to paste or duplicate trigger

### Story 4.2: Workflow Validation Engine

As a healthcare provider,
I want my workflow validated before activation,
so that I can catch configuration errors before workflows go live.

**Acceptance Criteria:**

1. Validation checks: all blocks are configured, all blocks are connected (no orphans), one trigger exists, no circular logic
2. Validation runs when user clicks "Activate Workflow" button
3. Validation results clearly identify which blocks have issues
4. Validation errors prevent workflow activation
5. Validation error summary displayed with count of errors and list of problematic blocks
6. Clicking error in list highlights corresponding block on canvas
7. Validation passes only when all checks succeed
8. Validation runs in under 5 seconds for workflows with up to 50 blocks

### Story 4.3: Test-First Activation Flow

As a healthcare provider,
I want to be prompted to test my workflow before activating,
so that I ensure it works correctly before assigning to patients.

**Acceptance Criteria:**

1. When user clicks "Activate Workflow" on workflow with no successful test runs, system displays prompt
2. Prompt message: "This workflow hasn't been tested yet. We recommend running a test before activating. Would you like to test now?"
3. Prompt provides options: "Run Test", "Activate Anyway", "Cancel"
4. Clicking "Run Test" navigates to Test & Log tab with test controls ready
5. Clicking "Activate Anyway" proceeds with validation and activation
6. Clicking "Cancel" closes prompt without activating
7. If workflow has successful test run in history, prompt is skipped
8. Test requirement prompt appears after validation passes, not before

### Story 4.4: Workflow Activation and Status Management

As a healthcare provider,
I want to activate my validated workflow,
so that it becomes available for assignment to patients.

**Acceptance Criteria:**

1. Draft workflows display "Activate Workflow" button in header
2. Clicking "Activate Workflow" triggers validation followed by optional test prompt
3. If validation passes and user proceeds, workflow status changes from "Draft" to "Active"
4. "Activate Workflow" button is replaced by "Update Workflow" button after activation
5. Active status badge is displayed in workflow header
6. Activated workflows can still be edited (configuration changes only, structure changes require re-validation)
7. "Update Workflow" triggers re-validation before applying changes to active workflow
8. Status change is immediately persisted

### Story 4.5: Workflow Error Reporting

As a healthcare provider,
I want to see detailed information about workflow errors,
so that I can fix issues preventing activation.

**Acceptance Criteria:**

1. When workflow has validation errors, "Error" badge appears in header with error count
2. Clicking error badge opens error details modal
3. Error details modal lists all errors with: error type, block name/location, description, suggested fix
4. Each error in list is clickable to highlight corresponding block on canvas
5. Error modal provides "Fix Issues" action that closes modal and focuses first error block
6. Error badge disappears once all errors are resolved
7. Errors are categorized by severity: blocking (prevents activation) vs warnings (allows activation with confirmation)

## Epic 5: Test Execution and Log Viewing

Provide workflow testing capabilities with dummy patient data, real-time execution monitoring, and comprehensive log viewing for both test and live workflow runs.

### Story 5.1: Test & Log Tab Interface

As a healthcare provider,
I want to access workflow testing and logging in a dedicated interface,
so that I can validate and monitor my workflows.

**Acceptance Criteria:**

1. Workflow Composer provides "Test & Log" tab alongside "Compose" tab
2. Test & Log tab displays full-width interface (no Block Palette or AI Assistant panels)
3. Tab contains sub-tabs: "Test Run" (default) and "Log View"
4. Switching tabs preserves workflow composer state
5. Tab navigation is clear and accessible
6. Tab content loads efficiently on first access

### Story 5.2: Test Run Execution with Dummy Patient

As a healthcare provider,
I want to run my workflow with dummy patient data,
so that I can see how it will execute without affecting real patients.

**Acceptance Criteria:**

1. Test Run sub-tab displays "Run with Dummy Patient" button as primary action
2. Clicking button initiates test execution with dummy patient data
3. System checks trigger condition to determine workflow start
4. System displays message: "All waiting times changed to 10 seconds for test run"
5. Test execution proceeds through workflow blocks sequentially
6. Test status area shows: progress indicator, current block being executed, elapsed time
7. Test completes when workflow reaches end or encounters error
8. Test results are logged for review in Log View

### Story 5.3: Real-Time Test Execution Monitoring

As a healthcare provider,
I want to see my workflow execute in real-time during testing,
so that I understand how it flows and can identify issues.

**Acceptance Criteria:**

1. During test execution, currently executing block is highlighted on timeline/trace
2. Block-by-block execution trace displays with checkmarks for completed blocks
3. Errors during execution display error icon and error message
4. Execution timeline shows timing information for each block
5. Test can be stopped/cancelled by user mid-execution
6. Execution monitoring updates in real-time (no manual refresh needed)
7. Visual feedback clearly distinguishes passed vs failed blocks

### Story 5.4: Interactive Test Execution for Approval Blocks

As a healthcare provider,
I want to interact with approval blocks during test runs,
so that I can test workflows requiring human decisions.

**Acceptance Criteria:**

1. When test execution reaches approval/decision block, execution pauses
2. Test interface displays Approve/Reject buttons for approval blocks
3. Clicking Approve continues workflow on approval path
4. Clicking Reject continues workflow on rejection path
5. Approval interactions are logged in test execution trace
6. Timeout behavior is respected during test (with 10-second override)
7. User can see impact of different approval decisions by re-running test

### Story 5.5: Test Results Summary

As a healthcare provider,
I want to see a summary of test execution results,
so that I can quickly assess if my workflow is working correctly.

**Acceptance Criteria:**

1. After test completes, test results summary displays
2. Summary shows: success/failure status, total duration, number of blocks executed, final outcome
3. If test failed, summary highlights error block and error message
4. Summary provides "View Full Trace" link to detailed execution log
5. Summary provides "Run Again" button to re-execute test
6. Successful test run is recorded for workflow activation eligibility
7. Summary is persistent (remains visible after execution completes)

### Story 5.6: Log View Interface with Filtering

As a healthcare provider,
I want to view logs of workflow executions with filtering options,
so that I can review test and live workflow runs.

**Acceptance Criteria:**

1. Log View sub-tab contains nested tabs: "Test Runs" and "Live Runs"
2. Log interface displays filter controls: status dropdown (All/Success/Failed), date range selector, patient search
3. Log table displays columns: Timestamp, Patient, Status, Duration, Actions
4. Logs are sorted by timestamp (most recent first) by default
5. Filtering updates log table immediately without page reload
6. Log table is paginated for large result sets
7. Empty state displayed when no logs match filters

### Story 5.7: Detailed Log Execution Trace

As a healthcare provider,
I want to view detailed execution trace for any workflow run,
so that I can troubleshoot issues and understand workflow behavior.

**Acceptance Criteria:**

1. Each log entry provides "View" action in Actions column
2. Clicking "View" opens detail modal showing full execution trace
3. Execution trace shows: each block executed, block execution duration, block inputs/outputs, decisions made
4. Failed executions show error details with stack trace and error analysis
5. Trace displays in chronological order with timeline visualization
6. Modal provides "Download Log" option for detailed analysis
7. Modal is scrollable for long execution traces

## Epic 6: Patient Assignment and Monitoring

Enable assignment of activated workflows to patients, management of patient-workflow relationships, and monitoring of patient progress through workflow blocks.

### Story 6.1: Patient Assignment Interface

As a healthcare provider,
I want to assign activated workflows to specific patients,
so that automated workflows execute for those patients.

**Acceptance Criteria:**

1. "Manage Usage" button displayed in workflow header
2. Clicking "Manage Usage" opens patient assignment modal
3. Modal displays list of currently assigned patients with: name, assignment date, current block, status (active/paused)
4. Modal provides "Assign Patient" action button
5. Assign action opens patient selection interface with search
6. Selected patients are immediately assigned to workflow
7. Assignment is persisted and reflected in patient list
8. Only active workflows can have patient assignments

### Story 6.2: Batch Patient Assignment

As a healthcare provider,
I want to assign multiple patients to a workflow at once,
so that I can efficiently deploy workflows to patient cohorts.

**Acceptance Criteria:**

1. Patient assignment interface supports multi-select
2. Batch assignment action assigns all selected patients simultaneously
3. Assignment progress indicator shown for large batches
4. Successfully assigned patients appear in assigned patient list
5. Failures during batch assignment are reported individually with reasons
6. Partial success (some assignments succeed, some fail) is handled gracefully
7. Batch assignment completes within reasonable time for up to 100 patients

### Story 6.3: Patient Deassignment and Pause/Resume

As a healthcare provider,
I want to deassign patients or pause their workflows,
so that I can stop automation when needed without losing progress.

**Acceptance Criteria:**

1. Each patient in assignment list provides actions: Pause, Resume, Deassign
2. Pause action stops workflow execution for that patient without removing assignment
3. Resume action restarts paused workflow from current block
4. Deassign action removes patient from workflow with confirmation
5. Deassigned patients' workflow progress is archived for reference
6. Paused status is clearly indicated in patient list
7. Deassignment is immediate and irreversible (with confirmation)

### Story 6.4: Workflow Assignment Count Display

As a healthcare provider,
I want to see how many patients are assigned to each workflow,
so that I can understand workflow utilization at a glance.

**Acceptance Criteria:**

1. Workflow header displays "Assigned to X patients" badge when workflow has assignments
2. Badge shows current assignment count
3. Badge is clickable to open Manage Usage modal
4. Assignment count updates in real-time when patients are assigned/deassigned
5. Badge is not displayed for workflows with zero assignments
6. Assignment count visible in both Workflow Composer and MyWorkbench list

### Story 6.5: Block-Level Patient Monitoring

As a healthcare provider,
I want to see which patients are currently in each block of an assigned workflow,
so that I can monitor workflow progress.

**Acceptance Criteria:**

1. Blocks in assigned workflows display patient count indicator badge
2. Badge shows number of patients currently in that block
3. Clicking badge opens modal with list of patients in that block
4. Patient list modal shows: patient name, entry time to block, block status (waiting/processing/blocked)
5. Modal updates in real-time as patients move through blocks
6. Empty blocks (no patients) show count of 0 or no badge
7. Patient count indicators are visible at all canvas zoom levels

### Story 6.6: Workflow Edit Restrictions for Assigned Workflows

As a healthcare provider,
I want to be prevented from making breaking changes to assigned workflows,
so that I don't disrupt ongoing patient care.

**Acceptance Criteria:**

1. Active and assigned workflows cannot be switched to draft status
2. Structural changes (adding/removing/reconnecting blocks) require all patients be deassigned first
3. Configuration changes to existing blocks are allowed with warning prompt
4. System displays clear message when attempting restricted actions: "Cannot modify assigned workflow. Deassign all patients first."
5. Archive action is disabled for assigned workflows
6. Update Workflow validates that changes won't break ongoing executions
7. User can view full list of assigned patients when attempting restricted action

## Epic 7: Template Library and Preview

Provide access to workflow template library, read-only template preview with metadata, and template copying functionality to accelerate workflow creation.

### Story 7.1: Template Library Access

As a healthcare provider,
I want to access a library of workflow templates,
so that I can learn from examples and jumpstart common workflows.

**Acceptance Criteria:**

1. MyWorkbench provides access to "Vibrant Intelligence Library" containing workflow templates
2. Library displays templates in grid or list view with preview cards
3. Each template card shows: template name, brief description, usage count, rating/thumbs up count, category tags
4. Templates are organized by categories (e.g., Appointment Management, Lab Results, Chronic Care)
5. Library provides search functionality to find templates by name or keyword
6. Library loads efficiently even with large template collections (lazy loading)
7. Clicking template card opens Template Preview mode

### Story 7.2: Template Preview Mode

As a healthcare provider,
I want to preview workflow templates in read-only mode,
so that I can evaluate them before copying to my workbench.

**Acceptance Criteria:**

1. Selecting template opens Workflow Composer in Template Preview mode
2. Template Preview displays canvas-only layout (no Block Palette or AI Assistant panels)
3. Top banner displays: "Template Preview - Read Only"
4. Side panel displays: template introduction, usage count ("x times used"), thumbs up with count (clickable)
5. Canvas shows template workflow with all blocks and connections
6. Zoom controls are available for navigation
7. All interactive workflow editing features are disabled
8. Template Preview mode is clearly visually distinct from edit mode

### Story 7.3: Template Block Configuration View

As a healthcare provider,
I want to view block configurations in template preview,
so that I can understand how the template is set up.

**Acceptance Criteria:**

1. Clicking blocks in Template Preview mode opens configuration modal in read-only view
2. Configuration modal displays all block settings and parameters
3. Modal clearly indicates read-only status (grayed out form fields, "View Only" banner)
4. Modal provides "Close" button (no Save button)
5. Configuration values are displayed exactly as configured in template
6. User cannot modify any configuration values in preview mode
7. Modal provides context about block's role in template workflow

### Story 7.4: Copy Template to Workbench

As a healthcare provider,
I want to copy a template to my workbench,
so that I can customize it for my specific needs.

**Acceptance Criteria:**

1. Template Preview provides "Copy to My Workbench" button prominently displayed
2. Clicking button creates editable duplicate of template in user's workflow list
3. Copied workflow has all blocks, connections, and configurations from template
4. Copied workflow name is template name with user's practice suffix
5. Copied workflow starts in "Draft" status with no patient assignments
6. User is navigated to Workflow Composer in edit mode with copied workflow
7. Copied workflow appears in MyWorkbench workflow list
8. Copy operation completes within 3 seconds

### Story 7.5: Template Rating and Usage Tracking

As a healthcare provider,
I want to see how often templates are used and rate them,
so that I can find proven, popular templates.

**Acceptance Criteria:**

1. Template cards display usage count ("X times used")
2. Template preview displays thumbs up icon with count
3. Users can click thumbs up to rate template positively
4. User's thumbs up is recorded and count increments immediately
5. Users can un-thumbs-up (toggle off) if clicked by mistake
6. Each user can only thumbs up template once
7. Usage count increments when user copies template to workbench
8. Popular templates (high usage/rating) are featured or sorted higher in library

## Epic 8: AI Assistant Integration

Integrate AI-powered chat assistant into workflow composer for workflow creation guidance, suggestions, and troubleshooting support.

### Story 8.1: AI Assistant Panel Interface

As a healthcare provider,
I want access to an AI assistant while building workflows,
so that I can get help without leaving the workflow composer.

**Acceptance Criteria:**

1. AI Assistant panel displays in right panel of Workflow Composer Compose tab
2. Panel header shows "AI Assistant" with AI icon
3. Panel is collapsible to maximize canvas space when not needed
4. Panel has fixed width (~350px) with scrollable message history area
5. Panel provides clear visual distinction from Block Palette and Canvas
6. Panel layout accommodates message history and input area
7. Panel is accessible via keyboard navigation

### Story 8.2: AI Chat Interaction

As a healthcare provider,
I want to chat with the AI assistant about my workflow,
so that I can get guidance and suggestions.

**Acceptance Criteria:**

1. Chat interface provides text input field and send button
2. User messages appear right-aligned in message history
3. AI responses appear left-aligned in message history
4. Enter key sends message, Shift+Enter creates new line in input
5. Send button is disabled while AI is generating response
6. AI responses stream in real-time as they generate
7. Message history is scrollable and auto-scrolls to latest message
8. Input field clears after sending message

### Story 8.3: AI Workflow Suggestions

As a healthcare provider,
I want the AI to suggest workflow structures and blocks,
so that I can build workflows faster with expert guidance.

**Acceptance Criteria:**

1. User can describe desired workflow in natural language to AI
2. AI analyzes description and suggests appropriate blocks and structure
3. AI suggestions include rationale for recommended blocks
4. AI can suggest entire workflow templates based on use case
5. User can ask AI to explain how specific blocks work
6. AI suggestions are contextual based on current workflow state
7. AI responses are helpful, accurate, and appropriate for healthcare workflows

### Story 8.4: File and Image Attachment Support

As a healthcare provider,
I want to attach images and files in AI chat,
so that I can share examples or screenshots for better assistance.

**Acceptance Criteria:**

1. Chat input area provides attachment button/icon
2. Clicking attachment opens file picker
3. Supported file types include: images (PNG, JPG), PDFs, text files
4. Attached files appear as preview in message before sending
5. User can remove attached file before sending
6. AI can analyze attached images and reference them in responses
7. File size limit is enforced (e.g., 10MB) with clear error message
8. Uploaded files are handled securely

### Story 8.5: AI Context Awareness

As a healthcare provider,
I want the AI to understand my current workflow context,
so that suggestions are relevant to what I'm building.

**Acceptance Criteria:**

1. AI has access to current workflow structure (blocks, connections, configurations)
2. AI can reference specific blocks in workflow by name in responses
3. AI suggestions account for blocks already placed on canvas
4. AI can identify potential issues or gaps in workflow logic
5. AI maintains conversation context across multiple messages
6. AI can answer questions about specific blocks in current workflow
7. AI context resets when user switches to different workflow

### Story 8.6: AI Error Handling and Limitations

As a healthcare provider,
I want clear feedback when AI encounters errors or limitations,
so that I understand what's happening and can adjust my approach.

**Acceptance Criteria:**

1. AI service connection errors display friendly error message
2. AI response timeouts show "AI is taking longer than expected" message with retry option
3. AI clearly communicates when it cannot answer a question or doesn't understand
4. AI provides suggestions for rephrasing unclear questions
5. AI disclaims when providing general guidance vs. definitive answers
6. Rate limiting is handled gracefully with clear messaging
7. AI error states don't break chat interface or prevent further interaction

## Checklist Results Report

### Executive Summary

**Overall PRD Completeness**: 85%

**MVP Scope Appropriateness**: Just Right - The PRD appropriately scopes a brownfield frontend enhancement with clear boundaries and phased delivery through 8 epics.

**Readiness for Architecture Phase**: Nearly Ready - PRD is well-structured with comprehensive functional requirements and clear user stories. Primary gap is the placeholder for block type requirements (FR5) which needs population before full architecture design.

**Most Critical Gaps**:
1. FR5 Block Type Requirements placeholder needs population with detailed specifications for each block type (Triggers, Actions, Logic)
2. No explicit out-of-scope section to clarify backend boundaries
3. Limited data model specifications for workflow serialization format
4. Minimal security/HIPAA considerations for healthcare context

### Category Analysis

| Category                         | Status  | Critical Issues |
| -------------------------------- | ------- | --------------- |
| 1. Problem Definition & Context  | PASS    | None - Clear problem, target users, and goals |
| 2. MVP Scope Definition          | PARTIAL | Missing explicit out-of-scope section; FR5 placeholder |
| 3. User Experience Requirements  | PASS    | Well-defined UX vision, interaction paradigms, core screens |
| 4. Functional Requirements       | PARTIAL | FR5 block type details missing; otherwise comprehensive |
| 5. Non-Functional Requirements   | PARTIAL | Good performance specs; missing HIPAA/security details |
| 6. Epic & Story Structure        | PASS    | Excellent epic sequencing with 48 well-formed stories |
| 7. Technical Guidance            | PARTIAL | Integration points identified; needs data model specs |
| 8. Cross-Functional Requirements | PARTIAL | Integration points clear; data model and HIPAA gaps |
| 9. Clarity & Communication       | PASS    | Well-structured, consistent terminology, clear writing |

### Top Issues by Priority

**BLOCKERS**:
- **FR5 Block Type Requirements**: Placeholder section must be populated with detailed requirements for each block type (triggers, actions, logic blocks). This is critical for both UX design and architecture.

**HIGH**:
- **HIPAA/Security Requirements**: Healthcare context requires explicit security and compliance considerations, especially for patient data in workflow execution
- **Data Model Specification**: Workflow serialization format, block configuration schema, execution state model need definition
- **Out-of-Scope Boundaries**: Explicitly document what is NOT included (backend execution engine, patient management system, AI service implementation)

**MEDIUM**:
- **Error Recovery Patterns**: More detail on error handling and recovery for failed workflow executions
- **Audit Trail Requirements**: Workflow changes and patient assignments likely need audit logging for healthcare compliance
- **Template Governance**: Who creates/approves templates for the Vibrant Intelligence library?

**LOW**:
- **Internationalization**: No mention of i18n/l10n requirements
- **Offline Capabilities**: Are there scenarios where offline access is needed?
- **Mobile Responsiveness Details**: General responsive design mentioned but mobile-specific workflows unclear

### MVP Scope Assessment

**Appropriately Scoped**:
- Epic sequencing is logical and incremental
- Each epic delivers testable value
- Foundation → Building → Testing → Production pipeline is sound
- Brownfield integration approach is realistic

**Potential Complexity Concerns**:
- Epic 2 (Canvas and drag-and-drop) is technically complex and may need 2-3 week timeline
- Epic 8 (AI Assistant) depends on external AI service selection and integration - could be deferred to post-MVP
- Block-level patient monitoring (Story 6.5) with real-time updates adds significant complexity

**Suggestions for True MVP**:
- Consider deferring Epic 8 (AI Assistant) to Phase 2 - workflow creation is functional without it
- Template rating/usage tracking (Story 7.5) could be simplified to basic usage count only
- Batch patient assignment (Story 6.2) could start with single assignment only

### Technical Readiness

**Well-Defined**:
- Frontend integration points clear
- Performance benchmarks specified (NFRs)
- Testing requirements comprehensive
- Browser compatibility noted

**Needs Architect Investigation**:
1. **Workflow Data Model**: Architect must design workflow definition schema, block configuration format, execution state model
2. **Canvas Rendering Technology**: Decision needed on canvas library (e.g., React Flow, Rete.js, custom SVG)
3. **Real-Time Updates**: Architecture for block-level patient monitoring with real-time updates
4. **Auto-Save Architecture**: Debouncing strategy, conflict resolution, offline handling
5. **Block Type Extensibility**: Framework for adding new block types in future

**Identified Technical Risks**:
- Canvas performance with 100+ blocks may require optimization strategies
- Real-time patient monitoring could create scaling challenges
- AI assistant context awareness requires sophisticated state management
- Auto-layout algorithm complexity for complex workflow graphs

### Recommendations

**Immediate Actions (Before Architecture Phase)**:

1. **Populate FR5 Block Type Requirements**
   - Document each trigger type (e.g., Order Status Changed, Report Available, Calendar Event Created)
   - Document each action type (e.g., Send Message, Create Task, Update Note)
   - Document each logic type (e.g., If/Then, Wait, Loop, AI Touch)
   - Specify configuration parameters for each block type

2. **Add Out-of-Scope Section**
   - Backend workflow execution engine (integration point defined, implementation out of scope)
   - Patient management system (integration point defined, implementation out of scope)
   - AI service selection and deployment (integration point defined, implementation out of scope)
   - MyWorkbench implementation (assumes exists or will be developed separately)

3. **Add Security & Compliance Section**
   - HIPAA considerations for patient data in workflows
   - Audit logging requirements for workflow changes and patient assignments
   - Data encryption requirements for workflow configurations
   - Access control requirements (who can create/edit/assign workflows)

4. **Define Data Model Requirements**
   - Workflow definition JSON schema (at high level)
   - Block configuration structure
   - Execution state model for patient progress tracking
   - Template metadata structure

**Suggested Improvements**:

1. Add user personas section (e.g., "Dr. Sarah - Primary Care Physician", "Nurse Coordinator")
2. Include workflow examples (e.g., "Lab Result Notification Workflow" with specific trigger → action → logic sequence)
3. Consider adding wireframe references or mockups for key screens (even hand-drawn sketches)
4. Add section on workflow versioning strategy (what happens when active workflow is updated?)

**Next Steps**:

1. User to populate FR5 Block Type Requirements placeholder
2. PM to add out-of-scope, security, and data model sections
3. Review updated PRD with stakeholders
4. Hand off to UX Expert for UI/UX design
5. Hand off to Architect for technical design

### Final Decision

**NEEDS REFINEMENT**: The PRD is high-quality and nearly ready, but requires:
- FR5 Block Type Requirements population (BLOCKER)
- Out-of-scope clarification (HIGH)
- Security/HIPAA section (HIGH for healthcare context)
- Data model specifications (HIGH)

Once these items are addressed, the PRD will be **READY FOR ARCHITECT**.

## Next Steps

### UX Expert Prompt

The Workflow Frontend PRD is ready for UX design. Please review the PRD and create comprehensive UI/UX specifications including:

- Detailed wireframes for all core screens (MyWorkbench, Workflow Composer with three panels, Test & Log interface, Template Preview)
- Visual design system (colors, typography, iconography for healthcare context)
- Component library specifications (Block Palette blocks, Canvas blocks in various states, modals, etc.)
- Interaction design specifications (drag-and-drop mechanics, zoom controls, connection creation, etc.)
- Responsive design guidelines for desktop/tablet usage
- Accessibility specifications (WCAG AA compliance, keyboard navigation)

Focus on creating a clean, professional healthcare aesthetic that balances powerful functionality with simplicity and clarity.

### Architect Prompt

The Workflow Frontend PRD is ready for technical architecture design (pending resolution of FR5 Block Type Requirements and data model specifications). Please review the PRD and create comprehensive technical architecture including:

- Frontend architecture (component structure, state management, data flow)
- Workflow data model (JSON schema for workflow definitions, block configurations, execution state)
- Canvas rendering architecture (technology selection and performance optimization strategy)
- API integration layer (backend service contracts for workflow CRUD, patient assignment, execution, logging)
- Real-time update architecture (for patient monitoring and auto-save)
- Testing strategy (unit, integration, E2E test approach)
- Deployment architecture (build process, environment configuration, CI/CD)

Ensure architecture supports brownfield integration with existing healthcare platform and accommodates future extensibility for new block types.

