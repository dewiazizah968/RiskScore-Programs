# RiskScore
RiskScore is a credit risk scoring system designed to classify potential borrowers based on their credit risk level. The system utilizes a combination of divide-and-conquer algorithms and threshold-based greedy approaches to assess and categorize risk effectively.

To facilitate the development process, each webpage in the system is implemented as a separate Python file. This modular approach was adopted to streamline collaboration within a three-person development team.


## Installation and Cloning
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/riskscore.git
   ```
2. Navigate to the project directory:
   ```bash
   cd riskscore
   ```
3. Make sure you have Python installed. Then, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Converting to an Executable File
This application is desktop-based. To generate an executable file for the system:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the following command to create an executable:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico main.py
   ```
   - `--onefile`: Combines all files into a single executable.
   - `--windowed`: Removes the console window when running the application.
   - `--icon=icon.ico`: Sets the application icon.

3. After the process completes, the executable file will be located in the `dist` folder.


## Accessing the Application
To view the completed application, navigate to the `dist` folder. The executable file will be ready for use.


## Contributing
We welcome contributions to improve and extend this project. If you have suggestions, fixes, or ideas for new features, feel free to fork the repository and create a pull request. Your input is highly appreciated!


Thank you for your interest in RiskScore! If you have any questions or need further assistance, please don't hesitate to reach out.

