
class TranslationFailedError(Exception):
    """Exception raised when translation fails"""
    pass


class EmbeddingFailedError(Exception):
    """Exception raised when embedding creation fails"""
    pass


class DecisionFailedError(Exception):
    """Exception raised when decision fails"""
    pass


class QuestionGenerationFailedError(Exception):
    """Exception raised when question generation fails"""
    pass


class AnsweringFailedError(Exception):
    """Exception raised when answering fails"""
    pass
