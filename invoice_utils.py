# invoice_utils.py
import os
from importnb import Notebook

# Load the notebook (which contains the function)
with Notebook():
    from notebooks.ocr import process_invoice, format_invoice_data, plot_tax_per_item  # Import the function directly

# You can now call get_invoice_data from here in other files
