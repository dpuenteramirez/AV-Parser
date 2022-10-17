# Full usage examples

```bash
# Execute Qualys WAS
conda run --no-capture-output -n AV-PARSER python run.py -F qualys-vmdr -f '/Users/d3x3r/Documents/AV-Parser/data/Qualys/vmdr' -l debug -o vmdr -C

# Execute Kiuwan Vulnerabilities
conda run --no-capture-output -n AV-PARSER python run.py -F kiuwan-vulnerabilities -f '/Users/d3x3r/Documents/AV-Parser/data/Kiuwan/App1/Vulnerabilities.csv' -l debug -C

# Execute Kiuwan Components/Insights
conda run --no-capture-output -n AV-PARSER python run.py -F kiuwan-insights-components -f '/Users/d3x3r/Documents/AV-Parser/data/Kiuwan/App1/Components.csv' -l debug -C

# Execute Kiuwan Security
conda run --no-capture-output -n AV-PARSER python run.py -F kiuwan-insights-security -f '/Users/d3x3r/Documents/AV-Parser/data/Kiuwan/App1/Security.csv' -l debug -C

# Execute Kiuwan License
conda run --no-capture-output -n AV-PARSER python run.py -F kiuwan-insights-license -f '/Users/d3x3r/Documents/AV-Parser/data/Kiuwan/App1/License.csv' -l debug -C

# Execute Kiuwan Obsolescence
conda run --no-capture-output -n AV-PARSER python run.py -F kiuwan-insights-obsolescence -f '/Users/d3x3r/Documents/AV-Parser/data/Kiuwan/App1/Obsolescence.csv' -l debug -C

# Execute Kiuwan Full
conda run --no-capture-output -n AV-PARSER python run.py -F kiuwan-full -f '/Users/d3x3r/Documents/AV-Parser/data/Kiuwan/App1/' -l debug -C 

```
