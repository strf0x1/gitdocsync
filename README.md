# gitdocsync
keep github project docs in sync with latest releases for ingestion into llm code editors and rags. 
  
# why
to work with llms effectively in llm code editors or rag systems, especially with libraries that are rapidly evolving like langchain or astro, you need
a way to reference the latest documentation to make sure your llm has the latest information when writing code. one way to do this is to supplement the llm 
with a RAG. a good example would be in open web ui, you can add knowledge bases that you reference when making a query using the '#' symbol. this project
just lets you define a simple json config file with the repos you want, and you can run it in a cron job to keep everything up to date.

# bootstrap
to run the first time, make sure you have git, python3, poetry and venv, then just use 'bootstrap.sh'. this will install the requirements and get everything 
set up. 

# running
after you have run the bootstrap, you can run the script manually with poetry using 'poetry run python docs_updater.py'. you can also put this in a cron job
to update the docs on a schedule.

# cron
To set up a cron job that runs the script every 2 hours, you can use the following steps:

1. Open your crontab file for editing:
   ```
   crontab -e
   ```

2. Add the following line to the file:
   ```
   0 */2 * * * cd ~/git/gitdocsync && poetry run python docs_updater.py
   ```

This cron job will:
- Run every 2 hours (0 */2 * * *)
- Change to the gitdocsync directory (cd ~/git/gitdocsync)
- Execute the script using poetry (poetry run python docs_updater.py)

Make sure to adjust the path if your gitdocsync directory is located elsewhere.

After saving the crontab file, the cron job will be active and will run the script every 2 hours, keeping your documentation up to date.


# logs
logs are stored in ./logs
  
