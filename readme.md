<h1 align="center">Interpred</h1>

<p align="center">
  <img src="icon.png" alt="Interpred Icon" width="300" height="300" style="object-fit: cover;">
</p>

<h2 align="center">Lisensi</h2>
<p align="center"><strong>Lisensi:</strong> MIT</p>

**Interpred** is a drug interaction prediction bot built using Python and the `telebot` library. The bot allows users to input a list of drugs, and it returns any potential interactions between them. The application utilizes an open-source database from DrugBank (version 2024-01-02) for the drug interaction information.

## Features

- **Drug interaction prediction**: Predicts possible interactions between drugs.
- **Telegram integration**: Uses Telegram as the interface for interaction with users.
- **Synonym normalization**: The bot normalizes drug names to account for synonyms and product names.
- **Logging**: Logs interactions and user messages to a file as well as outputs logs to the terminal.

## Requirements

Before running **Interpred**, you will need to have the following installed on your system:

- **Python 3.8+**
- **pip** (Python package manager)
- A Telegram bot token (available from the [BotFather](https://core.telegram.org/bots#botfather))

## Getting Started

### Clone the repository

```bash
git clone https://github.com/Arifmaulanaazis/Interpred.git
cd Interpred
```

### Install the required Python modules

```bash
pip install pyTelegramBotAPI logging
```

This will install the required dependencies for the bot, including:

- `telebot` (for Telegram bot interaction)
- `logging` (for logging user interactions and errors)

### Using Git LFS for Large Files

**Interpred** may include large files that are managed by Git LFS (Large File Storage). If you're cloning the repository, ensure you have Git LFS installed to handle these files.

1. **Install Git LFS** on your machine:
   - For Debian/Ubuntu: `sudo apt install git-lfs`
   - For Mac (Homebrew): `brew install git-lfs`
   - For Windows: [Download and install Git LFS](https://git-lfs.github.com/)

2. **Initialize Git LFS** after cloning the repository:
   ```bash
   git lfs install
   ```

3. **Download the large files tracked by Git LFS**:
   ```bash
   git lfs pull
   ```

This will ensure that large files, such as datasets or models, are downloaded correctly after cloning the repository.

### Setup your Telegram Bot

1. Create a Telegram bot by talking to [BotFather](https://core.telegram.org/bots#botfather) and retrieve your bot token.
2. Create a file named `token.json` in the root directory of the project with the following content:

   ```json
   {
       "token": "YOUR_TELEGRAM_BOT_TOKEN"
   }
   ```

### Running the Application

After cloning the repository and installing the dependencies, you can start the bot by running:

```bash
python interpred.py
```

The bot will start and begin listening for messages in your Telegram chat.

### Example Usage

- Send a message in the following format to the bot:

  ```
  prediction: drug1, drug2, drug3
  ```

  The bot will respond with any interactions found between the drugs.

- If no interactions are found, the bot will reply: "No interactions were found between the included drugs."

## Contributing

We welcome contributions to enhance **Interpred**. Here’s how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b my-feature-branch
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add a new feature"
   ```
4. Push your changes:
   ```bash
   git push origin my-feature-branch
   ```
5. Submit a pull request.

Please ensure your code follows the existing code style and passes all tests before submitting.

## License

**Interpred** is licensed under the MIT License. See the `LICENSE` file for more details.

## Citation Database

The drug interaction data used in this project was obtained from DrugBank (version 2024-01-02), an open-source drug database.