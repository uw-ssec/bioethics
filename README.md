# Bioethics Project

This project provides tools and services for bioethics research and applications. The following instructions explain how to set up and run the project using Docker and Docker Compose.

## Prerequisites

Ensure you have the following installed on your system:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/uw-ssec/bioethics.git
   cd bioethics
   ```

2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - Backend: [http://localhost:8000](http://localhost:8000)
   - Streamlit (Interface): [http://localhost:8501](http://localhost:8501)

4. To stop the containers, press `Ctrl+C` in the terminal or run:
   ```bash
   docker-compose down
   ```

## Customization

- Modify the `docker-compose.yml` file to adjust service configurations.
- Update the `Dockerfile` to include additional dependencies or changes.

## Troubleshooting

- If you encounter permission issues, try running Docker commands with `sudo`.
- Ensure no other services are using ports `8000` or `8501`.

For further assistance, refer to the official [Docker documentation](https://docs.docker.com/).

## Open source licensing

Statement from Schmidt Sciences:

_Schmidt Sciences expects that any code from projects funded by Schmidt Sciences
be released as open source under an
[OSI](https://opensource.org/licenses)-approved permissive license (such as
[Apache v2.0](https://choosealicense.com/licenses/apache-2.0/) or
[MIT](https://choosealicense.com/licenses/mit/)). We recommend that projects
avoid using GPL due to known complexities associated with it. We encourage
projects to publish data used for peer-reviewed scientific articles along with
the code used to produce the results. Additionally, we recommend avoiding any
license modifications for simplicity, and alignment with standard practices._
