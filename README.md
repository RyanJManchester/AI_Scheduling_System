# AI Inspection Scheduling software

### Database

<details>

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
</details>

### Folder Structure

<details>
    <summary> Details about the folder structure for the repository</summary>

##### Root Files
- **package.json**: Contains the metadata, dependencies, scripts and npm build commands
- **package-lock.json**: Locks the version of all packages for consistent dependencies across installs
- **requirements.txt**: Specifies python dependencies for backend

##### `database/`
- Contains `.sql` files and database management scripts

##### `frontend/`
- Contains the frontend gui, including typescript

    - **index.html**: The entry point for every user.
    - **tsconfig.json**: Configures Typescript compilation to javascript, and sets version specification
    - **dist/**: Houses all the compiled javascript from ts
    - **src/**: Contains Typescript source code and resources.
        -**app.ts**: Main Typescript file associated with `index.html`
        - **components/**: Smaller `.ts` files to break down the typescript into manageable chunks.
    - **styles/**:Contains all the `.css` and styling code for the GUI.

##### `backend/`
- Contains the code for the application backend

    - **inspection_scheduling**: main application code
    - **api_utils**: Contains functions for API calls to external services
    - **env.example**: how the .env file should be setup
    - **.env file**: For secure storage of API keys


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