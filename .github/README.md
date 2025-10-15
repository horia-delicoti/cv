[![Build](https://github.com/horia-delicoti/cv/actions/workflows/compile.yml/badge.svg)][workflow_compile]
[![Validate](https://github.com/horia-delicoti/cv/actions/workflows/validate.yml/badge.svg)][workflow_validate]
[![Tag](https://github.com/horia-delicoti/cv/actions/workflows/tag.yml/badge.svg)][workflow_tag]
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)][mit]
[![Made with LaTeX](https://img.shields.io/badge/Made%20with-LaTeX-blue.svg)][latex]

<h1 align="center">🧑‍💻 Horia Delicoti - CV</h1>
<p align="center">
<a href="https://github.com/horia-delicoti/cv"><img src="./images/cv-logo.png" width="48"/></a><br>
<i>This repo contains the source for my personal CV</i>
<br />
<i>A PDF <a href="https://www.latex-project.org/">(LaTeX)</a> auto-built from <a href="https://jsonresume.org/">JSON Resume</a> data</i>
<br />
<b> 📄 <a href="https://github.com/horia-delicoti/cv/releases/latest/download/Horia_Delicoti_CV.pdf"><code>Horia-Delicoti-CV.pdf</code></a></b> <br />
</p>

## 💡 Motive

Instead of writing my resume manually in Word, PDF, or LaTeX, I maintain it as a structured JSON data then use scripts to automatically generate a LaTeX and PDF version.

## 🧠 About

The resume content is defined in [`resume.yml`](/resume.yml) following the [jsonresume.org][json_resume] standard, and validated
against [`schema.json`](/schema.json) using [`validate.py`](/lib/validate.py).
A [`LaTeX document`](/tex/resume.tex) is then generated from [`template.jinja`](/template.jinja) using [`generate.py`](/lib/generate.py)
and [`compiled`](/lib/compile.py) to PDF using [pdflatex][pdflatex]. The final PDF is automatically generated in [`out/resume.pdf`](/out/).
The entire process: from `YAML` → `LaTeX` → `PDF` is fully automated via the [`Taskfile`](/Taskfile.yml).

## 🚀 Getting Started

### ⚙️ Prerequisite

To run this project, you need **[Task][taskfile]** and **[Python3][python3]** installed on your machine.
[Latex][latex] will be installed by the [Taskfile](/Taskfile.yml#L69) _([MacTeX][mactex] on macOS and [TeX Live][texlive] on Linux)_

- **🍎 macOS**

```sh
brew install go-task
brew install python3
```

- **🐧 Linux**

```sh
sudo apt update
sudo apt install python3 python3-venv python3-pip curl -y
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
```

### 🧪 Usage - Local

```sh
# Clone the repo
git clone https://github.com/horia-delicoti/cv.git && cd cv

# Modify resume data
vim resume.yml

# Check all available commands
task help

# Or simply run everything (install deps, validate, generate, compile).
task all -v OUTPUT_PDF=out/<your_name>_CV.pdf # Optionally specify the output PDF file name using `OUTPUT_PDF` variable
```

<details>
  <summary>Commands</summary>

- `task help`        - Show help message
- `task all`         - Install dependencies, validate, generate and compile
- `task venv`        - Create a Python virtual environment if it doesn't exist
- `task install`     - Install required Python dependencies
- `task install-tex` - Install TeX Live (Linux) or MacTeX (macOS)
- `task validate`    - Validate YAML content against the JSON schema
- `task generate`    - Generate LaTeX file from YAML and Jinja2 template
- `task compile`     - Compile PDF from LaTeX file

</details>

```mermaid
flowchart LR
    %% Direction: left-to-right
    %% Nodes
    A[📝 resume.yml<br/>schema.json] -->|validate.py| B[✅ Validation]
    B -->|generate.py + template.jinja| C[📃 LaTeX document<br/>resume.tex]
    C -->|compile.py + pdflatex| D[📄 out/resume.pdf]
```

### 🎨 Customize

You can modify the resume by editing the [`resume.yml`](/resume.yml) file, following the [JSON Resume standard](https://jsonresume.org/).
You can also customize the LaTeX template located at [`template.jinja`](/template.jinja) to change the layout and design of the resume.
All the scripts are located in the [`/lib`](/lib) directory.
They are triggered by the [`Taskfile`](/Taskfile.yml)

### 📸 Screenshot

<h3 align="center">📄 PDF</h3>
<p align="center"><img src="./screenshots/screenshot-pdf.png" width="350" alt="Generated PDF preview preview"/</p>

## 🤝 Contributing

No need to contribute or raise issues. Just fork the repo and make the changes you need for your own CV.

## 🙌 Attributions

### Contributors

![Contributors](https://readme-contribs.as93.net/contributors/horia-delicoti/cv)

## 🫡 Acknowledgements

Thanks to [Lissy93 CV](https://github.com/Lissy93/cv) for the inspiration and [dwmkerr makefile-help](https://github.com/dwmkerr/makefile-help) for the Makefile template.

## 📚 Resources

### 🧩 Data & Templates

- [JSON](https://www.json.org/json-en.html) - A lightweight data interchange format that is easy for humans to read and write, and easy for machines to parse and generate.
- [JSON Resume](https://jsonresume.org/) - The open source initiative to create a JSON-based standard for resumes.
- [jsonschema](https://pypi.org/project/jsonschema/) - An implementation of JSON Schema for Python.
- [PyYAML](https://pypi.org/project/PyYAML/) - A YAML parser and emitter for Python.
- [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) - A modern and designer-friendly templating language for Python.

### 🐍 Python Libraries for LaTeX & PDF Generation

- [PyLaTeX](https://jeltef.github.io/PyLaTeX/current/) - A Python library for creating and compiling LaTeX files or snippets.
- [pdflatex](https://pypi.org/project/pdflatex/) - A simple wrapper around the pdflatex command to compile LaTeX files from Python.
- [RenderCV](https://github.com/rendercv/rendercv) - A tool to generate a PDF resume from JSON Resume schema using LaTeX templates.
- [Coloroma](https://github.com/tartley/colorama) - A simple cross-platform colored terminal text in Python.

### 🧮 LaTeX & TeX Distributions

- [LaTeX](https://www.latex-project.org/) - A high-quality typesetting system; it includes features designed for the production of technical and scientific documentation.
- [TeX Live](https://www.tug.org/texlive/) - A comprehensive TeX system that includes all the major TeX-related programs, macro packages, and fonts that are free software.
- [MacTeX](https://tug.org/mactex/) - A TeX distribution for macOS that includes TeX Live, a full set of TeX-related programs, macro packages, and fonts.

### ⚙️ Build & Utility Tools

- [Task](https://taskfile.dev/) - A simple task runner / build tool that aims to be simpler and easier to use than Make.
- [PNG Egg](https://www.pngegg.com/) - A free online tool to convert SVG to PNG and get transparent background images.
- [Mermaid](https://mermaid-js.github.io/mermaid/#/) - A JavaScript-based diagramming and charting tool that renders Markdown-inspired text definitions to create and modify diagrams dynamically.
- [Shields.io](https://shields.io/) - A service that provides a simple way to create consistent and customizable badges for open source projects.

## ⚖️ License

This project is licensed under the [MIT][mit] License. See the [LICENSE](/LICENSE) file for details.

<!-- License + Copyright -->
<p  align="center">
  <i>© <a href="https://horia.delicoti.com">Horia Delicoti</a> 2025</i><br>
  <i>Licensed under <a href="https://www.tldrlegal.com/license/mit-license">MIT</a></i><br>
  <a href="https://github.com/horia-delicoti"><img src="./images/octocat_spiderman.png" width="100" /></a><br>
  <sup>Happy exploring 🙂</sup>
</p>

[json_resume]: https://jsonresume.org/
[pdflatex]: https://pypi.org/project/pdflatex/
[latex]: https://www.latex-project.org/
[mactex]: https://formulae.brew.sh/cask/mactex
[texlive]: https://www.tug.org/texlive/
[mit]: https://opensource.org/licenses/MIT
[python3]: https://www.python.org/downloads/
[taskfile]: https://taskfile.dev/docs/installation
[workflow_validate]: https://github.com/horia-delicoti/cv/actions/workflows/validate.yml
[workflow_compile]: https://github.com/horia-delicoti/cv/actions/workflows/compile.yml
[workflow_tag]: https://github.com/horia-delicoti/cv/actions/workflows/tag.yml

<!-- Ambition Brew -->
<!--
   ( (
    ) )
  ........
  | CV ☕ |]
  \      /
   `----'
-->