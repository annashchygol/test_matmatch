# Algorithm description
 1. Read Input file into a DataFrame.
 2. Remove specific characters and whitespaces.
 3. Cleaning columns one by one.
 4. Check units and convert, once necessary.
 5. Add temperature association.
 
 
 ## Requirements: 
 * python >= 3.8
 * packages specified in requirements.txt
 
 
 ## How to run ?
 * By specifying one of the following:
   ["csv", "json", "xlsx"]
   to the `-o` or `--outformat` flag, user can specify output format.
 * By default xlsx file is created in the `out` folder. 
 
 
## Example: 
```python src/main.py -o json``` 
