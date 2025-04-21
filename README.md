# Discord Course Discussion Tracker Bot  

A Discord bot that will ease the burden of keeping track of who is participating in discussion posts.

Language: Python  
Framework: `discord.py`

## Intended Functionality  


- Track students' posts in discussion post threads  
- Give word count of messages  
- Time of messages vs time of thread creation (diff -- how late was it?)  
- Each thread should have at least 2 posts (answer/reply)  
- Message can additionally be saved for visual verification  

- Output where?  
    - Google spreadsheet (via [Sheety API](https://sheety.co/docs/authentication.html))  
    - HTML output  
    - Actual database?

---  

## Pain Points  

- Identifying which thread belongs to which course/unit/discussion question #  
    - Maybe add a Discord command:  
      ```bash  
      !dp admin 1 1  
      ```
      Admin course discussion post, unit 1, discussion post 1.  

- Creating database schema/format of data.



## Local Testing

Set up a Python virtual environment:
```bash
python3 -m venv venv
```
This generates the virtual environment files.  

Then, activate the virtual environment by sourcing the `activate` shell script that
was generated.  
```bash
. venv/bin/activate
```
The venv is now active, and you can install project-specific dependencies.  
```bash
pip install -U discord.py
```



