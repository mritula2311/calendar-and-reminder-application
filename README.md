# Enhanced Calendar and Reminder App

This is a PyQt6-based desktop application that provides a user-friendly interface for managing events and reminders. The app features a calendar view, event management system, and customizable UI elements.

## Features

- Interactive calendar view
- Event creation and management
- Color-coded events
- Event recurrence options
- JSON-based event saving and loading
- Dark mode UI
- Customizable background

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- PyQt6 library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/calendar-reminder-app.git
   ```

2. Navigate to the project directory:
   ```
   cd calendar-reminder-app
   ```

3. Install the required dependencies:
   ```
   pip install PyQt6
   ```

## Usage

To run the application, execute the following command in the project directory:

```
python main.py
```

### Adding an Event

1. Select a date on the calendar.
2. Fill in the event details in the right panel:
   - Event Title
   - Event Description
   - Category
   - Color (click "Choose Color")
   - Time
   - Recurrence (None, Daily, Weekly, Monthly)
3. Click "Add Event" to create the event.

### Managing Events

- To view events for a specific date, click on the date in the calendar.
- To edit an event, select it from the list and click "Edit Selected Event".
- To delete an event, select it from the list and click "Delete Selected Event".

### Saving and Loading Events

- Click "Save Events" in the toolbar to save all events to a JSON file.
- Click "Load Events" to load previously saved events.

### Customizing the App

- Click "Change Background" in the toolbar to set a custom background image for the app.

## Contributing

Contributions to the Enhanced Calendar and Reminder App are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project uses the following license: [MIT License](LICENSE).

## Acknowledgements

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [Python](https://www.python.org/)
