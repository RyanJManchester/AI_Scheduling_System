# AI Inspection Scheduling software


#### Creating and Populating SQLite Tables Using SQL Files


##### Step 1: Ensure SQLite is Installed
Before proceeding, ensure that the SQLite executable is downloaded and accessible. You can download it from the [SQLite official website](https://www.sqlite.org/download.html). Follow the installation instructions for your operating system.

##### Step 2: Open Command Line or Terminal
Open your command line (Windows Command Prompt, or Terminal on macOS/Linux).

##### Step 3: Launch SQLite
Navigate to the directory where your SQLite executable is located (if it’s not in your PATH). Use the `cd` command to change directories.

Start SQLite with the following command:

```bash
sqlite3 inspection_scheduling_system.db
#once inside SQLite db
.read path_to_your_file/init_tables.sql
.read path_to_your_file/populate_tables.sql
.tables #optional: to list tables
select * from Inspector #optional: list inspectors in Inspector table
.exit #exit SQLite
```

