# Visualizer++: A Maltego Plugin

## Foreword

This was a project done within a week during Global Cybersecurity Camp 2024. It will be FOSS and updates are not guaranteed.

## Instructions

Have Docker & Docker Compose installed. (Docker Desktop is enough to have these two)

This plugin allows you to import phone/message logs as CSVs and will show you the connection between them.

## Build 

```bash 
git clone https://github.com/UltimateHG/gcc2024_project/ && cd gcc2024_project
cd phone_dumps_analysis 
pip install -r requirements.txt
docker compose up -d --build
```

## Import the transformation in Maltego

![](images/specification.png)
