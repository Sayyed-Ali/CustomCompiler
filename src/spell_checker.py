"""
Keyword Spell Checker
Uses Levenshtein Distance (Edit Distance) to suggest corrections
This is our first ML feature!
"""

from typing import List, Tuple, Optional


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein (edit) distance between two strings.
    This is a classic Dynamic Programming algorithm used in ML/NLP.
    
    Returns: minimum number of edits (insertions, deletions, substitutions)
        needed to transform s1 into s2
    
    Example:
        levenshtein_distance("whiel", "while") = 1 (swap 'e' and 'l')
        levenshtein_distance("fi", "if") = 2 (2 swaps)
    """
    # Convert to lowercase for case-insensitive comparison
    s1 = s1.lower()
    s2 = s2.lower()
    
    # If one string is empty, distance is length of the other
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    
    # Create matrix for dynamic programming
    # dp[i][j] = edit distance between s1[0:i] and s2[0:j]
    rows = len(s1) + 1
    cols = len(s2) + 1
    dp = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Initialize first row and column
    for i in range(rows):
        dp[i][0] = i  # Distance from empty string
    for j in range(cols):
        dp[0][j] = j  # Distance to empty string
    
    # Fill the matrix
    for i in range(1, rows):
        for j in range(1, cols):
            if s1[i-1] == s2[j-1]:
                # Characters match - no edit needed
                dp[i][j] = dp[i-1][j-1]
            else:
                # Characters don't match - try all operations and pick min
                insertion = dp[i][j-1] + 1
                deletion = dp[i-1][j] + 1
                substitution = dp[i-1][j-1] + 1
                dp[i][j] = min(insertion, deletion, substitution)
    
    return dp[rows-1][cols-1]


class KeywordSpellChecker:
    """
    Checks for misspelled keywords and suggests corrections
    using edit distance algorithm
    """
    
    def __init__(self):
        # All keywords in our language
        self.keywords = [
            'if', 'else', 'while', 'for',
            'int', 'float', 'string', 'bool',
            'true', 'false',
            'print', 'return', 'break', 'continue'
        ]
        
        # Maximum edit distance to consider as "similar"
        # Distance of 1-2 = likely typo
        # Distance of 3+ = probably different word
        self.max_distance = 2
    
    def find_similar_keywords(self, word: str) -> List[Tuple[str, int]]:
        """
        Find keywords similar to the given word.
        
        Args:
            word: The potentially misspelled word
        
        Returns:
            List of (keyword, distance) tuples, sorted by distance
        """
        suggestions = []
        
        for keyword in self.keywords:
            distance = levenshtein_distance(word, keyword)
            
            # Only include if distance is reasonable
            if distance <= self.max_distance:
                suggestions.append((keyword, distance))
        
        # Sort by distance (closest first)
        suggestions.sort(key=lambda x: x[1])
        
        return suggestions
    
    def suggest_correction(self, word: str) -> Optional[dict]:
        """
        Get the best correction suggestion for a word.
        
        Args:
            word: The potentially misspelled word
        
        Returns:
            Dictionary with suggestion details, or None if no good match
        """
        similar = self.find_similar_keywords(word)
        
        if not similar:
            return None
        
        # Get the best match (smallest distance)
        best_keyword, distance = similar[0]
        
        # Calculate confidence score (0-100%)
        # Distance 0 = 100% (exact match)
        # Distance 1 = ~80-90%
        # Distance 2 = ~60-70%
        max_word_len = max(len(word), len(best_keyword))
        confidence = (1.0 - (distance / max_word_len)) * 100
        
        return {
            'original': word,
            'suggestion': best_keyword,
            'distance': distance,
            'confidence': confidence,
            'all_suggestions': [kw for kw, _ in similar[:3]]  # Top 3
        }
    
    def check_identifier(self, identifier: str) -> Optional[dict]:
        """
        Check if an identifier might be a misspelled keyword.
        
        This is called when the lexer finds an IDENTIFIER token
        that's not in the symbol table yet.
        
        Returns:
            Suggestion dict if this looks like a typo, None otherwise
        """
        # Only check if it's similar to a keyword
        suggestion = self.suggest_correction(identifier)
        
        # Only return if confidence is reasonably high (> 50%)
        if suggestion and suggestion['confidence'] > 50:
            return suggestion
        
        return None


# Test the spell checker
if __name__ == "__main__":
    checker = KeywordSpellChecker()
    
    print("Testing Spell Checker (ML Feature #1)\n")
    print("=" * 60)
    
    # Test cases
    test_words = [
        "whiel",      # Common typo for "while"
        "fi",         # Common typo for "if"
        "esle",       # Typo for "else"
        "pritn",      # Typo for "print"
        "flot",       # Typo for "float"
        "intt",       # Typo for "int"
        "treu",       # Typo for "true"
        "xyz",        # Not a keyword
    ]
    
    for word in test_words:
        print(f"\nWord: '{word}'")
        suggestion = checker.suggest_correction(word)
        
        if suggestion:
            print(f"  ✓ Suggestion: '{suggestion['suggestion']}'")
            print(f"  ✓ Confidence: {suggestion['confidence']:.1f}%")
            print(f"  ✓ Edit Distance: {suggestion['distance']}")
            if len(suggestion['all_suggestions']) > 1:
                print(f"  ✓ Alternatives: {suggestion['all_suggestions'][1:]}")
        else:
            print(f"  ✗ No suggestions (not similar to any keyword)")
    
    print("\n" + "=" * 60)
    print("Spell checker working!")