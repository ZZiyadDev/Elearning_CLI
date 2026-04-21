# E-Learning CLI Application

A command-line interface application for managing an e-learning platform with role-based access for students, teachers, and administrators.

## Features

### For Students

- **Course Enrollment**: Browse and enroll in available courses
- **Lesson Viewing**: Access course content and mark lessons as completed
- **Progress Tracking**: Monitor completion status and quiz scores
- **Quiz System**: Take quizzes to test knowledge
- **Profile Management**: Change password and view account information

### For Teachers

- **Course Creation**: Create new courses with lessons and quizzes
- **Course Management**: Edit course titles, add/modify/delete lessons
- **Student Monitoring**: View student enrollment and progress
- **Profile Management**: Change password and view account information

### For Administrators

- **User Management**: List, delete, and change user roles
- **Course Oversight**: View and delete courses
- **System Statistics**: Monitor platform usage and completion rates

## Installation

1. Ensure Python 3.6+ is installed
2. Clone or download the project files
3. No additional dependencies required (uses only standard library)

## Usage

Run the application:

```bash
python main.py
```

### User Roles

- **Student**: Focus on learning and progress tracking
- **Teacher**: Create and manage educational content
- **Admin**: System administration and oversight

### Data Files

- `users.json`: User accounts and roles
- `courses.json`: Course content, lessons, and quizzes
- `progress.json`: Student progress and quiz scores

## Security Features

- Password hashing using SHA-256
- Input validation and sanitization
- Role-based access control
- Secure password change functionality

## Development

### Code Structure

- `main.py`: Application entry point and menu routing
- `authentification.py`: Login, registration, and password management
- `etudiant.py`: Student interface and functionality
- `enseignant.py`: Teacher interface and functionality
- `admin.py`: Administrator interface and functionality
- `data.py`: Data loading, saving, and validation utilities

### Adding New Features

1. Update data structures in JSON files as needed
2. Add functionality to appropriate role module
3. Update menus and routing in `main.py`
4. Add validation in `data.py` if required

## Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Update documentation
4. Test thoroughly before committing

## License

This project is open source. Feel free to use and modify as needed.
