# Reminder to build and tag from your fork of the bifrost repository first.
FROM bifrost:latest

# Your repository name
ENV PROJECT=cFS

# Install dependencies of your project expansion
COPY --chown=bifrost requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install your project expansion
COPY --chown=bifrost . ./$PROJECT
RUN pip install ./$PROJECT

# Override the default variables
# Setup Default Variables
# Tip: You can override using your own dockerfile.
# Tip: You can override using the docker-compose config template.
ENV AIT_CONFIG=/app/config/config.yaml
ENV AIT_ROOT=/app/ait
ENV BIFROST_SERVICES_CONFIG=/app/config/services.yaml
