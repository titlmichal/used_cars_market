# used_cars_market

## 27.8.2025: Initial commit

### Purpose of this project
Goal of this project is twofolds. First, I want to gain more objective insights in the used car market. Second, I aim to practice already learnt tools (e.g. Python, Git, etc) and acquire new skills (mostly regarding data engineering - cloud, dbt, elt, dwh).

### Planned approach
Im using LLM (Gemini) as a mentor, professional guide, not a coder/step-by-step guider, and sort of architect. I believe this allows me to allign my project with in demand skills while leaving me with solving the actual problem myself, avoiding spamming forums but still requiring me to the hard work. Current outlook is as follows:
1) create scraper for selected used cars webpage (E in ELT)
2) load the data into GCP/BigQuery (L in ELT)
3) deal with the messy extractions via dbt (T in ELT) and create model and tests
4) set up automation via GitHub Actions, connection to BI tool and visualize