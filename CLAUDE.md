# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Server
```bash
npm run start          # Start development server on port 8000
npm run dev           # Start development server on port 8080  
npm run preview       # Open http://localhost:8000 in browser
```

### Alternative Server Methods
```bash
python3 -m http.server 8000    # Python server (cross-platform)
python -m http.server 8000     # Python 2 fallback
```

## Architecture Overview

This is a **healthcare communication platform** built as a multi-page HTML application with embedded CSS and JavaScript. The architecture follows a **monolithic single-file approach** for each major section, making it suitable for rapid prototyping and development.

### Core Application Structure

The platform consists of **four main application pages**:

1. **`index.html`** - Patient Chat Workspace (main communication hub)
2. **`Healthcare-Provider-Workbench.html`** - Task management and active workflows
3. **`workflow-composer.html`** - Visual workflow builder with drag-and-drop interface
4. **`My-Practice-Dashboard.html`** - Practice settings and configuration

Each HTML file is **self-contained** with embedded CSS and JavaScript, using CDN resources for external dependencies.

### Technology Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS 3.4.16 (CDN)
- **Icons**: Remix Icons 4.6.0 (CDN)
- **Charts**: ECharts 5.5.0 (for analytics)
- **Fonts**: Inter (primary), Pacifico (accent)

### Key Design Patterns

#### 1. Workflow System Architecture
The workflow composer (`workflow-composer.html`) implements a **Notion-style block editor** with:
- **Block-based workflow creation** with drag-and-drop
- **Two workflow types**: Patient workflows (triggered by patient events) and Practice workflows (system-wide automation)
- **Smart Review system**: AI analysis + human approval with escalation capabilities
- **Conditional logic blocks**: IF/THEN branching, loops, wait conditions
- **AI Touch blocks**: Intelligent analysis and automated decision-making

#### 2. Healthcare Data Model
Based on `obj-status.md`, the system tracks these core healthcare objects with status timestamps:
- **Patient Profile** (Updated)
- **Orders** (Created, Modified, Redrawn, Payment states, Lab status, Cancellation)
- **Reports** (Available, Shared)
- **Encounter Notes** (Shared, Updated)  
- **Documents/Forms** (Viewed, Submitted)
- **Calendar Events** (Created, Accepted, Rejected, Tentative, Cancelled)
- **Tasks** (Open, Completed)
- **Internal Notes** (Updated)

#### 3. Component Communication Pattern
Each HTML file uses **global JavaScript functions** and **DOM manipulation** for state management. Key patterns:
- **Event-driven updates** using `addEventListener`
- **Modal-based configuration** for complex settings
- **Dynamic DOM rendering** for lists and complex UI elements
- **CSS class toggling** for state changes

### Critical Code Sections

#### Workflow Block System (`workflow-composer.html`)
- **Block Configuration Object** (`blockConfigs`): Defines all available workflow block types
- **Block Rendering Logic** (`renderBlockContent`): Handles preview display for each block type
- **Modal Configuration System**: Dynamic modal creation for block-specific settings
- **Smart Review Implementation**: AI analysis toggle, escalation settings, timeout configuration

#### Navigation System (All Files)
- **Consistent navigation tabs** across all pages
- **Active state management** using CSS classes
- **Cross-page linking** with proper URL parameters (e.g., `?type=patient` for workflow types)

#### Healthcare-Specific UI Components
- **Patient status indicators** (online/offline states)  
- **Multi-channel communication** (SMS, email, in-app messaging)
- **Appointment scheduling** with healthcare-specific time slots
- **Task management** with priority levels and assignment
- **HIPAA-compliant design patterns**

### Important Conventions

#### CSS Methodology
- **Tailwind utility-first approach** with custom CSS for complex components
- **Primary color scheme**: `#4f46e5` (Indigo) for healthcare professional feel
- **Responsive design**: Mobile-first with healthcare workflow considerations
- **Custom scrollbar styling** for better UX in healthcare environments

#### JavaScript Patterns  
- **Global scope functions** for cross-component communication
- **Configuration objects** for block definitions and settings
- **Event delegation** for dynamic content
- **Modal lifecycle management** with proper cleanup

#### Healthcare Compliance Considerations
- **No actual patient data storage** in current implementation
- **HIPAA-ready architecture** with audit trail placeholders
- **Secure communication patterns** built into UI design
- **Role-based access control** structure prepared for backend integration

### Development Workflow

When making changes:
1. **Test across all four main pages** to ensure navigation consistency
2. **Verify responsive design** on mobile devices (healthcare workers often use tablets/phones)
3. **Check workflow block functionality** if modifying workflow-composer.html
4. **Maintain color scheme consistency** across all files
5. **Test modal interactions** thoroughly as they're used extensively for configuration
6. Only commit to git when I say so

### Key File Dependencies

- **Tailwind CSS**: Used consistently across all files with same configuration
- **Remix Icons**: Healthcare-specific iconography (user-heart, building, brain, etc.)
- **Inter Font**: Primary typography for professional healthcare appearance  
- **ECharts**: Analytics and reporting visualization (Healthcare-Provider-Workbench.html)

The codebase is designed for **rapid healthcare application development** with a focus on **clinical workflow automation** and **patient communication management**.