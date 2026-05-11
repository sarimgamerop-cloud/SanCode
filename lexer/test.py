# test_lexer.py
# Tests every bug and missing feature identified in the lexer review.
# Run with:  python test_lexer.py
# ============================================================
 
import sys, signal
sys.path.insert(0, '/home/claude')
 
from tokens import *
from scanner import Lexer, UnterminatedStringLiteral, InvalidTokenError
 
# ── Helpers ────────────────────────────────────────────────────────────────────
 
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
 
passed = failed = 0
 
def _run_with_timeout(source, secs=2):
    """Tokenise source with a hard wall-clock timeout. Returns (tokens, error, timed_out)."""
    def _alarm(signum, frame): raise TimeoutError()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(secs)
    try:
        tokens = Lexer(source).tokenise()
        signal.alarm(0)
        return tokens, None, False
    except TimeoutError:
        return None, None, True
    except Exception as e:
        signal.alarm(0)
        return None, e, False
 
def check(label, source, *, expect_types=None, expect_values=None,
          expect_exception=None, expect_hang=False):
    global passed, failed
 
    tokens, exc, hung = _run_with_timeout(source)
 
    def ok():
        global passed
        passed += 1
        print(f"  {GREEN}PASS{RESET}  {label}")
 
    def fail(detail):
        global failed
        failed += 1
        print(f"  {RED}FAIL{RESET}  {label}")
        print(f"        -> {detail}")
 
    if expect_hang:
        if hung:
            ok()
        else:
            result = f"exception: {type(exc).__name__}" if exc else f"tokens: {[t.token_type for t in tokens]}"
            fail(f"expected infinite loop but got: {result}")
        return
 
    if expect_exception:
        if exc and isinstance(exc, expect_exception):
            ok()
        elif hung:
            fail(f"expected {expect_exception.__name__} but lexer hung")
        elif exc:
            fail(f"expected {expect_exception.__name__}, got {type(exc).__name__}: {exc}")
        else:
            fail(f"expected {expect_exception.__name__}, got tokens: {[t.token_type for t in tokens]}")
        return
 
    if hung:
        fail("lexer hung (infinite loop)")
        return
    if exc:
        fail(f"unexpected exception: {type(exc).__name__}: {exc}")
        return
 
    types  = [t.token_type  for t in tokens]
    values = [t.token_value for t in tokens]
 
    if expect_types is not None:
        for i, exp in enumerate(expect_types):
            if i >= len(types) or types[i] != exp:
                got = types[i] if i < len(types) else "<missing>"
                fail(f"token[{i}] type: expected {exp!r}, got {got!r}  |  full: {types}")
                return
 
    if expect_values is not None:
        for i, exp in enumerate(expect_values):
            if exp is None:
                continue
            if i >= len(values) or values[i] != exp:
                got = values[i] if i < len(values) else "<missing>"
                fail(f"token[{i}] value: expected {exp!r}, got {got!r}")
                return
 
    ok()
 
def section(title):
    print(f"\n{BOLD}-- {title}{RESET}")
 
 
# ======================================================================
print(f"\n{BOLD}{'='*62}{RESET}")
print(f"{BOLD}  LEXER TEST SUITE{RESET}")
print(f"{BOLD}{'='*62}{RESET}")
 
# -- Bug 1: ] emits TT_LBRACKET instead of TT_RBRACKET --
section("Bug 1: ] should emit TT_RBRACKET (not TT_LBRACKET)")
 
check("[ emits TT_LBRACKET",
      "[", expect_types=[TT_LBRACKET])
 
check("] emits TT_RBRACKET  <- currently broken (emits TT_LBRACKET)",
      "]", expect_types=[TT_RBRACKET])
 
check("Matched pair [] -> LBRACKET, RBRACKET  <- currently both LBRACKET",
      "[]", expect_types=[TT_LBRACKET, TT_RBRACKET])
 
# -- Bug 2: // line-comment branch is dead (unreachable elif) --
section("Bug 2: // line comments (dead elif causes infinite loop on '/')")
 
check("Bare / hangs  <- infinite loop due to dead elif",
      "/", expect_hang=True)
 
check("// comment hangs  <- same dead branch",
      "// this is a comment", expect_hang=True)
 
check("Code after // should still tokenise (once fixed)",
      "42\n// skip\n7",
      expect_types=[TT_INT, TT_INT, TT_EOF],
      expect_values=["42", "7"])
 
check("/ between operands emits TT_SLASH (once fixed)",
      "10 / 2",
      expect_types=[TT_INT, TT_SLASH, TT_INT])
 
# -- Bug 3: /* */ block-comment termination is broken --
section("Bug 3: /* */ block comments (double-advance skips wrong chars)")
 
check("/* comment */ followed by token  <- may hang or mis-parse",
      "/* hello */ 42",
      expect_types=[TT_INT, TT_EOF],
      expect_values=["42"])
 
check("Multi-line /* */ block comment",
      "/* line1\nline2 */ 99",
      expect_types=[TT_INT, TT_EOF],
      expect_values=["99"])
 
# -- Bug 4: String guard condition too broad --
section("Bug 4: String guard condition rejects valid strings")
 
check('Double-quoted string "hello"',
      '"hello"',
      expect_types=[TT_STR, TT_EOF],
      expect_values=["hello"])
 
check("Single-quoted string 'world'",
      "'world'",
      expect_types=[TT_STR, TT_EOF],
      expect_values=["world"])
 
check('String opening with a letter "abc"  <- guard may block',
      '"abc"',
      expect_types=[TT_STR, TT_EOF],
      expect_values=["abc"])
 
check('String opening with a digit "123"  <- guard may block',
      '"123"',
      expect_types=[TT_STR, TT_EOF],
      expect_values=["123"])
 
check("Unterminated string raises UnterminatedStringLiteral",
      '"no close',
      expect_exception=UnterminatedStringLiteral)
 
# -- Bug 5: ALPHABETS missing 'w' --
section("Bug 5: ALPHABETS string is missing 'w' (uvxyz not uvwxyz)")
 
check("Identifier 'window' -> TT_IDENT  <- 'w' makes lexer error",
      "window",
      expect_types=[TT_IDENT, TT_EOF],
      expect_values=["window"])
 
check("Identifier 'www'",
      "www",
      expect_types=[TT_IDENT, TT_EOF],
      expect_values=["www"])
 
check("Identifier 'lowercase_w'",
      "lowercase_w",
      expect_types=[TT_IDENT, TT_EOF],
      expect_values=["lowercase_w"])
 
# -- Missing: Delimiter tokens --
section("Missing: Delimiter tokens raise InvalidTokenError instead of emitting")
 
check("'.' emits TT_DOT",
      ".", expect_types=[TT_DOT, TT_EOF])
 
check("',' emits TT_COMMA",
      ",", expect_types=[TT_COMMA, TT_EOF])
 
check("':' emits TT_COLON",
      ":", expect_types=[TT_COLON, TT_EOF])
 
check("';' emits TT_SEMICOLON",
      ";", expect_types=[TT_SEMICOLON, TT_EOF])
 
check("Member access 'obj.field' -> IDENT DOT IDENT",
      "obj.field",
      expect_types=[TT_IDENT, TT_DOT, TT_IDENT])
 
check("Args 'f(a, b)' -> IDENT LPAREN IDENT COMMA IDENT RPAREN",
      "f(a, b)",
      expect_types=[TT_IDENT, TT_LPAREN, TT_IDENT, TT_COMMA, TT_IDENT, TT_RPAREN])
 
# -- Missing: Float literal crashes --
section("Missing: Float literals crash with NoneType error")
 
check("Float '3.14' emits TT_FLOAT",
      "3.14",
      expect_types=[TT_FLOAT, TT_EOF],
      expect_values=["3.14"])
 
check("Float '0.5'",
      "0.5",
      expect_types=[TT_FLOAT, TT_EOF],
      expect_values=["0.5"])
 
check("Integer '42' still emits TT_INT",
      "42",
      expect_types=[TT_INT, TT_EOF],
      expect_values=["42"])
 
# -- Minor: advance() at EOF --
section("Minor: advance() has no EOF guard (IndexError risk)")
 
check("Empty source -> only EOF token",
      "",
      expect_types=[TT_EOF])
 
check("Single token then EOF: '+'",
      "+",
      expect_types=[TT_PLUS, TT_EOF])
 
# -- Minor: peek() off-by-one check --
section("Minor: peek() correctness (two-char tokens)")
 
check("'==' -> TT_EQEQ",    "==", expect_types=[TT_EQEQ,    TT_EOF])
check("'!=' -> TT_BANGEQ",  "!=", expect_types=[TT_BANGEQ,  TT_EOF])
check("'>=' -> TT_GTE",     ">=", expect_types=[TT_GTE,     TT_EOF])
check("'<=' -> TT_LTE",     "<=", expect_types=[TT_LTE,     TT_EOF])
check("'**' -> TT_STARSTAR","**", expect_types=[TT_STARSTAR, TT_EOF])
check("'&&' -> TT_AND",     "&&", expect_types=[TT_AND,     TT_EOF])
check("'||' -> TT_OR",      "||", expect_types=[TT_OR,      TT_EOF])
 
# -- Integration --
section("Integration: Realistic program snippet")
 
prog = 'dec x = 42\nif x > 10 { out("ok") }'
 
check("Snippet tokenises without error", prog)
 
check("'dec' is TT_KEYWORD at index 0",
      prog, expect_types=[TT_KEYWORD], expect_values=["dec"])
 
check("Snippet first four tokens: KEYWORD IDENT EQ INT",
      prog,
      expect_types=[TT_KEYWORD, TT_IDENT, TT_EQ, TT_INT],
      expect_values=["dec", "x", None, "42"])
 
# -- Summary --
total = passed + failed
print(f"\n{BOLD}{'='*62}{RESET}")
print(f"{BOLD}  Results: {GREEN}{passed} passed{RESET}{BOLD}, {RED}{failed} failed{RESET}{BOLD} / {total} total{RESET}")
if failed:
    print(f"  {YELLOW}Each FAIL marks an unfixed bug.{RESET}")
else:
    print(f"  {GREEN}All tests passed — lexer is clean.{RESET}")
print(f"{BOLD}{'='*62}{RESET}\n")