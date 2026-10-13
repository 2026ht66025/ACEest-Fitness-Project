# ACEest Fitness & Gym
### Flask Application and DevOps Assignment

**GitHub Repository:** https://github.com/2026ht66025/ACEest-Fitness-Project

---

## Table of Contents

1. Project Overview
2. Objectives
3. Application Features
4. Technology Stack
5. Application Architecture
6. Prerequisites
7. Installation and Setup
8. Using the Application
9. Manual Testing
10. Automated Testing with pytest
11. Code Quality with Flake8
12. Git and GitHub Workflow
13. Docker Containerization
14. Continuous Integration with GitHub Actions
15. Continuous Integration with Jenkins
16. Project Structure
17. Database Design
18. Security and Data Handling
19. Troubleshooting
20. Submission Verification Checklist

---

## 1. Project Overview

ACEest Fitness & Gym is a gym management web application developed using Python and Flask. It provides a dark-and-gold dashboard for managing gym members, memberships, workout sessions, and weight measurements.

The application uses SQLite to store records and HTML/CSS to present an interactive web interface.

The project also demonstrates DevOps practices, including version control, automated testing, code-quality analysis, containerization, continuous integration, and technical documentation.

## 2. Objectives

The objectives of this project are to:

- Develop a functional web application for gym management.
- Organize application code into maintainable files and directories.
- Use Git and GitHub to maintain source-code history.
- Validate application behavior through automated tests.
- Check Python code quality using Flake8.
- Package the application and its dependencies using Docker.
- Automate testing and image building through GitHub Actions.
- Configure a Jenkins pipeline for independent build and test execution.
- Document installation, execution, testing, and troubleshooting procedures.

## 3. Application Features

### 3.1 Member Management

- Register members with their name, email, age, height, and weight.
- Select a membership plan: Monthly, Quarterly, Annual, or Expired.
- View registered members on the dashboard.
- Open an individual member profile.
- Reject duplicate email addresses.
- Validate required member details.
- Delete members and their associated workout and weight records.

### 3.2 Workout Management

- Record workouts for registered members.
- Store the workout name, duration, and notes.
- Display recent workouts on the dashboard.
- View workout history on an individual member profile.
- Validate workout details before saving.

### 3.3 Weight Tracking

- Record a member's weight over time.
- Store optional notes for each measurement.
- Display weight history on the member profile.
- Update the member's current registered weight.
- Calculate Body Mass Index (BMI) from the current weight and height.

**Note:** BMI is a general screening measure and is not a medical diagnosis.

### 3.4 User Interface

The application uses a dark background with gold accents, a navigation sidebar, summary cards, registration forms, and data tables. The layout is designed to remain usable on desktop and smaller screens.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web framework and HTTP routes |
| HTML | Web-page structure |
| CSS | Layout, styling, and responsive design |
| SQLite | Persistent application database |
| Git | Source-code version control |
| GitHub | Remote repository and collaboration |
| pytest | Automated testing |
| Flake8 | Code-quality and style checks |
| Docker | Container image creation and execution |
| GitHub Actions | Automated CI workflow |
| Jenkins | Pipeline-based build and test automation |

## 5. Application Architecture

The application follows a simple web-application architecture.

1. A user opens the application in a web browser.
2. The browser sends an HTTP request to the Flask application.
3. Flask processes the request using the appropriate route.
4. The application reads or updates data in SQLite when necessary.
5. Flask renders an HTML template or redirects the user.
6. The browser displays the resulting page.

The main components are:

- `app.py`: Flask routes, request handling, database operations, and application startup.
- `templates/`: HTML templates rendered by Flask.
- `static/`: CSS assets used by the interface.
- `instance/fitness.db`: Default local SQLite database.
- `tests/`: Automated tests for application behavior.

## 6. Prerequisites

For local development, install:

- Python 3.9 or a compatible version.
- pip, the Python package installer.
- Git.

For containerization, install Docker.

For the full DevOps workflow, a GitHub account and an accessible Jenkins server with the required plugins and tools are also needed.

## 7. Installation and Setup

### 7.1 Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/2026ht66025/ACEest-Fitness-Project.git
cd ACEest-Fitness-Project
```

### 7.2 Create a Virtual Environment

A virtual environment isolates the packages required by the project.

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

On Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 7.3 Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `requirements.txt` file defines the Flask, pytest, and Flake8 dependencies.

### 7.4 Start the Application

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

Keep the terminal open while using the application. Press `Ctrl+C` to stop the development server.

The application creates its SQLite database in the `instance` directory by default. The database location can be changed using the `FITNESS_DATABASE` environment variable.

## 8. Using the Application

### 8.1 Register a Member

1. Open the dashboard.
2. Locate the Register Member form.
3. Enter the member's name, email, age, height, and weight.
4. Select a membership plan.
5. Submit the form.
6. Confirm that the member appears in the Members table.

Each member must have a unique email address.

### 8.2 Record a Workout

1. Register a member if one does not already exist.
2. Locate the Record Workout form.
3. Select a member.
4. Enter the workout name and duration in minutes.
5. Add optional notes.
6. Save the workout.
7. Confirm that it appears in Recent Workouts.

### 8.3 View a Member Profile

1. Locate the member in the Members table.
2. Select View.
3. Review the member's details and BMI.
4. Review the weight and workout histories.

### 8.4 Record a Weight Measurement

1. Open the member profile.
2. Enter a positive weight value.
3. Add optional notes.
4. Save the measurement.
5. Confirm that the weight history contains the new record.

### 8.5 Delete a Member

1. Select Delete beside the member.
2. Confirm the browser prompt.
3. Verify that the member is removed.

Deleting a member also deletes associated workout and weight-history records. Use test records when demonstrating deletion.

## 9. Manual Testing

Manual testing verifies that the main features work through the browser.

| Test | Procedure | Expected result |
|---|---|---|
| Dashboard | Open the application home page | Dashboard and forms load |
| Member registration | Submit valid member details | Member appears in the table |
| Duplicate email | Register an existing email again | Duplicate-email message appears |
| Invalid member | Submit invalid or missing values | Validation message appears |
| Workout recording | Save a workout for a member | Workout appears in recent activity |
| Member profile | Select View for a member | Profile and BMI are displayed |
| Weight tracking | Add a weight measurement | New measurement is saved |
| Member deletion | Delete a test member | Member and associated records are removed |

Capture screenshots of the actual results for the assignment report.

## 10. Automated Testing with pytest

Automated tests check application behavior without requiring each feature to be tested manually.

### Run the Test Suite

Activate the virtual environment and run:

```bash
pytest -v
```

The current test suite contains nine tests covering:

1. Dashboard loading.
2. Member registration.
3. Duplicate email rejection.
4. Invalid member rejection.
5. Member profile and BMI.
6. Unknown member handling.
7. Workout recording.
8. Weight-measurement recording.
9. Member deletion.

The expected successful summary is:

```text
9 passed
```

The test fixture uses a temporary database so that automated tests do not overwrite the normal application database.

### Run a Single Test

For example:

```bash
pytest -v tests/test_app.py::test_dashboard_loads
```

### Test Execution in CI

Both the GitHub Actions workflow and Jenkins pipeline are configured to run pytest. The Docker image also includes the test files so the suite can be executed inside the container.

## 11. Code Quality with Flake8

Flake8 checks Python code for common errors and style issues.

### Critical Error Check

```bash
flake8 app.py tests --select=E9,F63,F7,F82
```

### General Code-Quality Check

```bash
flake8 app.py tests
```

Both commands should complete without reporting errors.

The `.flake8` configuration contains a narrowly scoped exception for the test module's import-path setup. The critical-error check remains enabled.

## 12. Git and GitHub Workflow

Git records project changes, while GitHub hosts the remote repository.

### 12.1 Check Repository Status

```bash
git status
```

### 12.2 Stage Changes

```bash
git add app.py tests Dockerfile requirements.txt
```

Stage other changed files as required, including the README and CI configuration.

### 12.3 Commit Changes

Use descriptive commit messages that explain the change.

```bash
git commit -m "Add automated tests and Docker support"
```

### 12.4 Inspect Commit History

```bash
git log --oneline --decorate
```

### 12.5 Push Changes

```bash
git push
```

For the first push of a new `main` branch, use:

```bash
git push -u origin main
```

### 12.6 Feature Branch Workflow

For work on a separate feature:

```bash
git switch -c feature/example-change
```

After making and testing changes:

```bash
git add .
git commit -m "Describe the feature or fix"
git push -u origin feature/example-change
```

Open a pull request on GitHub to propose merging the feature branch into `main`. Review the changes and CI results before merging.

Only claim that a branch or pull request was used if it was actually created and completed.

### 12.7 Files That Should Not Be Committed

The `.gitignore` file excludes generated and local files, including:

- Python virtual environments.
- Python cache files.
- pytest and Flake8 caches.
- The local `instance/` directory and database files.
- Environment files and coverage artifacts.

Do not commit credentials, access tokens, or private configuration.

## 13. Docker Containerization

Docker packages the application and its dependencies into an image that can be run in a container.

The project's `Dockerfile` uses a Python slim base image, installs the required packages, copies the application, templates, CSS, and tests, creates the database directory, and exposes port 5000.

### 13.1 Build the Image

Run from the project root:

```bash
docker build -t aceest-fitness:latest .
```

A successful build creates the `aceest-fitness:latest` image.

### 13.2 List the Image

```bash
docker images
```

### 13.3 Run Tests Inside the Container

```bash
docker run --rm --entrypoint python aceest-fitness:latest -m pytest -v
```

The expected result is nine passing tests.

### 13.4 Run the Web Application

```bash
docker run --rm -p 5000:5000 aceest-fitness:latest
```

Open:

http://127.0.0.1:5000

Stop the container with `Ctrl+C`.

### 13.5 Database Persistence

By default, the database created inside a container is stored in the container's writable layer. It is not persistent after the container is removed.

For local testing where the database must survive container removal, create a directory and mount it:

```bash
mkdir -p instance
docker run --rm -p 5000:5000 \
  -v "$(pwd)/instance:/app/instance" \
  aceest-fitness:latest
```

This example assumes the current directory is the project root.

## 14. Continuous Integration with GitHub Actions

The GitHub Actions workflow is located at:

`.github/workflows/main.yml`

### 14.1 Workflow Triggers

The current workflow runs when:

- Code is pushed to `main`.
- A pull request targets `main`.

### 14.2 Workflow Stages

The workflow performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.9.
3. Installs project dependencies.
4. Runs critical and general Flake8 checks.
5. Executes the pytest suite.
6. Builds a Docker image.
7. Runs pytest inside the Docker image.

### 14.3 View Workflow Results

1. Open the GitHub repository.
2. Select the Actions tab.
3. Select the ACEest Fitness CI workflow.
4. Open a workflow run.
5. Inspect each stage and its logs.

A green check mark indicates that the workflow completed successfully. A failed step must be inspected and corrected before considering the run successful.

## 15. Continuous Integration with Jenkins

Jenkins runs the pipeline defined in the root-level `Jenkinsfile`.

### 15.1 Pipeline Stages

The current pipeline contains:

1. **Checkout:** Retrieves source code using the configured SCM.
2. **Install Dependencies:** Creates a Python virtual environment and installs packages.
3. **Lint:** Runs Flake8 checks.
4. **Pytest:** Runs the tests and generates a JUnit XML report.
5. **Build Docker Image:** Builds an image tagged with the Jenkins build number.
6. **Pytest Inside Docker:** Executes the test suite inside the image.

The post-build section publishes the JUnit test report when available.

### 15.2 Prerequisites

The Jenkins environment must have:

- Git.
- Python 3 and pip.
- Docker.
- The Jenkins Pipeline plugin.
- The JUnit test-report plugin for publishing reports.
- Repository access and permission to run Docker commands.

The Jenkins service account must have the necessary permissions. Do not grant additional system privileges without understanding the security implications.

### 15.3 Configure the Jenkins Job

1. Open the Jenkins dashboard.
2. Create a new job of type Pipeline.
3. Open the job configuration.
4. Select **Pipeline script from SCM**.
5. Select **Git**.
6. Set the repository URL to:

   `https://github.com/2026ht66025/ACEest-Fitness-Project.git`

7. Set the branch specifier to `*/main`.
8. Set the script path to `Jenkinsfile`.
9. Save the job.
10. Select Build Now.

### 15.4 Verify a Build

1. Open the build.
2. Select Console Output.
3. Check the Checkout, Install Dependencies, Lint, Pytest, Docker build, and container-test stages.
4. Confirm that the build ends with:

```text
Finished: SUCCESS
```

If a build fails, use the console log to identify the first failing stage.

## 16. Project Structure

```text
ACEest-Fitness-Project/
├── .github/
│   └── workflows/
│       └── main.yml
├── static/
│   └── style.css
├── templates/
│   ├── client.html
│   └── dashboard.html
├── tests/
│   └── test_app.py
├── .flake8
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── README.md
├── app.py
└── requirements.txt
```

### File Descriptions

| File or directory | Description |
|---|---|
| `app.py` | Flask routes, validation, and database operations |
| `templates/dashboard.html` | Main dashboard |
| `templates/client.html` | Individual member profile |
| `static/style.css` | Dark-and-gold styling |
| `tests/test_app.py` | Automated test suite |
| `requirements.txt` | Python dependencies |
| `.flake8` | Flake8 configuration |
| `.gitignore` | Files excluded from Git |
| `Dockerfile` | Docker image instructions |
| `Jenkinsfile` | Jenkins pipeline definition |
| `.github/workflows/main.yml` | GitHub Actions workflow |
| `README.md` | Project and operating documentation |

The `instance/` directory is generated locally when the application creates its database. It is intentionally excluded from version control.

## 17. Database Design

The SQLite database contains three tables.

### Members

Stores member details, including name, email, age, height, weight, membership, and registration timestamp.

### Workouts

Stores workout records associated with members, including workout name, duration, notes, and timestamp.

### Weight History

Stores weight measurements associated with members, including weight, notes, and timestamp.

The workout and weight-history tables reference the members table. Foreign-key cascade deletion removes associated records when a member is deleted.

The application uses parameterized SQL queries for data operations.

## 18. Security and Data Handling

- Do not commit passwords, access tokens, or other credentials.
- Use environment variables for deployment-specific settings.
- The default Flask secret key is intended for development, not production.
- Use a strong, secret `SECRET_KEY` when deploying beyond a local lab.
- Restrict access to the application and database when handling real member information.
- Use test records for demonstrations and screenshots.
- Review container and Jenkins permissions before deployment.

The current application is a learning project. It does not implement user authentication or role-based access control.

## 19. Troubleshooting

### Flask Is Not Found

Activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### No Tests Are Collected

Confirm that `tests/test_app.py` exists and run:

```bash
pytest -v
```

### Flake8 Reports an Error

Read the filename and line number in the error message, correct the issue, and rerun both Flake8 commands.

### The Browser Cannot Open the Application

Confirm that Flask is running. Check that port 5000 is available and that the browser can reach the machine running the application.

### Docker Build Fails

Check that Docker is running, that the terminal is in the project root, and that the Dockerfile and required application files exist.

### Docker Permission Denied

Verify Docker service status and account permissions. On managed lab machines, follow the administrator's permission policy rather than changing system privileges indiscriminately.

### GitHub Actions Fails

Open the failed workflow in the Actions tab. Inspect the first failed stage and its logs, correct the issue, commit the change, and push again.

### Jenkins Fails

Inspect Console Output. Check repository access, Python installation, dependency installation, Docker permissions, and plugin availability.

### The Database Is Empty in a New Container

The container may have created a new database. Use a volume mount when persistent database storage is required.

## 20. Submission Verification Checklist

Use this checklist before submitting the assignment.

- [ ] Flask application starts and the dashboard loads.
- [ ] Member registration and validation work.
- [ ] Workout recording works.
- [ ] Member profiles, BMI, and weight history work.
- [ ] Automated tests pass.
- [ ] Critical Flake8 check passes.
- [ ] General Flake8 check passes.
- [ ] Docker image builds successfully.
- [ ] Tests pass inside Docker.
- [ ] Git commit history is present.
- [ ] Branch and pull-request workflow evidence is available, if required.
- [ ] GitHub Actions completes successfully.
- [ ] Jenkins completes successfully.
- [ ] README and source files are pushed to the public repository.
- [ ] Screenshots of successful results are saved for the submission report.

Do not mark a checklist item complete until its result has been verified.

---

**Repository:** https://github.com/2026ht66025/ACEest-Fitness-Project
## Git Branching and Pull Request Workflow

The project uses feature branches to develop changes separately from the main branch. This allows changes to be reviewed before they are merged into the main codebase.

### Workflow

1. Create a feature branch from `main`.
2. Make the required changes and test them locally.
3. Commit the changes with a descriptive commit message.
4. Push the feature branch to GitHub.
5. Open a pull request targeting `main`.
6. Review the changes and verify the CI checks.
7. Merge the pull request after the checks pass.

### Example Git Commands

```bash
git switch main
git pull origin main
git switch -c feature/example-change

# Make and test your changes
git add README.md
git commit -m "Document feature branch workflow"
git push -u origin feature/example-change
```

After pushing, create a pull request on GitHub from the feature branch into `main`.

This workflow improves traceability, supports code review, and helps prevent untested changes from being merged directly into the main branch.
