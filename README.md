# FileYeet 📂🔥

FileYeet is a simple, Dockerized tool designed to recursively find files with a specific extension in a source directory and "yeet" (copy) them all into a single flat destination folder. It features a retro-modern, neo-brutalist web interface for easy operation.

<img width="1758" height="962" alt="image" src="https://github.com/user-attachments/assets/0041bd6f-f32f-431e-8d24-6d998095b6c0" />

## Features

- **Recursive Search**: Finds files deep within nested subdirectories.
- **Flattened Output**: Copies all found files into a single output folder.
- **Smart Conflict Handling**: Automatically renames duplicates (e.g., `song.mp3` -> `song_1.mp3`).
- **Custom Extensions**: Supports any file type (`mp3`, `jpg`, `pdf`, etc.).
- **Web Interface**: Easy-to-use browser-based UI with a folder picker.
- **Dockerized**: Runs in a container for isolation and portability.

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shizuo-x/fileyeet.git
    cd fileyeet
    ```

2.  **Configure Drive Access (Important):**
    By default, the `docker-compose.yml` is configured to mount the `C:`, `D:`, and `E:` drives so the container can access your files.

    Open `docker-compose.yml` and verify the `volumes` section matches your system drives:
    ```yaml
    volumes:
      - C:/:/mnt/c
      - D:/:/mnt/d  # Remove if you don't have a D drive
      - E:/:/mnt/e  # Remove if you don't have an E drive
    ```
    *Note: On Linux/Mac, you will need to adjust these paths to mount your `/home` or specific directories.*

3.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```

## Usage

1.  Open your web browser and navigate to:
    `http://localhost:8336`

2.  **Target Extension**: Enter the file extension you want to find (default is `mp3`). Do not include the dot.

3.  **Source Directory**: Click "BROWSE" to select the folder you want to scan. You can navigate through your mounted drives (`/mnt/c`, `/mnt/d`, etc.).

4.  **Destination Directory**: Click "BROWSE" to select where you want the files to be copied.

5.  Click **EXECUTE COPY OPERATION**.

6.  The log window at the bottom will show the progress and any errors.

## Troubleshooting

-   **"Input directory not found"**: Ensure you have correctly mounted the drive in `docker-compose.yml` and that you are selecting the path starting with `/mnt/...` in the browser.
-   **Permission Errors**: Ensure Docker has permission to access your drives. On Windows, you might need to grant file sharing permissions in Docker Desktop settings.

## License

MIT License
