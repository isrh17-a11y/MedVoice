import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract and return all text from a PDF file.

    Args:
        pdf_path: Absolute or relative path to the PDF file.

    Returns:
        A single string containing the text from all pages.

    Raises:
        ValueError: If no text could be extracted from the PDF.
        Exception: Re-raised with a descriptive message on any other failure.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = "\n\n".join(pages).strip()
        if not text:
            raise ValueError(
                "Could not extract text. Make sure the PDF is not a scanned image."
            )
        return text
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Failed to parse PDF: {e}") from e


def extract_text_from_string(text: str) -> str:
    """Validate and return plain text input.

    Args:
        text: Raw text string from the user.

    Returns:
        The stripped input text.

    Raises:
        ValueError: If the text is empty after stripping.
    """
    text = text.strip()
    if not text:
        raise ValueError("No text provided.")
    return text
