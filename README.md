# Patient Chat Workspace

A unified healthcare communication platform that enables medical providers to manage patient interactions across multiple channels (SMS, Email, In-App messaging) in one centralized interface.

## Features

### 🏥 Multi-Channel Communication
- **Unified Inbox**: SMS, email, and in-app messages in one place
- **Real-time Status**: Patient online/offline indicators
- **Message Threading**: Organized conversations with timestamps and channel labels

### 👥 Patient Management
- **Patient Directory**: Visual patient list with profile photos
- **Status Tracking**: Online status and last activity indicators
- **Smart Search**: Find patients, chats, or documents quickly
- **Unread Counters**: Never miss important messages

### 🤖 AI Assistant Integration
- **Built-in AI Chat**: Floating assistant window
- **Smart Notifications**: Badge system for pending items
- **Always Available**: 24/7 support for patient care decisions

### 📅 Appointment Scheduling
- **Quick Booking**: Streamlined appointment creation
- **Multiple Types**: Follow-up, initial consultation, lab review, treatment sessions
- **Flexible Duration**: 30, 45, 60, or 90-minute slots
- **Notes Support**: Add appointment details and special instructions

### ✅ Task Management
- **Priority System**: Low, medium, high, urgent task levels
- **Due Date Tracking**: Never miss important deadlines
- **Detailed Descriptions**: Full context for each task
- **Assignment Capabilities**: Delegate tasks to team members

### 📋 Forms & Templates
- **Document Sharing**: Send forms and templates to patients
- **Lab Results**: Distribute test results and reports
- **Template Library**: Pre-built forms for common scenarios

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS 3.4.16
- **Icons**: Remix Icons 4.6.0
- **Fonts**: Inter (primary), Pacifico (accent)
- **Design**: Responsive, mobile-first approach

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/stabruriss/patient-chat-workspace.git
   cd patient-chat-workspace
   ```

2. **Open in browser**
   ```bash
   # Option 1: Direct file access
   open index.html
   
   # Option 2: Local server (recommended)
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

3. **Development with Windsurf**
   - Open the project folder in Windsurf
   - Start iterating and building new features
   - Use the built-in preview for real-time testing

## Project Structure

```
patient-chat-workspace/
├── index.html          # Main application file
├── README.md          # Project documentation
├── LICENSE            # MIT License
└── assets/            # Future: CSS, JS, images
    ├── css/
    ├── js/
    └── images/
```

## Navigation Tabs

The workspace includes four main sections:

1. **My Patients** (Current) - Patient communication hub
2. **My Calendar** - Appointment scheduling and management
3. **My Workbench** - Task and workflow management
4. **My Practice** - Practice settings and configuration

## Customization

### Color Scheme
The app uses a professional healthcare color palette:
- **Primary**: `#4f46e5` (Indigo)
- **Secondary**: `#8b5cf6` (Purple)
- **Success**: `#10b981` (Green)
- **Warning**: `#f59e0b` (Amber)
- **Error**: `#ef4444` (Red)

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interface elements
- Accessible design patterns

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Roadmap

### Phase 1: Core Features
- [x] Patient list and messaging interface
- [x] Multi-channel communication display
- [x] AI assistant integration
- [ ] Real-time message updates
- [ ] Patient search functionality

### Phase 2: Enhanced Features
- [ ] Appointment scheduling backend
- [ ] Task management system
- [ ] Form builder and templates
- [ ] File upload and sharing

### Phase 3: Advanced Features
- [ ] Video calling integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app companion
- [ ] Integration APIs

## Security & Privacy

This application is designed with healthcare data privacy in mind:
- No patient data is stored locally
- All communications should be encrypted
- HIPAA compliance considerations built-in
- Secure authentication patterns ready for implementation

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in this repository
- Contact the development team
- Check the documentation wiki

---

**Note**: This is a frontend prototype. Backend integration and real patient data handling require additional security measures and compliance with healthcare regulations (HIPAA, GDPR, etc.).
