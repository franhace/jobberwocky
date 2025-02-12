# RELEASE.md

## Overview

**Project:** Jobberwocky  
**Version:** v1.0.0  
**Release Date:** 2025-02-12

This release includes the integration of the `jobberwocky-extra-source-v2` module, which must be cloned into the same repository. In this release, we address the following features and fixes:
- [Briefly list new features or bug fixes]

---

## Prerequisites

Before deploying, ensure the following requirements are met:

- **Repository Structure:**  
  The repository must contain both the main Jobberwocky project and the `jobberwocky-extra-source-v2` module cloned as a sibling directory.

- **Environment Variables:**  
  Create a `.env` ( in this case provided ) file in the repository root with all necessary environment variables, such as:
  - `DATABASE_URL`
  - `EXTERNAL_API_URL`
  - Other relevant configuration settings

- **Dependencies:**  
  Ensure that Docker and Docker Compose are installed on your deployment environment.

---

## Build & Deployment Instructions

1. **Clone the Repository and Extra Source:**

   ```bash
   git clone https://github.com/yourusername/jobberwocky.git
   cd jobberwocky
   git clone https://github.com/yourusername/jobberwocky-extra-source-v2.git

2. **Build and Deploy Using Docker Compose:**
    ```bash
    docker-compose up --build
   

3. **Documentation:**
For detailed API documentation and project architecture, refer to the /docs endpoint once the application is running.

---