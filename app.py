import streamlit as st
import fitz  # PyMuPDF
import difflib


def extract_text(pdf_file):
    """Extract text from a PDF file uploaded by the user."""
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def compare_texts_html(text1, text2):
    """Generate an HTML diff of the texts."""
    text1_lines = text1.splitlines(keepends=True)
    text2_lines = text2.splitlines(keepends=True)
    diff = difflib.HtmlDiff().make_file(text1_lines, text2_lines, context=True, numlines=2)
    return diff

def main():
    # Set the page to wide mode
    st.set_page_config(layout="wide")
    st.title('PDF Text Comparison Tool')

    # Legend for color coding
    legend_html = """
    <div style='margin-bottom: 10px;'>
    <h2>Legend</h2>
    <p><span style='display: inline-block; background-color: #acffac;'>&nbsp;Green background&nbsp;</span> indicates text added in the second document.</p>
    <p><span style='display: inline-block; background-color: #ffabab;'>&nbsp;Red background&nbsp;</span> indicates text removed from the first document.</p>
    <p><span style='display: inline-block; background-color: #ffff99;'>&nbsp;Yellow background&nbsp;</span> indicates modifications or differences within lines.</p>
    <p>Text with no background color remains unchanged.</p>
    </div>
    """
    

    # Moving upload fields to the sidebar
    with st.sidebar:
        st.write("## Upload PDFs for Comparison")
        pdf_file1 = st.file_uploader("Choose the first PDF file", type=['pdf'], key="pdf1")
        pdf_file2 = st.file_uploader("Choose the second PDF file", type=['pdf'], key="pdf2")
        
    st.sidebar.markdown(legend_html, unsafe_allow_html=True)
    compare_button = st.button('Compare PDFs')
    if compare_button:
        if pdf_file1 is not None and pdf_file2 is not None:
            text1 = extract_text(pdf_file1)
            text2 = extract_text(pdf_file2)
            html_diff = compare_texts_html(text1, text2)
            # Displaying the result in the main page area
            st.components.v1.html(html_diff, height=600, scrolling=True)
        else:
            st.error("Please upload both PDF files.")

if __name__ == "__main__":
    main()    