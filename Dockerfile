# 1. Use an official Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the current directory contents into the container at /app
COPY . /app

# 4. Install any needed packages specified in requirements.txt
# We directly install them here for simplicity
RUN pip install --no-cache-dir pandas matplotlib seaborn

# 5. Run data_analysis.py when the container launches
CMD ["python", "data_analysis.py"]