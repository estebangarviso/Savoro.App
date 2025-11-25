"""
Text utilities for normalization and search
"""

import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalize text by removing accents and converting to lowercase.

    Args:
        text: The text to normalize

    Returns:
        Normalized text without accents in lowercase

    Examples:
        >>> normalize_text("Ñoquis")
        'noquis'
        >>> normalize_text("Café")
        'cafe'
        >>> normalize_text("Pollo a la Parrilla")
        'pollo a la parrilla'
    """
    if not text:
        return ""

    # Convert to NFD (Canonical Decomposition)
    # This separates base characters from their combining diacritical marks
    nfd = unicodedata.normalize("NFD", text)

    # Filter out combining marks (accents)
    # Category 'Mn' is "Mark, Nonspacing" which includes accents
    without_accents = "".join(
        char for char in nfd if unicodedata.category(char) != "Mn"
    )

    # Convert to lowercase and return
    return without_accents.lower()
