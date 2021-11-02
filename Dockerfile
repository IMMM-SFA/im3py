# Set base image. 
FROM python:3.6

# Set working directory in the container. 
WORKDIR /im3py

# Copy files to the working directory.
COPY . .

# Install dependencies.
RUN pip install --trusted-host files.pythonhosted.org --trusted-host pypi.python.org --trusted-host pypi.org -r requirements.txt

# Install the package.
RUN pip install ../im3py

# Check that we can import Model. 
RUN python -c "from im3py import Model"

# Keep container running. 
ENTRYPOINT ["tail", "-f", "/dev/null"]
