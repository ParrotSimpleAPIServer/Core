import os
import time
start_time = time.time()
import sys
import tomllib
from flask import Flask, request, make_response, Response
from waitress import serve
import rich
from rich.panel import Panel

PATH_plugins = str(os.path.abspath('.'))+'\\plugins'
sys.path.append(PATH_plugins)
PSAScore = globals()

try:
    import i18n
except:
    print("[FatalError] Can't load 'i18n.py', please fix this problem.")
    sys.exit(1)

version = "1.0.beta2"
api_version = 1.0

lang = i18n.en_us

def prefix(dtype):
    """
    i:Info
    w:Warn
    e:Error
    """
    prefix_list = {"i":"[cyan]Info[/]","w":"[yellow]Warn[/]","e":"[red]Error[/]"}
    return(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}][{prefix_list[dtype]}]")

def rp(text):
    rich.print(f"{text}")

def reponses(data_block):
    status = data_block['code']
    messages = data_block['msg']
    contents = data_block['data']
    response_data = make_response({'status':status, 'message':messages, 'data':contents}, status)
    response_data.headers['Access-Control-Allow-Origin'] = "*"
    return response_data

dirs = ['plugins', 'configs', 'statics']
rp(f'{prefix("i")}{lang.server.start.dircheck}')
for i in dirs:
    if not os.path.isdir(i):
        rp(f"{prefix('i')}{lang.server.start.dircreate}'{i}'")
        os.makedirs(i)

rp(f'{prefix("i")}{lang.server.start.loadconfig.info}')
try:
    if os.path.isfile('configs/main.toml'):
        with open('configs/main.toml','rb') as file_temp:
            Main_config = tomllib.load(file_temp)
    else:
        with open('configs/main.toml','w') as file_temp:
            file_temp.write(f'''[Server]\n\nPort = 5000\n#{lang.server.confignote.server.port}\n\nThreads = 4\n#{lang.server.confignote.server.threads}\n\nConnectionLimit = 100\n#{lang.server.confignote.server.connectionlimit}\n\nSendDebugInfo = true\n#{lang.server.confignote.server.senddebuginfo}\n\n[Plugins]\n\nURL = "api"\n#{lang.server.confignote.plugins.url}\n\nCheckApiVersion = true\n#{lang.server.confignote.plugins.checkapiversion}\n\nAvoidFunctionOverride = true\n#{lang.server.confignote.plugins.avoidfunctionoverride}\n\n[Statics]\n\nEnabled = true\n#{lang.server.confignote.statics.enabled.t1}\n#{lang.server.confignote.statics.enabled.t2}\n\nWhiteList = true\n#{lang.server.confignote.statics.whitelist}\n\n[Debugger]\n\nEnabled = true\n#{lang.server.confignote.debugger.enabled.t1}\n#{lang.server.confignote.debugger.enabled.t2}''')
        rp(f"{prefix('w')}Config file has created , please restart PSAS")
        sys.exit(0)
    if os.path.isfile('configs/staticswhitelist.txt'):
        with open('configs/staticswhitelist.txt','r', encoding='utf-8') as file_temp:
            statics_whitelist = file_temp.read().rstrip('\n')[1:]
    else:
        with open('configs/staticswhitelist.txt','w') as file_temp:
            file_temp.write("# Each line corresponds to a file name, and the first line will be regarded as a comment and will not be read.")
        statics_whitelist = []
except Exception as e:
    rp(f"{prefix('e')}{lang.server.start.loadconfig.fail}: {e}")
    sys.exit(1)

rp(f'{prefix("i")}{lang.server.start.scanplugin}...')
exes = os.listdir('plugins')
mounted_plugins = []
plugins_register = {}

plugins_count = 0
for i in exes:
    plugins_count += 1
    rp(f"{prefix('i')}{lang.server.start.loading.info}'{i}'({plugins_count}/{len(exes)})")
    try:
        exec(f"import {i}")
        try:
            exec(f"one_plugins_register_temp = {i}.register")
            conflict_list = list(set(plugins_register) & set(one_plugins_register_temp.commands))
            if Main_config['Plugins']['AvoidFunctionOverride']:
                if len(conflict_list) != 0:
                    rp(f"{prefix('w')}{lang.server.start.loading.registeroverridewarn.text.front}'{i}'{lang.server.start.loading.registeroverridewarn.text.behind}")
                    for i in conflict_list:
                        rp(f"{i}[{one_plugins_register_temp.commands[i]}] -> {plugins_register[i]}")
                        one_plugins_register_temp.commands.pop(i)
        except AttributeError:
            rp(f"{prefix('e')}{lang.server.start.loading.invalidregisterwarn.text.front}'{i}'{lang.server.start.loading.invalidregisterwarn.text.behind}")
            break
        plugins_register.update(one_plugins_register_temp.commands)
        if Main_config['Plugins']['CheckApiVersion']:
            if one_plugins_register_temp.version != api_version:
                rp(f"{prefix('w')}{lang.server.start.loading.apiversionwarn.text.front}'{i}'{lang.server.start.loading.apiversionwarn.text.behind}: {one_plugins_register_temp.version} -> PSAS:v{api_version}")
        mounted_plugins.append(i)
    except Exception as e:
        rp(f"{prefix('e')}{lang.server.start.loading.loadfail.text.front}'{i}'{lang.server.start.loading.loadfail.text.behind}: {e}")

rp(f'{prefix("i")}{lang.server.start.indexpage.info}')
try:
    with open('index.html','r') as file_temp:
        index_page = file_temp.read()
except Exception as e:
    rp(f"{prefix('e')}{lang.server.start.indexpage.fail}: {e}")
    index_page = "ParrotSimpleAPIServer"

end_time = time.time()

rich.print(Panel(f'''{lang.server.infopanel.port}: {Main_config["Server"]["Port"]}
{lang.server.infopanel.threads}: {Main_config["Server"]["Threads"]}
{lang.server.infopanel.connectionlimit}: {Main_config["Server"]["ConnectionLimit"]}
{lang.server.infopanel.loadtime}: {"{:.2f}s".format(end_time - start_time)}
{lang.server.infopanel.mountcount}: {len(mounted_plugins)}/{len(exes)} [{str(round((len(mounted_plugins)/len(exes))*100))+'%' if len(exes)!=0 else "None"}]
{lang.server.infopanel.apiversion}: v{api_version}
{lang.server.infopanel.register}: {len(plugins_register)}'''
,title=f"ParrotSimpleAPIServer v{version}"))

if __name__ == "__main__":
    app = Flask(__name__)
else:
    rp(f"{prefix('e')}This program was called as a function.")
    sys.exit(1)

app.config['DEBUG'] = True

@app.route('/')
def index():
    index_temp = ""
    for i in plugins_register.keys():
        index_temp += f"  \n[{i}](/{Main_config['Plugins']['URL']}/{i})  \n> **{plugins_register[i]}**  \n"
    index_temp = index_page.replace("[[STATUS]]",index_temp)
    return index_temp, 200
    
@app.route('/statics/<files>')
def styles(files):
    if Main_config['Statics']['Enabled']:
        if Main_config['Statics']['WhiteList']:
            if files in statics_whitelist:
                cansend = True
            else:
                cansend = False
        else:
            cansend = True
        if cansend:
            try:
                with open(f'statics/{files}','rb') as file_temp:
                    return file_temp.read()
            except Exception as e:
                return reponses({'code':500 , 'msg':f"{lang.client.errors.statics.internal}: {e}", 'data':''})
        else:
            return reponses({'code':404 , 'msg':f"{lang.client.errors.statics.notfound}", 'data':''})
    else:
        return reponses({'code':403 , 'msg':f"{lang.client.errors.statics.disabled}", 'data':''})

@app.route(f'/{Main_config["Plugins"]["URL"]}/<functions>', methods=['GET','POST', 'OPTIONS'])
def run_main(functions):
    if functions in plugins_register:
        input_api_data = {
            'client':{
                'request':{
                        'urlparams':request.args.to_dict(),
                        'data':request.data,
                        'method':request.method,
                        'head':request.headers
                    }
            },
            'server':{
                'data':{
                        'globals':PSAScore.copy().pop('PSAScore')
                },
                'info':{
                        'version':version,
                        'apiversion':api_version
                }
            }
        }
        action_temp = f"{plugins_register[functions]}(input_api_data)"
        if len(plugins_register[functions].split(".")) == 1:
            rp(f"{prefix('w')}{lang.client.errors.mainfunction.voidregistry.text.front}'{plugins_register[functions]}'{lang.client.errors.mainfunction.voidregistry.text.behind}")
        try:
            plugin_output = eval(action_temp)
            if type(plugin_output) == str:
                return plugin_output
            elif type(plugin_output) == Response:
                return plugin_output
            else:
                return reponses(plugin_output)
        except Exception as e:
            rp(f"{prefix('e')}'{plugins_register[functions]}': {e}")
            if Main_config["Server"]["SendDebugInfo"]:
                return reponses({'code':500 , 'msg':f"{lang.client.errors.mainfunction.failure.allowoutput.text.front}'{plugins_register[functions]}'{lang.client.errors.mainfunction.failure.allowoutput.text.front}: {e}", 'data':'Please contact the administrator'})
            else:
                return reponses({'code':500 , 'msg':f"{lang.client.errors.mainfunction.failure.notallowoutput.text}'{plugins_register[functions]}'", 'data':'Please contact the administrator'})
    else:
        return reponses({'code':404 , 'msg':f'{lang.client.errors.mainfunction.failure.invalidurl.text}', 'data':''})

@app.route('/PSASinfo')
def info_page():
    return str({'PSAS':f'{version}', 'API':f'{api_version}'})

@app.route('/debugger/<options>')
def run_debugger(options):
    if Main_config["Debugger"]["Enabled"]:
        if options == "plugins":
            return str({'mounted_plugins':{str(mounted_plugins)}, 'plugins_register':{str(plugins_register)}})
        elif options == "globals":
            return str(PSAScore)
        elif options == "params":
            return str(request.args.to_dict())
        else:
            return str("None")
    else:
        return reponses({'code':403 , 'msg':f"{lang.client.errors.debugapi.disabled.text}", 'data':''})

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=Main_config["Server"]["Port"], threads=Main_config["Server"]["Threads"], connection_limit=Main_config["Server"]["ConnectionLimit"], ident=f'PSAS/{version}')
