# Bioethics Project

This project provides tools and services for bioethics research and
applications. The following instructions explain how to set up and run the
project using pixi.

## Prerequisites

Ensure you have the following installed on your system:

- [pixi](https://pixi.sh) package manager

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/uw-ssec/bioethics.git
   cd bioethics
   ```

2. Install dependencies:

   ```bash
   pixi install
   ```

3. Run the Server:

   ```bash
   pixi run server
   ```

4. Run the Interface (You might need to run it in another terminal):

   ```bash
   pixi run streamlit
   ```

5. Access the services:

   - Backend: [http://localhost:8000](http://localhost:8000)
   - Streamlit (Interface): [http://localhost:8501](http://localhost:8501)

6. To stop the services, press `Ctrl+C` in the terminal.

## Customization

- Modify the pixi configuration files to adjust service configurations or
  dependencies.

## Troubleshooting

- Ensure no other services are using ports `8000` or `8501`.
- If you encounter issues with pixi, refer to the
  [pixi documentation](https://pixi.sh).

For further assistance, check the
[project issues section](https://github.com/uw-ssec/bioethics/issues).

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
