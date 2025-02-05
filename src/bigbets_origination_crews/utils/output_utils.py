from markdown import markdown
import pdfkit
import os
from crewai.tasks.task_output import TaskOutput
from bigbets_origination_crews.chat_shared import chat_interface

def print_output(output: TaskOutput, output_dir: str, report_folder: str, file_name: str):
    """
    Processa a saída de uma task, gera um PDF e envia mensagens via chat interface.
    
    Args:
        output (TaskOutput): Saída da task
        output_dir (str): Diretório base de saída
        report_folder (str): Nome da pasta do relatório (ex: "Value Chain", "Demand Signals")
        file_name (str): Nome do arquivo PDF a ser gerado
    """
    message = output.raw
    chat_interface.send(message, user=output.agent, respond=False)

    html_content = markdown(output.raw, extensions=['markdown_tables_extended'])

     # CSS para estilizar as tabelas
    table_css = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            border: 1px solid #ddd;
        }
        td {
            padding: 8px;
            border: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
    """
    
    final_html_content = f"""<html>
        <head>
        <meta charset="UTF-8">
        {table_css}
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """
  
    # Cria a pasta se não existir
    report_dir = os.path.join(output_dir, report_folder)
    os.makedirs(report_dir, exist_ok=True)

    output_pdf_path = os.path.join(report_dir, f"{file_name}.pdf")
    
    # Save the PDF
    options = {
        'encoding': 'UTF-8',
        'custom-header': [("Content-Type", "text/html; charset=UTF-8")]
    }
    pdfkit.from_string(
        final_html_content, 
        output_pdf_path, 
        options = options
    )
    
    # Enconde the path to be used in the URL
    output_pdf_path = output_pdf_path.replace(" ", "%20")
    
    # After saving the PDF file, send a message to the user with the download link
    chat_interface.send(f"You can download the **{file_name}** report [here](http://localhost:5006/{output_pdf_path})", user=output.agent, respond=False)
    
    # ...and then send a message to the user saying that the agent is thinking
    chat_interface.send("Agent thinking...", user="Assistant", respond=False)
