# SquadAI

SquadAI is a an autonomous agent program based on CrewAI, but it is intended to be used as a standalone program like AutoGPT rather than a package. It uses the open source Llama3 model from Groq API rather than OpenAI's models. 

## Features
- **Llama3 Model Integration**: Utilizes the Llama3 model via Groq API, providing a free alternative to other AI models.
- **Lightweight Design**: Built to be simple and easy to understand, making it accessible for developers at any level.
- **Open-Source Focus**: Aiming to attract contributors to help develop and enhance the project.
- **Access to LangChain tools

## Getting Started

### Prerequisites
Ensure you have Python installed on your system. You can check by running:
```bash
python --version
```
or
```bash
python3 --version
```

You will also need to go to Groq Cloud and get a Groq API key. Chage the name of env.template to .env and add your API key. Do the same thing for the WolframAlpha API. Also, consider getting a SerpApi API key as well and add it to the .env file. As this project grows more API keys will probably be needed, but I intend to keep everything free and open source.

### Installation
1. Clone the Repository:
```bash
git clone https://github.com/SpyderRex/SquadAI.git
cd SquadAI
```

2. Install the Requirements:
Install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```

## Usage
To run SquadAI, simply execute the following command in your terminal:
```bash
python3 main.py
```
A prompt will appear asking the user to provide a goal. The process toward completing that goal will be executed.

Alternately, you can create a project in the same way that crewAI does:
```bash
python3 -m squadai create squad test_squad
```

## squadai_tools
The original crewAI program also has a separate package called crewai-tools that must be installed separately. However, I have added this functionality within the project itself, in a module called squadai_tools. This is separate from the tool_reg directory that initializes the LangChain tools for the agents.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Obviously this is a work in project and an experiment with autonomous agent programs using free, open source models. More tools and functionality will be added as the project grows.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact
Spyder Rex - rex.multimedia.llc@gmail.com

Project Link: https://github.com/SpyderRex/SquadAI

## Donating
If you wish to donate financially to this project, you can do so [here](https://www.paypal.com/donate/?hosted_button_id=N8HR4SN2J6FPG)
