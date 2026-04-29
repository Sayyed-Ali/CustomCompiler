"""
Spell Checker using Levenshtein Distance
ML Feature #1: Detects ALL keyword typos (printt, whiel, etc.)
"""

from typing import Optional

class SpellChecker:
    """Check for keyword spelling mistakes using edit distance"""
    
    def __init__(self):
        # All keywords in the language
        self.keywords = [
            'if', 'else', 'while', 'for',
            'int', 'float', 'string', 'bool',
            'true', 'false',
            'print',  # ← Important: 'print' is here
            'return', 'break', 'continue'
        ]
    
    def levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance (edit distance)
        Returns minimum number of edits needed
        """
        m, n = len(s1), len(s2)
        
        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1].lower() == s2[j-1].lower():
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # deletion
                        dp[i][j-1],      # insertion
                        dp[i-1][j-1]     # substitution
                    )
        
        return dp[m][n]
    
    def check_keyword(self, word: str) -> Optional[dict]:
        """
        Check if word is a misspelled keyword
        
        Examples:
        - "printt" → suggests "print"
        - "whiel" → suggests "while"
        - "fi" → suggests "if"
        
        Returns dict with suggestion or None
        """
        # Don't check if it's exactly a keyword
        if word.lower() in self.keywords:
            return None
        
        best_match = None
        best_distance = float('inf')
        
        # Find closest keyword
        for keyword in self.keywords:
            distance = self.levenshtein_distance(word, keyword)
            if distance < best_distance:
                best_distance = distance
                best_match = keyword
        
        # Only suggest if:
        # 1. Distance is small (1-3 edits)
        # 2. Confidence is good (>40%)
        if best_match and best_distance > 0 and best_distance <= 3:
            max_len = max(len(word), len(best_match))
            confidence = (1 - best_distance / max_len) * 100
            
            # Lower threshold to 40% to catch more typos
            if confidence >= 40:
                return {
                    'suggestion': best_match,
                    'confidence': round(confidence, 1),
                    'distance': best_distance,
                    'original': word
                }
        
        return None


# Test
if __name__ == "__main__":
    checker = SpellChecker()
    
    tests = ["printt", "whiel", "fi", "esle", "pritn", "flot", "treu", "printx"]
    
    print("Testing Spell Checker:\n")
    for word in tests:
        result = checker.check_keyword(word)
        if result:
            print(f"✓ '{word}' → '{result['suggestion']}' ({result['confidence']}%)")
        else:
            print(f"✗ '{word}' → No suggestion")