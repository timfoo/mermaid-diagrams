import requests
import importlib.util
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from bs4 import BeautifulSoup
import markdown
import streamlit as st
import streamlit.components.v1 as components
import pdfplumber

# Logging
logging.basicConfig(level=logging.INFO)

# Function to scrape text from a URL
def scrape_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, "html.parser")
        text = soup.get_text()
        return text
    else:
        return "Failed to scrape the website"

# Function to load and process PDF
def process_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            tables = page.extract_tables()
    return text

# Function to load a markdown file
def load_markdown_as_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    html_content = markdown.markdown(markdown_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text

# Load content
def load_content(source, source_type):
    if source_type == 'pdf':
        return process_pdf(source)
    elif source_type == 'url':
        return scrape_text(source)
    elif source_type == 'markdown':
        return load_markdown_as_text(source)
    else:
        raise ValueError("""
            Invalid source type. 
            Use "pdf" or "url".
            """)

# Function to generate Mermaid code
def generate_mermaid_code(text, examples, api_key, model_name):
    llm = ChatOpenAI(api_key=api_key, model_name=model_name)
    prompt = PromptTemplate.from_template(template=prompt_template)
    formatted_prompt = prompt.format(examples=examples, text=text)
    response = llm(formatted_prompt)
    return response

# Load examples
def load_examples(file_path):
    spec = importlib.util.spec_from_file_location("mermaid_examples", file_path)
    mermaid_examples_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mermaid_examples_module)
    return mermaid_examples_module.mermaid_examples

# Define the prompt template
prompt_template = """
You are a helpful assistant that generates Mermaid code for diagrams. 
Here are some examples of Mermaid diagrams:

{examples}

Based on the text below, perform the following steps.
1. Identify the entire list of topics or ideas contained in the document
2. Design a detailed mindmap of the document with all the topics identified
3. Generate the corresponding Mermaid code.

Text: {text}

Provide only the Mermaid code. 

Formatting rules:
1. Use only ASCII-safe characters in your response.
2. Enclose all text in a node between "". Here's an example: ("Text in a node")
"""

# Clean mermaid code
def clean_mermaid_code(mermaid_code):
    mermaid_code_cleaned = mermaid_code.content.strip('`').replace('mermaid', '').strip()
    mermaid_code_cleaned = mermaid_code_cleaned.replace(u"\u2018", "'").replace(u"\u2019", "'")
    mermaid_code_cleaned = mermaid_code_cleaned.replace("end", "End")
    return mermaid_code_cleaned

def mermaid_chart_html(mermaid_code_content):
    html_code = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    <div class="mermaid" id="mermaid-chart">{mermaid_code_content}</div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
    """
    return html_code

# Streamlit app
st.set_page_config(
    page_title="AI Diagram Generator",
    layout="centered"
    )

# Sidebar for OpenAI API key and model selection
st.sidebar.title("AI Diagram Generator")
st.sidebar.image("Streamlit-Mermaid/media/mermaid.png")
st.sidebar.markdown("Use this tool to easily convert a webpage or PDF document into a mindmap!")

api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password", placeholder="sk-********")
help_text = st.sidebar.markdown("_Don't worry, your keys are not saved! Refresh the page to test it out._") 
linebreak_text = st.sidebar.markdown(" ") 
model_name = st.sidebar.selectbox("Select the OpenAI model name:", ["gpt-4o-mini", "gpt-4o"])

# Main content
tab1, tab2 = st.tabs(["📈 Diagram Generator", "Sample Output"])

with tab1:
    st.title("What do you want to convert?")

    # User input for source type
    source_type = st.selectbox("Select source (URL or PDF):", ["url", "pdf"])

    # User input for source based on source type
    if source_type == "pdf":
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file is not None:
            source = uploaded_file
    else:
        source = st.text_input("Enter the URL:")

    if st.button("Generate Mermaid Diagram"):
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        elif source_type == "pdf" and uploaded_file is None:
            st.error("Please upload a PDF file.")
        elif source_type == "url" and not source:
            st.error("Please enter a URL.")
        else:
            if source_type == "pdf":
                text = process_pdf(source)
            else:
                text = scrape_text(source)
            
            mermaid_examples = load_examples("mermaid_examples.py")

            # Generate Mermaid code
            with st.status(label="Generating Mermaid code...", expanded=True) as status:
                mermaid_code = generate_mermaid_code(text, mermaid_examples, api_key, model_name)
                st.write("Generating Mermaid code...")
                # Clean the Mermaid code
                cleaned_mermaid_code = clean_mermaid_code(mermaid_code)
                st.write("Cleaning Mermaid code...")
                st.write("Rendering Mermaid diagram...")
                status.update(label="Done!", state="complete", expanded=False)
                mermaid_html = mermaid_chart_html(cleaned_mermaid_code)
                
            st.markdown("## Mermaid Diagram")
            components.html(mermaid_html, width=800, height=400, scrolling=True)
            st.markdown("## How do I edit and/or save in a higher resolution")
            st.markdown("Copy the code below and paste it into the Mermaid Live Editor")
            st.link_button("Mermaid Live Editor", "https://mermaid.live", type="secondary")
            with st.expander("Generated Mermaid Code"):
                st.markdown("#### Generated Mermaid Code")
                st.code(cleaned_mermaid_code, language="mermaid")
            st.image("Streamlit-Mermaid/media/mermaid_live.jpeg", caption="How to use the Mermaid Live service")
                
with tab2:
    st.markdown("# Sample Output")
    st.markdown("Source: https://apoorv03.com/p/the-economics-of-generative-ai")
    st.markdown("Edit this in the Mermaid Live Editor: [Mermaid Live](https://mermaid.live/edit#pako:eNqNVV1r20AQ_CuLaKAFB1KK29QvwXHS1g9t0ti4UPyyOa2lI6c7cR9yTUh-e_ckOXFtKY2fhDw7tzsze7pPhEkpGSWF1GmB5VJbY_zbZTLPCS6F0aaQwoFZwVfSZNHLimA8XSbvlhr4x8irimwlaf30rn0fGWZUSFC4IQsF3pGDx88nR5ENlYqMTAWlNSvpHXiT4maf5EvwwRJUqAIB6hS8Re2kl0bv9rCo_x8LYQMqkLrl3mebBGtJe2jgF9J5K2_DP2Q76LY_51HcjWB87HIsKYXKwaJ97qq6oYo0s895xM0BoAVFXdwIHt98Gp73YaZ6ZTFi3p_0YsZlqaTAOEFNt8cWRzZFiVY6o2EtfQ4TZULaOrvp6n-qfZC1zY3o6Y5KUVkRCboK65laswWW0Tf2-_TDUZueqKVtxHG73l3X_r_evAaPt1JJv_mviaxQVGZ4cjwcHkFmjXMcRZtJ7bqnb0T_-Brw1sXTF8ExSfWf7aATowXPYbGv5UbIVkJmP60VbA5ol6WrbCFd1M9SycLzATV_f-Xzcl2TdSWJ6PlB57Ncrnz05FqhXxlbNLvTdf7ln0gC-BzJNgzeQIZMUfVVfmMPjeUiBWIvroVhn5vNPwxeDIXlrMbCn5yqeg26Dvgl-br5sZheTMdskWRtuJ1cZvnWsLPOtsyam-BKDi5P1Sq4DR5VRlV01reZ5-Q9z17yWFJn9QDtJaZkpgv2p69yEliNAhwfw1sKIpelA5YelFkz43xy1XtjFNxiRZHcRc8KvtoVoGUKz9aw132VN5QGsd3wpkwY593hbaJdKLiLGWXxGJgfXse7CqJN18gRa4IQysxiSjEQLGlKlRTU6dfTMTthcuCaM90LFyYHtAaPGBzn7oNeajYnpiASjjie_PnLBlBQKrGvph4VRUPP61uRGgAdc2K5UxGlTQYJP3LAUv6g3keSZeJz9mOZjPgxpRUGxb4v9QNDMXgz22iRjLwNNEhCmaKnC4ksUpGMVqgcv-WOeDe-Nx_p-ls9SKwJWf6EKFH_NmZb8fAX53VU7g)")
    st.markdown("## This mind map....")
    st.image("Streamlit-Mermaid/media/mindmap_sample.png")
    st.markdown("## ...is generated using this Mermaid code")
    st.code("""
        mindmap
    root("The Economics of Generative AI")
        ("Overview")
            ("The Semi layer makes ~90% of all Gen AI profits today")
            ("Future value and transition")
        ("Value Accrual in Gen AI")
            ("Current Value Distribution")
                ("Gen AI stack: A-shaped vs V-shaped")
                ("Revenue Tally")
                    ("Semis: ~$75B")
                    ("Infra: ~$10B")
                    ("Applications: ~$5B")
            ("Comparison with Cloud Economy")
                ("Intuitive value distribution in cloud")
                ("Semis layer captures ~83% of Gen AI revenues")
        ("Profit Accrual in Gen AI")
            ("Current Profitability Distribution")
                ("Apps: ~50-55% gross margins")
                ("Infra: ~65% gross margins")
                ("Semis: ~85% gross margins")
            ("Gross Profit Concentration")
                ("Semis capture ~88% of gross profits")
                ("Visual representation of gross profits")
        ("Future Perspectives")
            ("Shift in Platform Value")
                ("Expect application layer to gain value")
                ("Historical comparison with mobile and cloud")
            ("Critical Questions")
                ("Will NVIDIA maintain high margins?")
                ("How will AI app profitability evolve?")
                    ("Better pricing and value alignment")
                    ("Custom silicon chips for lower TCO")
                    ("Improvements in model architecture")
                    ("Reduction in model costs")
            ("Consumer Segment Transition")
                ("Hardware layer upgrade to AI devices")
                ("Consumer applications segments")
                    ("Information: search")
                    ("Entertainment: gaming, media")
                    ("Transaction: travel, e-commerce")
    """
    )     
        
