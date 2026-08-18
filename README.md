# About PSAS

PSAS is a plugin-based API server that implements plugin mounting using module import methods.

Language：en_us [zh_cn](README_zhcn.md)

# Features

* Minimalist single-file core
* Multi-language support
* Compatible with both PSAS-format responses and Flask native responses
* Plugin conflict detection
* Dedicated debugging interface and static file storage folder
* Easy-to-read TOML configuration files

# Deployment
> The virtual environment deployment method is not provided here for now.

1. Create a folder to store PSAS/Core
```bash
mkdir PSAS && cd PSAS
```
2.Clone this repository locally
```bash
git clone https://github.com/ParrotSimpleAPIServer/Core.git
```
3.Switch to the folder
```bash
cd Core
```
4.Install dependencies
```bash
pip install -r requirements.txt
```
5.Download the i18n support files from the warehouse and place them in the Core folder.
`https://github.com/ParrotSimpleAPIServer/i18n/blob/main/i18n.py`

6.Start
```bash
python main.py
```
PSAS will automatically create folders and configuration files on the first startup.  
Typically these files are:
* plugins/
* statics/
* configs/main.toml
* configs/staticswhitelist.txt

# Plugin System
The plugin file structure is similar to Python modules.  
For plugin writing specifications, please refer to the wiki of this repository.   
You can download the example plugin from the [ExamplePlugin](https://github.com/ParrotSimpleAPIServer/ExamplePlugin) repository for demonstration.

> [!CAUTION]
> Plugins have the ability to directly execute commands. Installing unvetted plugins may lead to system attacks!

> This page translated using machine translation, which inevitably leads to inaccuracies. 
