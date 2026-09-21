# Tourist Destination Finder

Modular KivyMD starter project for a Tourist Destination Finder mobile app.

---

## Getting the Project Locally

### 1. Repository Access

This is a collaborative project. Team members should be added as **collaborators** to the repository by the project owner.

Once you have been added as a collaborator, clone the main repository:

```bash
git clone https://{access_token}@github.com/digreatbrian/tourist-destination-finder.git
cd tourist-destination-finder
```

Where:

- `access_token`: Your GitHub Personal Access Token used for authentication.
- `digreatbrian`: The repository owner's GitHub username.

### 2. Create a Branch

Do not work directly on the `main` branch.

Create a branch for your work:

```bash
git checkout -b {your_username}/{feature_name}
```

For example:

```bash
git checkout -b brian/destination-search
```

Keep your branch focused on one feature or task.

### 3. Push Your Changes

After making your changes:

```bash
git add .
git commit -m "Add destination search"
git push origin brian/destination-search
```

Replace the branch name with your actual branch name.

### 4. Create a Pull Request

Once your work is ready:

1. Push your branch to GitHub.
2. Open the repository on GitHub.
3. Create a Pull Request from your branch into `main`.
4. Describe what you changed.
5. Request a review if necessary.
6. Wait for the changes to be reviewed and merged.

> **Important:** Do not push directly to `main` unless you have been explicitly asked to do so.

---

## Installing Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

If it fails, you can alternatively use:

```bash
python -m pip install -r requirements.txt
```

If it continues to fail, try replacing `python` with `py` in the command. 
If None of this works, ensure you got Python installed.

---

## Quick Start

Run the application with:

```bash
python main.py
```

The application uses SQLAlchemy with a local SQLite database stored at
`~/.tourist_destination_finder/destinations.db`. Set the
`TOURIST_DESTINATION_DATABASE` environment variable to use a different database
path, such as a temporary database during tests.

---

## AI Assistance & Sean Mutevani

AI assistance is allowed. **Claude** and **Codex** are recommended.

Whether code is written manually or generated with AI, you and the AI must strictly follow the [CODE_STYLE_GUIDE.md](https://github.com/digreatbrian/tourist-destination-finder/blob/main/CODE_STYLE.md).

> **Important:** Contributions that do not follow the code style guide are prohibited, as they make collaboration and code maintenance more difficult.

---

## Collaboration

This project uses a **branch-based collaboration workflow**.

Each contributor should:

- Work on their own branch.
- Keep changes focused on their assigned task.
- Commit changes regularly with clear commit messages.
- Push their branch to the repository.
- Open a Pull Request when the work is ready.
- Respond to review feedback.
- Avoid making unrelated changes in the same Pull Request.

### Branch Naming

Use the following format:

```text
{your_username}/{feature_name}
```

Examples:

```text
brian/destination-search
john/home-screen
mary/destination-details
peter/map-integration
```

This makes it easier to identify who is working on what.

### Pull Requests

Pull Requests are used to review and merge changes into `main`.

Before opening a Pull Request:

- Make sure the application runs.
- Test your changes.
- Follow the code style guide.
- Make sure you haven't included unrelated changes.
- Write a clear description of what you changed.

---

## Resources

If you don't know how to create branches, commit, push, create Pull Requests, or perform other basic Git/GitHub operations, be ready to research them.

Don't spend too much time researching. Learn the basics, try them practically, make mistakes, fix them, and continue.

**Practical experience is the goal.**

---

## Team Roles

See [TEAM_ROLES.md](./TEAM_ROLES.md) for team roles and responsibilities.
