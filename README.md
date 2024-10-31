# AI Inspection Scheduling software

### Database

<details>

### Creating and Populating PostgreSQL Tables Using SQL Files

#### Step 1: Ensure SQLite is Installed

Make sure PostgreSQL is installed and accessible. You can download it from the [PostgreSQL official website](https://www.postgresql.org/download/) and follow the installation instructions for your operating system.


#### Step 2: Open Command Line or Terminal

Open your command line (Windows Command Prompt, or Terminal on macOS/Linux).

#### Step 3: Connect to PostgreSQL

**Connect to PostgreSQL**: Use the `psql` command to connect to your PostgreSQL database. Replace `your_username` and `your_database_name` with your PostgreSQL username and database name:
   ```bash
    psql -U your_username -d your_database_name
   ```
#### Step 4. Execute SQL scripts

```bash
    \i 'path_to_your_file/init_tables.sql'
    \i 'path_to_your_file/populate_tables.sql'

    \dt #optional: list tables
    select * from inspector; #optional: check data in inspector table
    \q #exits postgres
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