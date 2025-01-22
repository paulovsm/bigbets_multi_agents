import os
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from io import BytesIO
from typing import Any, Optional, Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from crewai_tools import DirectorySearchTool

class URLFilePair(BaseModel):
    url: str = Field(..., description="The URL of the content to read.")
    file_name: str = Field(..., description="The name of the markdown document to be saved with .md extension.")

class OnlineContentReadToolSchema(BaseModel):
    """Input schema for reading content from multiple URLs."""
    url_file_pairs: List[URLFilePair] = Field(..., description="A list of URL and file name pairs.")

class OnlineContentReadTool(BaseTool):
    name: str = "Online Content Read Tool"
    description: str = "A tool to read the content of a web page or PDF file from a given URL. Tool input format shoulbe \"{\"url_file_pairs\": [{\"url\": \"URL\", \"file_name\": \"FILE NAME\"}]}\""
    args_schema: Type[BaseModel] = OnlineContentReadToolSchema
    directory: str = None

    def __init__(self, directory: str):
        super().__init__()
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        try:
            url_file_pairs = kwargs.get("url_file_pairs")
            if not url_file_pairs:
                return "URL and file name pairs are required to fetch and read the content."

            results = []
            for pair in url_file_pairs:
                url = pair['url']
                file_name = pair['file_name']

                try:
                    # Download the content from the URL
                    response = requests.get(url)
                    response.raise_for_status()

                    # Detect content type
                    content_type = response.headers.get('Content-Type', '').lower()

                    if 'application/pdf' in content_type:
                        content = self._extract_pdf_content(response.content)
                    elif 'text/html' in content_type:
                        content = self._extract_html_content(response.content)
                    else:
                        results.append(f"Unsupported content type for URL: {url}")
                        continue

                    # Save the content to a file
                    file_path = os.path.join(self.directory, file_name)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)

                    results.append(f"Content saved to {file_path}")

                except Exception as e:
                    results.append(f"Error processing URL {url}: {str(e)}")
                    
            # Load the vectorized content from the directory
            directory_tool = DirectorySearchTool(self.directory)
            #directory_tool._run()
            
            return results

        except Exception as e:
            return str(e)

    def _extract_pdf_content(self, content: bytes) -> str:
        """Extract text content from a PDF file."""
        pdf_reader = PdfReader(BytesIO(content))
        extracted_content = []

        # Extract text from each page
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:  # Append non-empty content
                extracted_content.append(text)

        return "\n".join(extracted_content)

    def _extract_html_content(self, content: bytes) -> str:
        """Extract text content from an HTML page."""
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text(separator="\n")

# Example usage
if __name__ == "__main__":
    content_tool = OnlineContentReadTool(directory="content")
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"  # Example URL
    result = content_tool._run(url_file_pairs=[{"url": pdf_url, "file_name": "dummy.pdf"}])
    print(result)
