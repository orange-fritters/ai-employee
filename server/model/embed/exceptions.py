
class TranslationFailedError(Exception):
    """Exception raised when translation fails"""
    pass


class EmbeddingFailedError(Exception):
    """Exception raised when embedding creation fails"""
    pass


class DecisionFailedError(Exception):
    """Exception raised when decision fails"""
    pass
