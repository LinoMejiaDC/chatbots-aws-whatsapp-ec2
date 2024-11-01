Here's a well-structured README for your project:

---

# WhatsApp Chatbot for Medical Appointment Scheduling

This repository contains a chatbot built with Python using Flask and OpenAI's GPT API, designed to handle client interactions for a medical office via WhatsApp. The chatbot assists clients with inquiries, provides information about services, and facilitates appointment scheduling through a personalized and friendly conversation. This project integrates Twilio's WhatsApp API to communicate with users, while OpenAI's ChatGPT powers conversational responses.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Contribution](#contribution)
- [License](#license)

---

## Features

- **Dynamic Conversations**: Engages users with personalized and friendly responses.
- **Scheduling Information**: Provides clinic details and appointment scheduling links.
- **WhatsApp Integration**: Communicates directly with clients through WhatsApp using Twilio.
- **Data Saving**: Saves conversation logs daily for tracking and quality improvement.
- **Multi-threaded Scheduler**: Runs background tasks to periodically save conversation logs.

## Prerequisites

To run this project, you’ll need:

- **Python 3.8+**
- **Twilio API Account** (with WhatsApp Business enabled)
- **OpenAI API Key**
- **Flask** for building the web server
- **Twilio Python Helper Library** for WhatsApp messaging
- **Additional Libraries**: `schedule`, `pytz`, `threading`

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your_username/whatsapp-chatbot-medical-scheduling.git
   cd whatsapp-chatbot-medical-scheduling
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Twilio and OpenAI API keys** (see Configuration below).

## Configuration

### Setting Up Environment Variables

To securely manage API keys, create a `.env` file in your root directory and add:

```bash
# .env
OPENAI_API_KEY="your_openai_api_key"
TWILIO_ACCOUNT_SID="your_twilio_account_sid"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
```

### Configuring Chatbot Details

Within the main Python script, update the variables in the **Configuration** section to match your medical practice:

- **name_bot**: Name of the bot
- **name_profesional**: Name of the professional (e.g., Dr. Joana)
- **product_bot**: Details of services offered, including descriptions, prices, and discounts.
- **atendimento**: Types of consultations (in-person or online)
- **formas_pagamento**: Accepted payment methods

## Usage

To start the chatbot, run:

```bash
python app.py
```

The app will start a Flask server, listening for incoming requests from Twilio. 

You can set up a public URL using a tool like [ngrok](https://ngrok.com/) to expose your local server for testing.

### Testing the Chatbot

To test the chatbot in a development environment:

1. Register a WhatsApp number with Twilio.
2. Set up your Twilio WhatsApp Sandbox and configure it to send messages to your local server.
3. Use the Twilio Sandbox number to send a message and test interactions.

## Project Structure

The main sections of the code include:

1. **Libraries and Configurations**: Imports and initial variable configurations.
2. **User Interactions**: Handles message reception and replies.
3. **Context and Conversation Flow**: Sets up the conversation flow based on user inputs.
4. **Scheduler for Logging Conversations**: Saves daily conversation logs and runs in a background thread.

```plaintext
whatsapp-chatbot-medical-scheduling/
├── app.py                       # Main application script with chatbot logic
├── config.py                    # API keys and other sensitive information
├── remove.py                    # Utility script for managing banned users or terms
├── requirements.txt             # Required Python libraries
└── README.md                    # Documentation file
```

## How It Works

1. **Receive and Parse Messages**: The Flask server listens for incoming WhatsApp messages from Twilio, capturing user inputs like questions about services, appointments, and payments.

2. **Engage in Conversation**:
   - The bot responds with predefined messages or dynamically generated answers using OpenAI's GPT API.
   - Based on the message flow, the bot may ask for personal information, provide clinic details, or direct the user to a booking link.

3. **Context Management**: The bot stores user information to maintain conversation flow across interactions, personalizing responses accordingly.

4. **Daily Log Saving**: Each day, the bot saves conversation logs in JSON format for tracking and potential analysis. This is handled by a background scheduler running as a separate thread.

5. **Message Limits and Exclusions**: If a user exceeds the message limit or belongs to a list of removed users, the bot can end the conversation or exclude them from further responses.

## Contribution

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License.

---

This README provides an overview of the bot's functionality, setup, and usage.
