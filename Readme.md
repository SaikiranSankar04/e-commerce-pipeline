# Ecommerce Analytics Pipeline

A full-stack data engineering & analytics project that simulates an ecommerce order ecosystem.
It features data generation, ETL processing, real-time KPIs, interactive visualizations, and containerized deployment.

Features:

1. Data Simulation: Generates realistic order-level data including user details, product categories, countries, and timestamps using the Faker library.

2. ETL Pipeline: Uses PySpark to clean, transform, and enrich raw generated data for downstream analytics.

3. Analytics API: Exposes key performance indicators (KPIs) such as daily orders, revenue by country, and sales by product category through REST APIs built with Flask.

4. Interactive Dashboard: Displays real-time metrics and visualizations. 

5. Tabular View & CSV Export: Provides views of raw and processed datasets with download options.

6. Containerized Architecture: All services run in isolated Docker containers, orchestrated using Docker Compose.

7. Deployed on Render 

| Layer                  | Tools & Frameworks             |
| ---------------------- | ------------------------------ |
| **Data Generation**    | Python, Faker                  |
| **ETL Processing**     | PySpark, Spark SQL             |
| **Analytics Engine**   | Pandas, Spark SQL              |
| **Backend API**        | Flask                          |
| **Frontend Dashboard** | Chart.js, Bootstrap            |
| **Deployment**         | Docker, Docker Compose, Render |
