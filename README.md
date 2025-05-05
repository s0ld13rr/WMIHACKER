# WMIHacker-Go

WMIHacker 2.0 is a tool written in Python that leverages Windows Management Instrumentation (WMI) for system management tasks, automation, or penetration testing purposes.

## Features

- Execute WMI queries to retrieve system information.
- Perform remote management tasks using WMI.
- Lightweight and fast, written in Python.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/wmihacker-go.git
    cd wmihacker-go
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:
    ```bash
    python wmihacker-go.py
    ```

## Usage

Run the tool with the following command:
```bash
python wmihacker-go.py [options]
```

### Options
- `-query`: Specify a WMI query to execute.
- `-remote`: Provide a remote machine name for remote management.
- `-help`: Display help information.

Example:
```bash
python wmihacker-go.py -query "SELECT * FROM Win32_OperatingSystem"
```

## Requirements

- Python 3.8 or later
- Windows OS

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational and authorized use only. The developers are not responsible for any misuse.
