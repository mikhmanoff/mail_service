
# Email Service Project

This project is a Django-based web application that allows users to send and receive emails using Gmail's IMAP and SMTP protocols. The project includes features such as:

- Sending emails via a web form.
- Viewing a list of incoming emails.
- Viewing detailed content of selected emails.

## Prerequisites

To run this project, you need:

- Python 3.8+
- Django 3.2+
- A Gmail account with [IMAP access enabled](https://support.google.com/mail/answer/7126229?hl=en).
- The following Python packages:
  - `django`
  - `python-dotenv` (to load environment variables)

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd email-service-project
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root of your project and add the following details:

   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

   > **Note**: Use an [app password](https://support.google.com/accounts/answer/185833?hl=en) for Gmail instead of your regular password.

5. **Run database migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

## Usage

- Navigate to `http://127.0.0.1:8000/send-email-form/` to send an email.
- Navigate to `http://127.0.0.1:8000/fetch-emails/` to view a list of incoming emails.

## File Structure

The main files and their roles:

- **mail/views.py**: Handles the logic for sending and fetching emails.
- **mail/templates/send_email.html**: Template for sending emails via a web form.
- **mail/templates/incoming_emails.html**: Template for displaying the list of incoming emails.
- **mail/urls.py**: Maps URLs to views for sending and fetching emails.

## Security

- Ensure that you keep your `.env` file secure and never commit it to version control.
- It is recommended to use app-specific passwords for Gmail instead of your regular password.

## License

This project is licensed under the MIT License.
