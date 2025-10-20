# Installation

This document provides detailed instructions on how to install the required libraries for the agentic system.

## Prerequisites

*   Python 3.8 or higher
*   pip

## Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/source-_-repo/ai-research-agent.git
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd repository
    ```

3.  **Create a `requirements.txt` file with the following content:**

    ```
    numpy
    nltk
    ```

4.  **Install the required libraries using pip:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Download the NLTK data:**

    Run the following command in your terminal to download the necessary NLTK data:

    ```bash
    python -c "import nltk; nltk.download('all')"
    ```

## Verifying the Installation

To verify that the installation was successful, you can run the test suite:

```bash
python -m unittest tests/test_base_agent.py
```

If the tests run without any errors, the installation is complete.
