#  Airline Data Analysis & Occupancy Optimization

##  Overview

Analyzed airline data to identify ways to improve **occupancy rates** and **profitability** using SQL and Python. Built an end-to-end pipeline from data ingestion to business insights.

---

##  Business Problem

Airlines face rising operational costs (fuel, taxes, labor).
Goal: **Increase occupancy rate to maximize revenue per flight**. 

---

##  Workflow

```text
CSV → Python (Ingestion) → SQL Server → Analysis → Insights
```

---

##  Data Ingestion

* Automated CSV-to-SQL pipeline using **Pandas + SQLAlchemy**
* Dynamic table creation

 `Airlines_Ingestion.py` 

---

##  Data & Exploration

* Multiple tables: flights, tickets, bookings, seats, etc. 
* Performed schema checks & missing value analysis

---

##  Key Analysis

* **Fleet Analysis**: Identified aircraft with >100 seats
* **Trends**: Ticket bookings and revenue increase together
* **Pricing**: Business class generates highest revenue
* **Revenue Performance**:

  * Highest: SU9 (high demand, lower price)
  * Lowest: CN1 (limited offerings) 

---

##  Occupancy & Impact

* Calculated occupancy rate per aircraft
* Simulated **10% increase in occupancy**

 Result: Significant increase in annual revenue

---

##  Insights

* Pricing strongly affects demand
* Low occupancy = missed revenue
* Balanced pricing + higher occupancy = optimal strategy

---

##  Tech Stack

* Python (Pandas, Matplotlib, Seaborn)
* SQL Server
* SQLAlchemy

---

##  Files

* `Airlines_Ingestion.py` – Data pipeline 
* `data_analysis_airlines.py` – Analysis 
* `Report (Airlines).pdf` – Business insights 

---

##  Key Skills Demonstrated

* SQL + Python integration
* Data analysis & visualization
* Business problem solving
* End-to-end project execution

---
