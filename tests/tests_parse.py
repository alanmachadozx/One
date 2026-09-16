from src.lexer.scanner import Scanner

def test_scanner_tokens():
    scanner = Scanner("open firefox")
    tokens = scanner.scan_tokens()
    assert len(tokens) > 0
