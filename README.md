# NHS - SMAIRs Funding Analysis

This project dives deep into [SMAIRs](https://data.ontario.ca/dataset/service-manager-annual-information-return-smair) dataset, not yet released to public, but obtained via [Freedom of information](https://www.ontario.ca/page/freedom-information-request).

Every year under NHS (National Housing Startegy), Service Managers have to file SMAIRs (Service Manager Annual Information Reports) PDFs to show how they have distributed funds in their respective cities.

---

## Conclusions

- The findings of the project highlight that public housing schemes have been consistently receiving higher funding that the private sector. 
-  Despite the evolving policies, the RGI rent supplements have shown no significant shift from public housing to private rentals over the years

This underscores the contribution of public housing in social housing and the effective administration of service managers. 

---

## Dataset conversion

Dataset had **108 PDFs** from **10 cities**, spanning 13 years (2010-2023). It also had 8 main schemes:

| Program                  | Type   |
|--------------------------|--------|
| Public Housing           | Public |
| Rent Supplement          | Private|
| Limited Dividend         | Private|
| Section 26               | Private|
| Section 27               | Private|
| Section 95 - PNP         | Private|
| Section 95 - MNP         | Public |
| Provincial Reformed      | Public |
| Pre-86 Urban Native      | Public |
| Post-85 Urban Native     | Public |

Cities:

![](/EDA/cropped_ontario_map.png)

### Coversion:

- [Python DocTR](https://pypi.org/project/python-doctr/) was used to OCR (Optical Character Recognition) the PDFs into Text files. (**doctor.py**)

- Text files were then converted to CSVs via regex scripts in **input_to_db** folder.

- CSV files were cleaned and certain pages were rotated. (**DataCleaning.py and PDFrotate.py**)

---

## EDA

- All EDA via graphs and feature engineering was done in Jupyter Notebook. (**final_notebook.ipynb**)

#### Funding:

**Ongoing Funding**
Total Monthly funding provided to cities.

Left skew.

![](/EDA/hist_ongoing.png)

Total trend.

![](/EDA/page3_total_ongoing.png)

Private vs. Public based on above table.

![](/EDA/page3_ongoing_pp.png)

**RGI**
Rent Geared Income is where rent is calculated at 30% of Needy Households income, rest is payed by funding.

Left skew.

![](/EDA/hist_rgi.png)

**Private vs. Public RGI**
Noteable dip in 2020, hence Statistical testing only done for 2011-2019.

![](/EDA/rgi_pp.png)

**RGI vs. Non-RGI**
Non-RGI is basically where rest of the funds are directed. 2020 dip is seen again.

![](/EDA/RGI_non_RGI.png)

Trend without 2020.

![](/EDA/trend.png)

**Cities**
Ottawa has highest funding while values of Peterborough are missing until 2016.

![](/EDA/heatmap.png)

Log-heatmap for better view.

![](/EDA/log_heatmap.png)

Boxplot also shows York.

![](/EDA/rgi_box.png)

Ongoing Funding boxplot.

![](/EDA/ongoing_box_plot.png)

**Units**
Housing units by year. 2020 dip in RGI is more evident.

![](/EDA/RGI_non_RGI_vacant_YoY.png)

Ottawa has most number of units hence requiring most funding.

![](/EDA/units_heatmap.png)


**CWL**
Centralized waiting list has households which are on wait for receiving benefits

![](/EDA/CWL_by_year.png)

Ottawa and York have highest demand.

![](/EDA/CWL_cities.png)

---

## Statistical Testing

This was the final step in the project methodology that involved developing statistical models to evaluate presence of any statistically significant shifts in the fund allocations. Hierarchical Linear Models were developed in R to assess the coefficients of contributing variables and their p-values. (**housing_model_final.R**)

### Ongoing Funding:

```R
model <- lmerTest::lmer(log(ongoing_funding) ~ year_centered * scheme + (1 | city), data = funds)
```
To access the interaction between ‘Year’ and ‘Scheme’ (Public and Private), an interaction term of these was introduced to the model, while city was added as a variable effects term. The logarithm of ongoing funding was taken into account to handle the extreme right skew in the data.

### RGI Funding:
On similar terms, the RGI Funding model was developed.

```R
model <- lmerTest::lmer(log(rgi_funding + 1) ~ year_centered * scheme + (1 | city), data = funds)
```
The logarithm of RGI funding was taken into account to handle the extreme left skew in the data.
