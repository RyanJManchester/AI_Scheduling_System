# AI Inspection Scheduling software

### Database

<details>

### Creating and Populating PostgreSQL Tables Using SQL Files

#### Step 1: Ensure Postgres is Installed

Make sure PostgreSQL is installed and accessible. You can download it from the [PostgreSQL official website](https://www.postgresql.org/download/) and follow the installation instructions for your operating system.

Before proceeding, ensure that Postgressql. You can download it from the [PostgreSQL Download](https://www.sqlite.org/download.html). Follow the installation instructions to donwload it on an ubuntu server.

##### Step 2: Launch PostgreSQL

1. Start by opening the PostgreSQL command line tool (psql). If you are not logged in as the PostgreSQL user, you may need to switch to the PostgreSQL user. Use the following command:

```bash
sudo -i -u postgres
```
2. Create a new database and connect to it

```bash
createdb inspection_scheduling
psql -d inspection_scheduling
```

3. Once inside, run the SQL files to create and poppulate tables
```bash
\i path_to_your_file/init_tables.sql
\i path_to_your_file/populate_tables.sql
\i path_to_your_file/views_and_procedures.sql
\dt #optional: list the tables in the db
select * from inspector; #optional: check data in inspector table
\q #exit postgres
createdb inspection_scheduling
psql -d inspection_scheduling
```

3. Once inside, run the SQL files to create and poppulate tables
```bash
\i path_to_your_file/init_tables.sql
\i path_to_your_file/populate_tables.sql
\i path_to_your_file/views_and_procedures.sql
\dt #optional: list the tables in the db
select * from inspector; #optional: check data in inspector table
\q #exit postgres
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

    - **inspection_scheduling**: Contains functions for the processes required to schedule an inspection
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