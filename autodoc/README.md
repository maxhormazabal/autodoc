# Auto Documentation

Autodoc library aims to build a basic documentation for projects that follow the following structure:

```bash
-modules
--component
---useCase
---- usecase.py
---services
---- service.py
```

It works with `mkdocs` library and create a modules.md file catching every single docstring for services and usecases. 

## Install requirements

```bash
cd documentation
```

```bash
pip install -r autodoc/requirements.txt
```

## Init documentation

```bash
mkdocs serve
```
If port 8000 is already in use;

```bash
mkdocs serve -a localhost:8001
```

### Execute

```bash
python ./documentation/autodoc/generate_docs.py <code folder> ./documentation/docs
```

For example

```bash
python ./documentation/autodoc/generate_docs.py ./src ./documentation/docs
```