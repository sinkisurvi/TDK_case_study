from flask import Flask
from flask_executor import Executor
from flask_shell2http import Shell2HTTP


''' 
Purspose of this file is to create an endpoint so that airflow container can 
execute spark-submit job remotely to spark-container
'''
app = Flask(__name__)

executor = Executor(app)
shell2http = Shell2HTTP(app=app, executor=executor, base_url_prefix="/commands/")

def on_shell_run(context, future):
  print(context, future.result())

shell2http.register_command(endpoint="pyspark", command_name="spark-submit", callback_fn=on_shell_run, decorators=[])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)