# Usage

The following are some configurations about how to use the aplication.

### Input File

The basic input methodology is as follows

Use _-f_ or _--file_ to specify the relative or full path to the document you want to parse.

```bash
python3 run.py <options> -f /path/to/my/file.csv
```

Use _-g_ or _--gui_ to specify the file using a system prompt

```bash
python3 run.py <options> -g
```

### Output file

Use _-o_ or _--output_ to specify the the file name of the output file, preferred without extension. In some cases more than one file will be generated, they will start with the given name. All the output will be at the /output directory.

```bash
python3 run.py <options> -o parsed
```

### AV engine

As of today, AV-Parser supports both [Kiuwan Vulns & Insights](../supported-formats/kiuwan.md), and [Qualys VMDR](../supported-formats/qualys.md), each one of them has its unique identifiers, refer to its documentation for all the options.

Use _-F_ or _--format_ to specify the format from the input file

```bash
python3 run.py <options> -F kiuwan-vulnerabilities
```

### Headers

Use _-H_ or _--headers_ to specify if the app headers do not want to be displayed. By default they will always be shown.

```bash
python3 run.py <options> -H
```

### Logs

As of today the apps makes use of the [_pwntools_](https://docs.pwntools.com/en/stable/index.html) library.&#x20;

Use _-l_ or _--log\_level_ to specify if the desired log level. By default they will be INFO.

```bash
python3 run.py <options> -l debug
```

### Clearing temp files

The application makes use of the system's internal storage in order to avoid overloading the internal memory in case of large files. They are stored in temporary directories, being deleted every time the computer is turned off.

Use _-C_ or _--clear_ to specify that all temporary files must be deleted once the application finishes successfully.

```bash
python3 run.py <options> -C
```







