from flask import Flask, render_template_string, request, jsonify
from contextlib import redirect_stdout
import io

from src.scanner import (
    Lexer,
    InvalidTokenError,
    UnterminatedStringLiteral,
    InvalidIdentifier,
    InvalidFloatLiteral,
    UnintialisedStringLiteral
)

from src.parser import Parser
from src.interpreter import Evaluator

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>San Playground</title>

<style>

body{
    max-width:1000px;
    margin:auto;
    font-family:sans-serif;
    padding:20px;
}

textarea{
    width:100%;
    height:300px;
    font-family:monospace;
    font-size:16px;
}

button{
    padding:10px;
    margin-right:10px;
}

pre{
    background:#eeeeee;
    padding:15px;
    border-radius:8px;
    white-space:pre-wrap;
}

</style>
</head>

<body>

<h1>San Playground</h1>

<textarea id="code">
func fib(n){
    if n <= 1{
        return n
    }

    return fib(n-1)+fib(n-2)
}

stdout fib(10)
</textarea>

<br><br>

<button onclick="runCode()">
Run
</button>

<h2>Output</h2>
<pre id="output"></pre>

<h2>Tokens</h2>
<pre id="tokens"></pre>

<h2>AST</h2>
<pre id="ast"></pre>

<script>

async function runCode(){

    let code =
        document.getElementById("code").value;

    let response =
        await fetch("/run",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                code:code
            })
        });

    let data = await response.json();

    document.getElementById("output").innerText =
        data.output;

    document.getElementById("tokens").innerText =
        data.tokens;

    document.getElementById("ast").innerText =
        data.ast;
}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/run", methods=["POST"])
def run():

    code = request.json["code"]

    try:

        lexer = Lexer(code)
        tokens = lexer.tokenise()

        parser = Parser(tokens)
        ast = parser.parse()

        evaluator = Evaluator()

        buffer = io.StringIO()

        with redirect_stdout(buffer):
            evaluator.evaluate(ast)

        output = buffer.getvalue()

        return jsonify({
            "output": output,
            "tokens": "\\n".join(map(str, tokens)),
            "ast": repr(ast)
        })

    except (
        InvalidTokenError,
        UnterminatedStringLiteral,
        InvalidIdentifier,
        InvalidFloatLiteral,
        UnintialisedStringLiteral
    ) as e:

        return jsonify({
            "output": str(e),
            "tokens": "",
            "ast": ""
        })

    except Exception as e:

        return jsonify({
            "output": "Internal Error:\\n" + str(e),
            "tokens": "",
            "ast": ""
        })


if __name__ == "__main__":
    app.run(debug=True)