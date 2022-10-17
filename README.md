---
description: >-
  AV-Parser is a project that aims to be able to parse, as expected, and
  generate reports from the most common AV engines available.
---

# AV-Parser

***

***

***

### Installation

For now the API is under construction and it is not known when it will be publicly available, so the only option is to clone the repository and install it locally.

Fisrt, start by cloning the repository.

```bash
git clone https://github.com/dpuenteramirez/AV-Parser.git
```

Once this is done, access the repository directory and install all Python dependencies. You can use a pyenv or a Conda virtual env, both configuration files are provided.

```bash
# Navigate to the repository directory
cd ./AV-Parser

# pyenv usage
python3 install -r req.pip

# Conda usage
conda env create -f av-parser.yml
```

It is now ready to be used locally.



### Usage

One of the key features is simplicity, from the end user's point of view, the less the user has to do the better.



If you do not want to keep entering manually the company info, there is a file under /data which can be named as _company.csv_, the app will check for its existance and correct format, in case everything checks, it will extrar the information. The expected format is as follows:

| company cod | component | year | starting id |
| ----------- | --------- | ---- | ----------- |
| d3x3r       | MyAPP     | 2022 | 1           |



The basic invocation is as follows, for specific usage based on the AV engine please refer to its wiki page.

```bash
python3 run.py <options>
```

***

### Troubleshooting

It is known that in some cases when using Conda, at least on the latest version of MacOS and Debian, it can fail some times when launching the app. An alternative is to run it as follows:

```bash
conda run --no-capture-output -n AV-PARSER python run.py <options>
```

