# Customer Support Bot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5%2B-green)](https://openai.com/)

A powerful customer support chatbot built with Streamlit and OpenAI's GPT models, designed to handle customer inquiries efficiently and provide intelligent responses.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Customer Support Bot leverages advanced AI to provide instant, intelligent responses to customer queries. Built with Streamlit for a seamless user interface and powered by OpenAI's language models, it offers a modern solution for automated customer service.

## Features

- **🤖 AI-Powered Responses**: Utilizes OpenAI's GPT models for intelligent conversation
- **💬 Real-time Chat Interface**: Clean and intuitive chat UI built with Streamlit
- **🎯 Context-Aware Conversations**: Maintains conversation context for coherent interactions
- **⚡ Easy Deployment**: Simple setup and deployment process
- **🔧 Customizable**: Easy to modify and extend for specific use cases
- **📱 Responsive Design**: Works well on both desktop and mobile devices

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/znblrean/customer-support-bot.git
cd customer-support-bot
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Running the Application

1. **Start the Streamlit app**
```bash
streamlit run app.py
```

2. **Access the application**
   - Open your web browser and go to `http://localhost:8501`
   - Start chatting with the customer support bot!

### Basic Usage

1. Enter your message in the chat input box
2. Press Enter or click the Send button
3. The AI will generate a response based on your query
4. Continue the conversation as needed

## Configuration

### Environment Variables

The following environment variables can be configured:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: GPT model to use (default: gpt-3.5-turbo)
- `TEMPERATURE`: Controls response creativity (default: 0.7)

### Model Settings

You can customize the AI behavior by modifying:
- **Temperature**: Higher values (e.g., 0.8) make responses more creative, lower values (e.g., 0.2) make them more focused
- **Max Tokens**: Limit the length of responses
- **System Prompt**: Define the bot's personality and response style

## Project Structure

```
customer-support-bot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── README.md             # Project documentation
├── utils/                # Utility functions
│   ├── __init__.py
│   └── chat_utils.py     # Chat-related utilities
├── config/               # Configuration files
│   └── settings.py       # Application settings
└── assets/               # Static assets (if any)
```

## Technologies Used

- **Streamlit**: Web application framework
- **OpenAI API**: AI-powered language model
- **Python-dotenv**: Environment variable management
- **Python 3.8+**: Programming language

## Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

1. Follow the installation steps above
2. Make your changes
3. Test thoroughly
4. Ensure code follows PEP 8 guidelines
5. Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/znblrean/customer-support-bot/issues) page
2. Create a new issue with detailed information
3. Provide steps to reproduce any bugs

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Streamlit](https://streamlit.io/) for the excellent web framework
- Contributors and users who help improve this project

---

**⭐ If you find this project helpful, please give it a star!**
