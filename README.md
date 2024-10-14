# Create the README.md file with the generated content in markdown format

readme_content = """
# ATS Resume Evaluation Application

This project is an **Applicant Tracking System (ATS)**-based application designed to evaluate resumes against job descriptions. It leverages **Google's Generative AI (Gemini)** model to provide insights into how well a resume matches a job description, highlights missing keywords, and generates a profile summary to help improve the resume. The application also includes a dynamic match percentage meter to visualize the match between the resume and job description.

## Features

- **Conversational ATS Analysis**: Evaluates resumes against job descriptions using AI.
- **Keyword Extraction**: Extracts and compares keywords between resumes and job descriptions.
- **Missing Keywords**: Identifies important skills or keywords that are missing from the resume.
- **Profile Summary**: Generates a summary of the candidate's strengths and weaknesses based on the resume.
- **Match Percentage Visualization**: Displays a dynamic percentage meter showing how well the resume matches the job description.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Setup

### Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.7+**
- **Google Generative AI (Gemini)** API key
- **Virtual Environment** (recommended)

### Installing Dependencies

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/ATS-Resume-Evaluation.git
    cd ATS-Resume-Evaluation
    ```

2. Set up and activate a virtual environment:

    ```bash
    python -m venv myenv
    source myenv/bin/activate    # On macOS/Linux
    myenv\\Scripts\\activate       # On Windows
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables:

    - Create a `.env` file in the root directory and add your **Google API key**:
    
    ```env
    GOOGLE_API_KEY=your-google-api-key
    ```

5. Install the `spaCy` model required for NLP tasks:

    ```bash
    python -m spacy download en_core_web_sm
    ```

## Usage

### Running the Application

1. Start the Streamlit app by running:

    ```bash
    streamlit run app.py
    ```

2. The application will launch in your browser at `http://localhost:8501`.

3. Follow these steps to use the application:

   - **Paste Job Description**: Copy and paste the job description into the text area provided.
   - **Upload Resume**: Upload your resume in PDF format.
   - **Submit**: Click the **Submit** button to evaluate your resume.
   - **View Results**: The app will display:
     - **Job Description Keywords**
     - **Resume Keywords**
     - **Missing Keywords** (keywords present in the job description but missing in the resume)
     - **Match Percentage**
     - **Profile Summary**

### Example Output

#### Match Percentage:

![Match Percentage](https://via.placeholder.com/400x100?text=Match+Percentage+Slider)

#### Missing Keywords:

```plaintext
Missing Keywords: Data engineering, solutions, metrics
