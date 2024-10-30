# AI Inspection Scheduling software

### Database

<details>

### Creating and Populating SQLite Tables Using SQL Files

### Step 1: Ensure SQLite is Installed

Before proceeding, ensure that the SQLite executable is downloaded and accessible. You can download it from the [SQLite official website](https://www.sqlite.org/download.html). Follow the installation instructions for your operating system.

### Step 2: Open Command Line or Terminal

Open your command line (Windows Command Prompt, or Terminal on macOS/Linux).

### Step 3: Launch SQLite

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
</details>

### Folder Structure

<details>
    <summary> Details about the folder structure for the repository</summary>

**package.json**
specifies all the metadata, dependencies, scripts and npm build commands
**package-lock.json**
locks the version of all packages, so that anyone who clones our repo and runs
npm install has the same dependencies and sub-dependencies, making it reproduceable.
**requirements.txt**
specifies python dependencies. may not be needed.
**database folder**
houses all the .sql and database management
**frontend folder**
all the frontend gui, including the typescript
- index.html:
    the starting point for every user.
- tsconfig.json:
    configures the tss compilation to js, speficy;s versions etc.
- dist folder:
    houses all the compiled javascript from ts
- src:
    the typescript folder and resources.
    app.ts - the main ts associated with index.html
    components folder
        - smaller .ts files to break down the typescript into
            manageable chunks.
- styles:
    all the .css and styling code for the GUI's.

**backend folder**
houses the code for the application
- ?python main application code
- env.example file - how the .env file should be setup and
- .env file; secure api key storage for third party API's



</details>

### Commands

<details>

##### **Install Dependencies**

```bash
npm install
```

##### **Build Frontend TypeScript**

```bash
npm run build:ts
```

##### **Run Backend Server (FastAPI)**

```bash
npm run start:backend
```

##### **Serve Frontend Files with Lite-Server**

```bash
npm run start:frontend
```

##### **Run Both Backend and Frontend Concurrently**

```bash
npm run start
```

#### **Run All Tests**

```bash
npm run test
```

#### **Adding a new runtime dependenciy / installation**

```bash
npm install <package-name> --save
```
#### **Adding a new development dependency / installation**

```bash
npm install <package-name> --save-dev
```
#### **Clean Build Output (Remove `dist/` Files)**

```bash
npm run clean
```

</details>