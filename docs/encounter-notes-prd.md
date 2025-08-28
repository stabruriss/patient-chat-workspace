# Encounter Notes Enhancement Product Requirements Document (PRD)

## Goals and Background Context

### Goals

Based on your existing demo and clarified focus on the composer functionality:

- **Smart Composition Efficiency**: Reduce note composition time by 50-70% through intelligent template matching and auto-population based on input recognition
- **Template Intelligence**: Achieve 80% accuracy in matching user input to appropriate clinical templates and auto-populating relevant sections
- **Action/Object Recognition**: Automatically detect clinical actions (ordered, prescribed, scheduled) and objects (medications, procedures, follow-ups) to trigger appropriate workflow automations
- **Workflow Integration**: Enable 85% of composed notes to automatically generate appropriate follow-up tasks, patient communications, and care coordination workflows
- **Provider Adoption**: Achieve 70% regular usage of the intelligent composer features among existing platform users within 6 months

### Background Context

The Encounter Notes Enhancement focuses primarily on intelligent **composition assistance** rather than voice transcription. While voice-to-text will leverage existing Heidi integration, the core value proposition is in the composer's ability to understand clinical input patterns, match appropriate templates, and recognize actionable content for workflow automation.

The existing encounter notes demo provides the UI foundation with basic text composition. The enhancement adds intelligence layer that listens to input, recognizes clinical patterns (symptoms, treatments, medications, procedures), matches appropriate documentation templates, and identifies workflow triggers - transforming manual note writing into an assisted, structured, and automation-enabled process.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|---------|
| 2024-12-20 | 1.0 | Initial PRD creation focusing on composer intelligence | John (PM) |

## Requirements

### Functional

#### Core System Architecture

**FR1**: The system SHALL provide access to encounter notes through patient chat quick actions(Quick Actions is defined in the MyPatient page) with seamless integration to existing patient communication workflow.

**FR2**: The system SHALL display patient header with basic information, support switching between patients, multi-select patients, and "all patients" view to see all encounter notes across the practice.

#### Voice-to-Encounter Notes (Heidi Integration)

**FR3**: The voice interface SHALL provide start/pause/stop recording controls with visual feedback for recording status.

**FR4**: The system SHALL generate recordings after stopping and allow playback with full transcript viewing capabilities.

**FR5**: The system SHALL generate note previews from transcripts with selectable formats (bullet points or SOAP) using Heidi integration.

**FR6**: The system SHALL support opening generated previews in the Composer to create new notes with pre-populated content.

**FR7**: The system SHALL allow changing patient assignment and service date for generated recordings before creating notes.

#### Composer - Core Note Management

**FR8**: The Composer SHALL support creating, editing, and managing encounter notes with patient assignment and service date assignment.

**FR9**: The system SHALL implement a 3-column layout: note list (left), editor (center), and smart actions (right).

**FR10**: The note list SHALL rank by newest first and provide dual search capabilities: traditional text search and LLM RAG matching ("ask" functionality). (AI is coming soon feature)

#### Editor - Markdown and Smart Input

**FR11**: The editor SHALL be a markdown text editor supporting rich text formatting for clinical documentation.

**FR12**: The system SHALL implement slash commands to insert: eRx, task, appointment, internal note, order, document, and workflow objects.(same as the chat quick actions)

**FR13**: The system SHALL provide "3-letter match" functionality with inline dropdown selection for:
- eRx: drug names  (list from Dr.Frist Integration)
- Order: names of practice products, Vibrant products, bundles (List from myWorkbench eZ-Bill templates)
- Document: pre-defined documents (forms, waivers, handbooks, webpages) (List from myWorkbench document templates)
- Workflow: available workflows (List from myWorkbench workflow templates)
- Smart block: user-defined templates (List from myWorkbench smart block templates)

**FR14**: The system SHALL support patient variable insertion through multiple methods:
- Dollar sign ($) trigger displaying complete list of all available patient variables from the patient-var.md specification
- "3-letter match" functionality with inline dropdown for patient variables (e.g., "age" matches Patient Age, "blo" matches Blood Pressure)
- Questionnaire integration: 3-letter match SHALL also match questionnaire questions and provide options to pull answers from submitted questionnaires with date selection support when patients have submitted multiple instances of the same questionnaire template

#### Smart Action Cards System

**FR15**: The system SHALL automatically create action cards when users insert actionable objects: eRx, order, document, workflow, task, appointment, or internal note objects into notes.

**FR16**: The system SHALL create action cards when inserted smart blocks contain actionable objects.

**FR17**: Action cards in the composer SHALL function as drafts, allowing users to click and edit using the same modals as the chat window.

**FR18**: The system SHALL provide execution capabilities for individual cards (send prescription, send invitation, assign task, place order, share document) from the right column.

**FR19**: The system SHALL support multi-select and "select all" functionality to execute multiple action cards simultaneously.

**FR20**: Upon execution, actions SHALL process through the chat window in the background while keeping users in the composer, with cards marked as executed and becoming view-only.

#### Auto-Note Generation

**FR21**: The system SHALL automatically generate encounter notes when medication actions require documentation for compliance, triggered from actions performed elsewhere in the platform.

**FR22**: Auto-generated notes SHALL include the originating action (eRx/lab order) as an executed smart card within the new note.

**FR23**: The system SHALL provide quick-create buttons from calendar appointments to generate new encounter notes with the appointment as a smart card.(this is a manual action, the note only created when user click the button), after the note is created, the button will be replaced with open note action, the appointment become a smart card in this new note.

#### Note Organization and Linking

**FR24**: The system SHALL organize notes by patient and service date/time without requiring separate encounter IDs.(There is no encounter ID in current design)

**FR25**: Notes SHALL link to their smart card objects, with each card generating predefined (but editable) text blocks in the note upon creation. For example: a Gut Zoomer order card is inserted in a note, the note will have a text block (e.g., "Patient has been prescribed Gut Zoomer stool test for comprehensive gut health analysis") generated from the order card, and the text block is editable.

**FR26**: Text blocks SHALL become independent and non-linked to their originating cards after editing, but linked to the card before editing, allowing it to be removed along with a card.(i.e. remove a card will remove the text blocks generated from it, only if the text block is not edited)

**FR27**: The system SHALL support note service date assignment, signature functionality, and note sharing capabilities.

#### Smart Blocks System

**FR28**: Smart Blocks SHALL be defined and managed through MyWorkbench integration with name-based matching for insertion during note drafting.

**FR29**: Smart blocks SHALL support inclusion of text, patient variables, and action cards within templates.(reuse the middle and right column composer interface as notes)

**FR30**: The system SHALL provide a preloaded library of ready-to-use smart blocks including common medical dictionary terms (allergies, diseases, symptoms, treatments).

**FR31**: Users SHALL be able to edit and rename library smart blocks with reset-to-default functionality available.

**FR32**: The system SHALL support user-defined custom smart blocks with the same composer interface as notes (without history and patient header).

**FR33**: Smart block variables and actions SHALL remain unassigned until used in actual notes, then automatically populate with current patient information.

#### Permission Control System

**FR34**: The system SHALL implement role-based access control supporting Practice Admin, Provider, and Staff permission levels. As defined in MyPractice document.

**FR35**: Practice Admins SHALL have full system access.

**FR36**: Providers SHALL have access to create, edit, and manage encounter notes with full smart block and action card functionality.

**FR37**: Encounter notes SHALL be view-only for Staff.

### Non Functional (for reference only)

**NFR1**: The 3-letter match system SHALL respond within 200ms to provide real-time inline dropdown suggestions.

**NFR2**: The system SHALL handle 100+ concurrent users across voice recording, note editing, and action card execution without performance degradation.

**NFR3**: Patient variable substitution SHALL occur in real-time as users type $ trigger without noticeable latency.

**NFR4**: All patient data, clinical content, and voice recordings SHALL maintain HIPAA compliance with encryption at rest and in transit.

**NFR5**: The system SHALL maintain compatibility with existing iframe modal architecture and integrate seamlessly with current patient chat workflow.

**NFR6**: Smart block and action card operations SHALL execute within x second to maintain clinical workflow efficiency.

**NFR7**: The note search functionality SHALL support both traditional text matching and LLM RAG queries with response times under x seconds.

**NFR8**: Voice-to-text integration with Heidi SHALL maintain 95%+ accuracy for medical terminology transcription.

## User Interface Design Goals (for reference only)

Based on your existing platform architecture and the comprehensive encounter notes functionality:

### Overall UX Vision

The encounter notes interface SHALL seamlessly integrate with the existing healthcare communication platform while providing a powerful, efficient clinical documentation workspace. The design emphasizes **contextual intelligence** where the system anticipates provider needs through smart suggestions, rapid object insertion, and workflow automation - transforming documentation from a burden into an active clinical workflow enabler.

The 3-column layout (note list, editor, smart actions) creates a **unified workspace** where providers can manage multiple patients' notes, compose with intelligent assistance, and execute clinical actions without context switching or modal disruption.

### Key Interaction Paradigms

- **Smart Input**: 3-letter matching and slash commands provide contextual, predictive input that reduces typing and cognitive load
- **Draft-to-Execute Workflow**: Action cards function as drafts in the composer, allowing review and bulk execution to maintain clinical safety while enabling efficiency
- **Contextual Variables**: Dollar-sign and 3-letter matching for patient variables and questionnaire data creates seamless data integration
- **Background Processing**: Actions execute through chat workflow while keeping providers in composer context
- **Progressive Disclosure**: Complex actions (eRx, orders) use familiar modals from chat interface, maintaining consistency across platform

### Core Screens and Views

From a product perspective, the critical screens necessary to deliver the PRD values and goals:

- **Encounter Notes Hub**: Main 3-column interface with patient header, note list, editor, and smart actions
- **Voice Recording Interface**: Heidi-integrated recording controls with playback, transcript viewing, and preview generation
- **Smart Block Management**: Template creation and editing interface (reusing composer layout without patient context)
- **Action Card Modals**: Consistent with existing chat interface for eRx, orders, appointments, tasks, workflows, documents
- **Patient Selection Interface**: Multi-patient support with switching and "all patients" view
- **Note Search Interface**: Dual-mode search with traditional text and LLM RAG "ask" functionality

### Accessibility: WCAG AA

The interface SHALL meet WCAG AA accessibility standards to ensure usability for providers with varying abilities and to support healthcare compliance requirements.

### Branding

The encounter notes interface SHALL maintain consistency with the existing healthcare communication platform's design system:
- **Color Scheme**: Continue using the established indigo primary color (#4f46e5) and healthcare-professional color palette
- **Typography**: Maintain Inter font family for professional healthcare appearance
- **Iconography**: Continue using Remix Icons with healthcare-specific icons (user-heart, file-text, mic, etc.)
- **Component Patterns**: Reuse established modal, button, and form patterns from the existing platform

### Target Device and Platforms: Web Responsive

**Primary**: Desktop/laptop browsers optimized for clinical workflow efficiency
**Secondary**: Tablet devices for bedside or mobile clinical use
**Architecture**: Web-based with iframe modal integration maintaining existing platform patterns

## Technical Assumptions (for reference only)

Based on your existing platform architecture and the comprehensive encounter notes functionality requirements:

### Repository Structure: Monorepo

The encounter notes enhancement SHALL continue with the established **monolithic single-file approach** for each major section, building upon the existing `encounter-notes.html` foundation while integrating with the broader healthcare platform codebase.

### Service Architecture

**Enhanced Monolith with API Integration**: The system SHALL maintain the existing single-file HTML architecture while adding intelligent backend services for:

- **Pattern Recognition Service**: Real-time 3-letter matching and smart input processing
- **Template Management API**: Smart blocks and questionnaire template handling through MyWorkbench integration  
- **Action Card Processing**: Draft creation, execution, and background chat workflow integration
- **Patient Variable Service**: Dynamic variable substitution and questionnaire data retrieval
- **Heidi Integration Layer**: Voice-to-text transcription and preview generation
- **Search Service**: Traditional text search and LLM RAG "ask" functionality

The core interface remains in enhanced `encounter-notes.html` with API calls to these specialized services.

### Testing Requirements

**Unit + Integration Testing**: Given the complexity of real-time pattern matching, action card workflows, and multiple system integrations, comprehensive testing is essential:

- **Unit Testing**: Core logic for 3-letter matching, variable substitution, template processing
- **Integration Testing**: Heidi voice integration, MyWorkbench template sync, chat workflow execution
- **End-to-End Testing**: Complete user workflows from voice recording through note creation to action execution
- **Performance Testing**: 3-letter match response times, concurrent user handling, search functionality

### Additional Technical Assumptions and Requests

**Frontend Architecture:**
- **Technology Stack**: Continue with Vanilla HTML5/CSS3/JavaScript and Tailwind CSS 3.4.16 for consistency
- **Real-time Processing**: WebSocket or Server-Sent Events for real-time 3-letter matching and variable suggestions
- **State Management**: Enhanced DOM manipulation patterns for managing 3-column layout, action cards, and patient context

**Backend Services:**
- **API Framework**: Node.js/Express for rapid development and existing platform compatibility
- **Database**: Enhanced patient data model supporting encounter notes, smart blocks, action cards, and questionnaire responses
- **Caching**: Redis or similar for 3-letter match performance and frequently accessed patient variables

**Integration Requirements:**
- **Heidi API**: RESTful integration for voice transcription and note preview generation
- **MyWorkbench Sync**: Real-time synchronization of templates, smart blocks, and permission changes
- **Chat Workflow API**: Background action execution with status updates and error handling
- **Dr.First Integration**: Real-time drug database access for eRx 3-letter matching

**Performance Considerations:**
- **3-letter Match Optimization**: Local caching of frequently matched terms with server-side fallback
- **Concurrent Users**: Architecture must support 100+ providers with real-time features without degradation
- **Mobile Responsiveness**: Tablet-optimized layout for bedside clinical use

**Security and Compliance:**
- **HIPAA Compliance**: All patient data, voice recordings, and clinical actions must maintain healthcare data protection standards
- **Audit Trails**: Complete logging of note creation, modification, action execution, and template usage
- **Role-based Access**: Integration with existing Practice Admin/Provider/Staff permission system

**Deployment and Scaling:**
- **Iframe Compatibility**: Maintain existing modal integration patterns with enhanced functionality
- **CDN Integration**: Optimized delivery of static assets while maintaining single-file architecture benefits
- **Backup and Recovery**: Robust data protection for clinical documentation and patient information

## Epic List

The following epics provide a logical sequence for delivering the comprehensive encounter notes enhancement, with each epic delivering significant end-to-end functionality:

**Epic 1: Core Composer Infrastructure & Basic Note Management**
Establish the foundational 3-column composer interface with basic note creation, patient assignment, and service date management. Delivers a functional note-taking system.

**Epic 2: Smart Input System (3-Letter Match & Variables)**  
Implement intelligent input capabilities including 3-letter matching for all object types, patient variable insertion with dollar trigger, and questionnaire integration. Delivers dramatically improved typing efficiency and contextual data access.

**Epic 3: Smart Action Cards & Chat Integration**
Create the action card system with draft functionality, bulk execution, and background chat integration. Delivers the core functionality that transforms notes from documentation into actionable clinical workflows.

**Epic 4: Voice Integration & Smart Blocks**
Integrate Heidi voice-to-text with note preview generation and implement the smart blocks template system through MyWorkbench. Delivers voice-enabled documentation and template-based efficiency improvements.

**Epic 5: Advanced Features & Polish**
Add advanced search (LLM RAG "ask" functionality), auto-note generation from external actions, appointment integration, and permission refinement. Delivers the complete clinical workflow platform with all sophisticated features.

## Epic 1: Core Composer Infrastructure & Basic Note Management

**Epic Goal**: Establish the foundational 3-column composer interface that replaces the current basic encounter notes system with a professional clinical documentation workspace. This epic delivers immediate value through improved organization, multi-patient support, and structured note management while creating the infrastructure for intelligent features in subsequent epics.

### Story 1.1: Basic 3-Column Layout Implementation

As a healthcare provider,
I want a 3-column encounter notes interface (note list, editor, smart actions placeholder),
so that I can efficiently manage multiple patients' notes in an organized workspace.

#### Acceptance Criteria
1. 3-column responsive layout renders correctly on desktop and tablet devices
2. Left column displays note list with patient context and service dates
3. Center column provides markdown text editor for note composition
4. Right column displays placeholder for future smart actions functionality
5. Interface integrates seamlessly with existing iframe modal system
6. Layout maintains visual consistency with existing platform design system

### Story 1.2: Patient Header and Context Management

As a healthcare provider,
I want to view and switch between patients in the encounter notes interface,
so that I can manage documentation for multiple patients efficiently.

#### Acceptance Criteria
1. Patient header displays current patient's basic information (name, DOB)
2. Patient switching dropdown allows selection of other patients in the practice
3. "All patients" view option shows combined note list across entire practice
4. Patient context persists when switching between interface tabs
5. Patient information updates dynamically when switching contexts
6. Interface handles patient selection errors gracefully

### Story 1.3: Note Creation and Basic Management

As a healthcare provider,
I want to create, edit, and organize encounter notes with service dates,
so that I can maintain accurate clinical documentation for each patient encounter.

#### Acceptance Criteria
1. "New Note" button creates blank encounter note for selected patient
2. Service date picker allows assignment of encounter date/time
3. Note list displays notes ranked by newest first with search functionality
4. Notes save automatically every 30 seconds with visual save indicators
5. Note deletion requires confirmation and maintains audit trail
6. Each note displays patient name, service date, and creation timestamp

### Story 1.4: Enhanced Markdown Editor Integration

As a healthcare provider,
I want a markdown-enabled text editor optimized for clinical documentation,
so that I can create well-formatted, professional encounter notes.

#### Acceptance Criteria
1. Markdown text editor supports rich formatting (headers, lists, bold, italic)
2. Clinical-optimized toolbar provides quick access to common formatting
3. Real-time preview option shows formatted output alongside raw markdown
4. Editor maintains cursor position and undo/redo functionality
5. Auto-save functionality preserves work without interrupting typing flow
6. Editor supports standard keyboard shortcuts for medical documentation workflows
7. Character count and word count display for documentation requirements

### Story 1.5: Basic Note Search and Organization

As a healthcare provider,  
I want to search and filter encounter notes by patient and date,
so that I can quickly locate specific clinical documentation.

#### Acceptance Criteria
1. Traditional text search functionality searches note content and patient names
2. Date range filtering allows filtering notes by service date periods
3. Patient-specific filtering shows notes for selected patients only
4. Search results highlight matching terms within note content
5. Search performance returns results within 2 seconds for typical practice volume
6. Search functionality works across single patient and "all patients" views
7. Clear search/filter options reset interface to default view

## Epic 2: Smart Input System (3-Letter Match & Variables)

**Epic Goal**: Transform note composition from manual typing to input through 3-letter matching for all object types, comprehensive patient variable integration, and questionnaire data access. This epic delivers dramatic efficiency improvements that will drive user adoption and engagement with the platform.

### Story 2.1: 3-Letter Match Core Engine Implementation

As a healthcare provider,
I want real-time suggestions when I type 3 letters for clinical objects,
so that I can quickly insert accurate medical terms, orders, and workflows without lengthy typing.

#### Acceptance Criteria
1. 3-letter match triggers inline dropdown after typing 3 consecutive letters
2. Dropdown appears within 200ms of trigger for real-time user experience
3. System matches against eRx drugs, orderable items, document templates, workflows, and smart blocks
4. Arrow keys navigate dropdown selection with Enter to insert
5. Escape key dismisses dropdown without insertion
6. Match results display object type icons for easy identification
7. No matches found displays "No results" message with option to create new objects
8. If user keep typing, the dropdown will update in real-time.

### Story 2.2: eRx Drug Name Integration (Dr.First)

As a healthcare provider,
I want 3-letter matching for medication names with accurate drug database access,
so that I can quickly reference and prescribe medications with confidence in accuracy.
(This feature depends on eRx feature)

#### Acceptance Criteria
1. Dr.First integration provides drug database access for 3-letter matching
2. Drug matches display generic and brand names with strength information
3. Drug selection inserts standardized medication name format
4. System handles API timeouts gracefully with cached fallback options
5. Drug interaction warnings display when multiple medications are referenced in same note
6. Prescription formatting follows clinical documentation standards

### Story 2.3: Practice Object Integration (MyWorkbench Templates)

As a healthcare provider,  
I want 3-letter matching for practice-specific orders, documents, and workflows,
so that I can quickly access my practice's templates and standardized procedures.

#### Acceptance Criteria
1. Real-time synchronization with MyWorkbench template libraries for current practice
2. Order matching includes practice products, Vibrant products, and custom bundles
3. Document matching includes document templates
4. Workflow matching displays available automated patient workflow templates
5. Template updates in MyWorkbench reflect immediately in 3-letter match results
6. Practice-specific templates prioritize over generic options in match results
7. Template descriptions display in dropdown to aid provider selection

### Story 2.4: Patient Variable System Implementation

As a healthcare provider,
I want to insert patient variables using $ trigger and 3-letter matching,
so that I can quickly populate notes with current patient data without manual lookup.

#### Acceptance Criteria
1. Dollar sign ($) trigger displays complete list of available patient variables
2. 3-letter matching works for patient variables (e.g., "age" matches Patient Age)
3. Variable insertion pulls real-time patient data from current patient context
4. Variables display with clear labels and current values in dropdown
5. Age calculations display appropriate units (days/weeks/months/years per patient-var.md)
6. Missing or unavailable patient data displays as "[Not Available]" with clear indication
7. Variable categories organize dropdown for easier navigation (demographics, vitals, history)

### Story 2.5: Questionnaire Integration and Data Access

As a healthcare provider,
I want 3-letter matching for questionnaire questions with date selection for responses,
so that I can incorporate patient-submitted assessment data into clinical documentation.

#### Acceptance Criteria
1. 3-letter matching identifies questionnaire questions from submitted patient assessments
2. Question matches display with patient response data and submission dates
3. Multiple questionnaire submissions provide date selection dropdown for specific responses
4. Most recent questionnaire response defaults with option to select historical data
5. Incomplete questionnaire responses display with missing question indicators  
6. Question insertion includes both question text and patient response in plain text
7. System handles questionnaire template updates and maintains historical response access

## Epic 3: Smart Action Cards & Chat Integration

**Epic Goal**: Create the transformative action card system that converts documentation into executable actions. This epic delivers the core competitive advantage by enabling providers to draft, review, and execute clinical actions directly from notes while maintaining safety through the draft-execute pattern and background processing.

### Story 3.1: Slash Command System Implementation

As a healthcare provider,
I want to use slash commands to insert actionable objects into my notes,
so that I can quickly create structured clinical actions while documenting patient encounters.

#### Acceptance Criteria
1. Forward slash (/) trigger displays dropdown menu of available action types
2. Action types include: eRx, task, appointment, internal note, order, document, workflow
3. Slash command selection opens appropriate modal consistent with existing chat interface
4. Modal completion inserts structured text block and creates corresponding action card
5. Multiple slash commands can be used within single note without conflicts
6. System maintains cursor position and typing flow after modal completion
7. Slash commands work consistently across all note types (Normal/Auto)

### Story 3.2: Smart Action Card Creation and Display

As a healthcare provider,
I want automatic action card creation when I insert actionable objects,
so that I can see and manage all clinical actions associated with each note.

#### Acceptance Criteria  
1. Action cards automatically appear in right column when actionable objects are inserted
2. Cards display object type, key details, and current status (draft/executed)
3. Card visual design matches existing chat interface action cards for consistency
4. Cards link to their corresponding text blocks in note editor with highlighting
5. Card deletion removes both card and associated text block (if unedited)
6. Card editing reopens original modal with current values pre-populated
7. Cards persist across note save/load cycles with accurate status tracking

### Story 3.3: Draft Functionality and Card Management

As a healthcare provider,
I want action cards to function as drafts that I can review and modify,
so that I can ensure accuracy before executing clinical actions.

#### Acceptance Criteria
1. All action cards start in "draft" status with clear visual indicators
2. Draft cards allow editing through same modals used in chat interface
3. Card modifications update corresponding text blocks in note (if unedited)
4. Individual card deletion removes card and linked text block with confirmation (if text block is unedited)
5. Draft status persists when switching between notes or patients
6. Auto-save every 30 seconds prevents accidental loss of draft modifications

### Story 3.4: Multi-Select and Bulk Execution

As a healthcare provider,
I want to select multiple action cards and execute them simultaneously,
so that I can efficiently process multiple clinical actions from a single encounter note.

#### Acceptance Criteria
1. Checkbox selection allows individual card selection with visual feedback
2. "Select All" option enables bulk selection of all action cards in current note
3. Multi-select toolbar displays execution options and selected card count
4. Bulk execution processes all selected cards sequentially with progress indicators  
5. Individual card failures don't prevent other cards from executing successfully
6. Execution status updates in real-time for each card

### Story 3.5: Chat Integration

As a healthcare provider,
I want action card execution to process through existing chat workflows,
so that clinical actions integrate seamlessly with established communication patterns.

#### Acceptance Criteria
1. Action execution sends through background
2. Provider remains in composer interface during action processing
3. Executed cards update status and become view-only
4. Failed executions display error messages with retry options where applicable
5. Chat history reflects executed actions.
6. Background processing doesn't interrupt note composition or interface responsiveness
7. Execution status synchronizes across multiple browser sessions for same practice.

## Epic 4: Voice Integration & Smart Blocks

**Epic Goal**: Enhance documentation efficiency through Heidi voice-to-text integration with intelligent note preview generation and implement the comprehensive smart blocks template system. This epic delivers voice-enabled workflows and template-based efficiency improvements that further reduce documentation time and improve consistency.

### Story 4.1: Heidi Voice-to-Text Integration

As a healthcare provider,
I want voice recording with automatic transcription through Heidi integration,
so that I can create encounter note content draft through speech instead of typing.

#### Acceptance Criteria
1. Voice recording tab provides start/pause/stop controls with visual feedback
2. Real-time recording status displays duration and audio quality indicators
3. Heidi API integration processes recordings with medical terminology accuracy
4. Completed recordings allow playback with full transcript viewing
5. Recording management supports patient assignment and service date modification
6. Failed transcriptions provide retry options with error messaging
7. Audio data complies with HIPAA requirements through secure transmission and storage

### Story 4.2: Voice Note Preview Generation

As a healthcare provider,
I want AI-generated note previews from voice transcripts with format selection,
so that I can quickly convert speech into structured clinical documentation.

#### Acceptance Criteria
1. Transcript processing generates note previews in bullet points or SOAP format
2. Preview generation completes within 10 seconds of transcript completion
3. Generated previews maintain clinical accuracy while improving structure and clarity
4. Format selection (bullet/SOAP) influences content organization and medical terminology
5. Preview editing allows modifications before transferring to composer
6. Multiple preview attempts support iterative improvement of generated content
7. Preview quality indicators help providers assess generated content reliability

### Story 4.3: Voice-to-Composer Workflow

As a healthcare provider,
I want to transfer voice-generated previews into the composer for editing,
so that I can combine voice efficiency with intelligent note composition features.

#### Acceptance Criteria
1. "Open in Composer" button transfers preview content to new note, along with patient assignment and service date.
2. Transferred content maintains formatting, with a link to the original voice recording.

### Story 4.4: Smart Blocks Template System

As a healthcare provider,
I want access to smart block templates through MyWorkbench integration,
so that I can quickly insert standardized content, variables, and action cards into notes.

#### Acceptance Criteria
1. Smart blocks integrate with 3-letter matching for rapid insertion
2. MyWorkbench synchronization provides real-time access to practice-defined templates
3. Smart block insertion supports text, patient variables, and embedded action cards
4. Template variables populate automatically with placeholder for patient context upon insertion
5. Historical and draft notes using the modified template kept unchanged, while new invokings using the modified template will use the updated template.

### Story 4.5: Preloaded Smart Block Library Management

As a healthcare provider,
I want access to a comprehensive library of preloaded medical smart blocks,
so that I can quickly insert standardized medical terminology and common clinical patterns without creating custom templates.

#### Acceptance Criteria
1. Preloaded library includes comprehensive medical dictionary terms organized by categories (allergies, diseases, symptoms, treatments, procedures, medications)
2. Library smart blocks SHALL be displayed in a separate tab/section from user-created custom smart blocks to maintain clear distinction between system-provided and practice-specific templates
3. Library smart blocks integrate seamlessly with 3-letter matching alongside custom practice templates
4. Common clinical phrases and documentation patterns included (e.g., "patient denies", "NKDA", "ROS negative except as noted")
5. Medical terminology follows standard clinical abbreviations and formatting (ICD-10 aligned where applicable)
6. Library templates can be edited and renamed by providers. Modified library content should be marked as modified and can be reset to default.
6. Updated library content synchronizes across practice without disrupting custom smart blocks
7. Library categorization supports hierarchical browsing (Cardiology → Symptoms → Chest Pain → variants)
8. User can turn on/off the library smart blocks.

### Story 4.6: Smart Block Management and Customization

As a healthcare provider,
I want to create and customize smart block templates,
so that I can standardize frequently used documentation patterns specific to my practice.

#### Acceptance Criteria
1. Smart block composer interface reuses middle and right column layout without patient context
2. Template creation supports text, patient variables placeholders, and action card placeholders
3. Name-based matching requires unique, searchable template names for 3-letter functionality (i.e. every smart block must have a unique name)
4. Template accessible across practice providers


## Epic 5: Advanced Features & Polish

**Epic Goal**: Complete the sophisticated clinical workflow platform with advanced search capabilities, automated note generation, calendar integration, and refined permission controls. This epic delivers the final layer of intelligence and automation that transforms encounter notes into a comprehensive clinical workflow hub.

### Story 5.1: LLM RAG "Ask" Search Functionality

As a healthcare provider,
I want to ask natural language questions about patient notes and receive intelligent answers,
so that I can quickly find relevant clinical information across large volumes of documentation.

#### Acceptance Criteria
1. "Ask" search accepts natural language queries about patient notes and clinical content
2. LLM RAG processing returns relevant note excerpts with source citations
3. Search results rank by relevance and recency
5. "Ask" functionality works only for single patient notes
6. Search history maintains recent queries for quick re-execution

### Story 5.2: Auto-Note Generation from External Actions

As a healthcare provider,
I want automatic note creation when I perform medication actions requiring compliance documentation,
so that required clinical documentation occurs seamlessly without manual intervention.

#### Acceptance Criteria
1. eRx actions performed outside composer automatically trigger encounter note creation
2. Lab order placement generates corresponding encounter notes with order details
3. Auto-generated notes include originating action as executed smart card
4. Note creation uses appropriate patient context and current service date
5. Auto-generated content use the same text block as corresponding action card was inserted manually.
6. Generated notes appear in note list with "Auto" icon designation for easy identification.
7. Providers can edit auto-generated notes and the icon is removed when the note is edited.

### Story 5.3: Calendar Appointment with "Create Encounter Note" Button

As a healthcare provider,
I want quick-create buttons on calendar appointments to generate encounter notes,
so that I can seamlessly document patient visits directly from scheduling workflows.

#### Acceptance Criteria
1. Calendar appointments display "Create Note" button when appointment is confirmed
2. Button click creates new encounter note pre-populated with appointment details
3. Appointment becomes smart card within newly created note
4. After note creation, "Create Note" button changes to "Open Note" for subsequent access
5. Note creation automatically assigns service date from appointment date/time


### Story 5.4: Enhanced Permission Controls and Audit

As a healthcare provider/administrator,
I want refined permission controls with comprehensive audit trails,
so that clinical documentation maintains appropriate access controls and regulatory compliance.

#### Acceptance Criteria
1. Practice Admin role manages smart block libraries and system-wide template access
2. Provider role creates, edits, and manages encounter notes with full functionality
3. Staff role limited to view-only access for encounter notes with no edit capabilities
4. Permission changes reflect immediately across all user sessions
5. Audit trail captures all note creation, modification, action execution, and access events
6. User activity logging includes timestamps, user identification, and specific actions taken
7. Compliance reporting provides audit data export for regulatory requirements

### Story 5.5: Digital Note Signature

As a healthcare provider,
I want to digitally sign completed encounter notes,
so that clinical documentation meets legal requirements and regulatory compliance standards.

#### Acceptance Criteria
1. Digital signature functionality marks notes as completed with provider identification and timestamp
2. Signed notes become locked from further editing with clear visual indicators (locked icon, grayed out editor)
3. Signature requires provider digital signature
4. Signed notes display signature details (provider name, credentials, signature timestamp) in note header
5. Signature events create comprehensive audit trail entries with provider identification and timestamp

### Story 5.6: Note Export

As a healthcare provider,
I want to export encounter notes in various formats for external sharing and documentation,
so that I can share clinical information with patients, colleagues, and external systems while maintaining HIPAA compliance.

#### Acceptance Criteria
1. Export functionality supports export selected notes to PDF or plain text files.
2. Export options support single, multiple selection, or select all. 
3. Exported documents maintain formatting provider credentials and signature, if signed.
4. Only export the text content of the note, smart cards are not included. 