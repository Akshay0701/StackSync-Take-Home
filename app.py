import os
import sys
import tempfile
import subprocess
import json
import textwrap
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
PYTHON_CMD = "python"

@app.route('/execute', methods=['POST'])
def execute_script():
    # Parse and validate input JSON
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify(result=None, stdout="", error="Invalid JSON payload"), 400
    script = data.get('script')
    if not script or 'def main' not in script:
        return jsonify(result=None, stdout="", error="Script must define a main() function"), 400

    # Write user script and runner
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, 'user_script.py')
        runner_path = os.path.join(tmpdir, 'runner.py')

        with open(script_path, 'w') as f:
            f.write(script + '')

        runner_code = textwrap.dedent("""
            import json
            import user_script
            import sys

            try:
                result = user_script.main()
            except Exception as e:
                sys.argv = []
                sys.exit(1)

            print('@@RESULT_START@@')
            print(json.dumps(result))
            print('@@RESULT_END@@')
        """ )
        with open(runner_path, 'w') as f:
            f.write(runner_code)

        # Execute runner in subprocess
        proc = subprocess.Popen(
            [PYTHON_CMD, runner_path],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = proc.communicate()

    # On execution error, return stderr in stdout field
    if proc.returncode != 0:
        return jsonify(result=None, stdout=err.strip())

    # Extract JSON result
    if '@@RESULT_START@@' not in out:
        return jsonify(result=None, stdout=out.strip())

    pre, rest = out.split('@@RESULT_START@@', 1)
    json_part, post = rest.split('@@RESULT_END@@', 1)
    try:
        result = json.loads(json_part.strip())
    except json.JSONDecodeError:
        return jsonify(result=None, stdout=(pre + post).strip())

    return jsonify(result=result, stdout=(pre + post).strip())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)