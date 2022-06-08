# developer-churn-prediction installation guide

```bash
# Get the project
$ git clone https://github.com/TECH4DX/developer-churn-prediction.git
# Build docker image via the Dockerfile
$ docker build -t person_or_orgnization/image_name:version ./
# Push the image if you want
$ docker push person_or_orgnization/image_name:version
# Run the 
$ docker run -e OPEN_SEARCH_HOST=host_here -e OPEN_SEARCH_PORT=port_here -e OPEN_SEARCH_USER=username_here -e OPEN_SEARCH_PASSWORD=password_here -it person_or_orgnization/image_name:version /bin/bash
```

```python3
# To run this project, please set the variable values in advance.
# OPEN_SEARCH_HOST: The host of the OpenSearch.
# OPEN_SEARCH_PORT: The port of the OpenSearch.
# OPEN_SEARCH_USER: Username.
# OPEN_SEARCH_PASSWORD: Password.
host = os.environ.get('OPEN_SEARCH_HOST', '')
port = os.environ.get('OPEN_SEARCH_PORT', '')
auth = (os.environ.get('OPEN_SEARCH_USER', ''),  os.environ.get('OPEN_SEARCH_PASSWORD', ''))
```