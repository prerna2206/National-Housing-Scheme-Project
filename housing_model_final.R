library(readr)
library(tidyr)
library(dplyr, quietly = TRUE)
library(foreach)
library(caret, quietly = TRUE)

funds <- read_csv("housing_data_page_3.csv", 
                  show_col_types = FALSE)

funds <- funds %>% 
  filter(Year >= 2011 & Year <= 2019 & City != "Peterborough" & 
           `Ongoing Funding` > 0 & Name != "TOTAL")

data_schemes <- data.frame(
  Program_Type = c('Public housing', 'Section 95 - MNP', 'Provincial reformed', 
                   'Pre-86 urban native', 'Post 85 urban native', 
                   'Rent supplement', 'Limited dividend', 'Section 26', 
                   'Section 27', 'Section 95 - PNP'),
  Housing_Sector = c('Public', 'Public', 'Public', 'Public', 'Public', 
                     'Private', 'Private', 'Private', 'Private', 'Private')
)

output <- foreach(i = 1:nrow(funds), .combine = c) %do% {
  data_schemes$Housing_Sector[which(funds$Name[i] == data_schemes$Program_Type)]
}

funds$Scheme <- output

names(funds) <- c("year", "city", "name", "number", "one_time_funding", 
                  "funding_target", "total", "percentage", "scheme")

## Ongoing - Public vs Private

funds2 <- funds %>% select(year, city, funding_target, scheme)

funds2 %>% glimpse()

funds2 <- funds2 %>% mutate(year_centered = scale(year, scale = FALSE))
funds2

funds2 %>% boxplot(funding_target ~ city, data = .)

par(mar = c(4,4,1,1), mfrow = c(2,2))
plot(funds2 %>% lm(funding_target ~ year*scheme*city, data = .), which = 1:4)

funds2 %>% lm(funding_target ~ year*scheme*city, data = .) %>% summary()

funds2 %>% aov(funding_target ~ year*scheme *city, data = .) %>% summary()

library(lme4)

model <- lmer(log(funding_target) ~ year_centered * scheme + (1 | city), 
              data = funds2)
summary(model)

# Random effects visualization
ranef(model)

m1 <- lm(funding_target ~ scheme*city, data = funds2) ## only ottawa, public:Durham, public: York Significant
summary(m1)

m2 <- lm(funding_target ~ year*scheme, data = funds2) ## only ottawa, public:Durham, public: York Significant
summary(m2)

## RGI Funding in Public vs Private

# Calculate RGI Funding and Non-RGI Funding
funds <- funds %>%
  mutate(
    rgi_funding = `funding_target` * percentage / 100,
    non_rgi_funding = `funding_target` - rgi_funding
  )

# View the first few rows of the modified dataset
funds %>% glimpse()

funds3 <- funds %>% select(year, city, scheme, rgi_funding)

funds3 %>% glimpse()

# Remove rows with NA or NaN values in rgi_funding
funds3 <- funds3 %>% filter(!is.na(rgi_funding) & !is.nan(rgi_funding) & !is.infinite(rgi_funding))
#funds3$rgi_funding_adjusted <- funds3$rgi_funding + 1

funds3 <- funds3 %>% mutate(year_centered = scale(year, scale = FALSE))
funds3

funds3 %>% boxplot(rgi_funding ~ city, data = .)

par(mar = c(4,4,1,1), mfrow = c(2,2))
plot(funds3 %>% lm(rgi_funding ~ year*scheme*city, data = .), which = 1:4)

funds3 %>% lm(rgi_funding ~ year*scheme*city, data = .) %>% summary()

funds3 %>% aov(rgi_funding ~ year*scheme *city, data = .) %>% summary()

model <- lmer(log(rgi_funding+1) ~ year_centered * scheme + (1 | city), 
              data = funds3)
summary(model)

fixed_effects <- summary(model)$coefficients
fixed_effects_df <- data.frame(
  Term = rownames(fixed_effects),
  Estimate = fixed_effects[, 1],
  Std.Error = fixed_effects[, 2],
  t.value = fixed_effects[, 3]
)

aggregated_data <- funds3 %>%
  group_by(city, scheme) %>%
  summarise(Total_Funding = sum(rgi_funding, na.rm = TRUE)) %>%
  mutate(Funding_Scaled = ifelse(scheme == "Public", Total_Funding, -Total_Funding)) # Negate Private for pyramid

# Create the population pyramid
funds3

# Random effects visualization
ranef(model)

par(mar = c(4,4,1,1), mfrow = c(2,2))
plot(funds3 %>% lmer(log(rgi_funding+1) ~ year_centered * scheme + (1 | city),data = .), which = 1:4)

hist(funds3$rgi_funding, main = "Histogram of RGI Funding", xlab = "RGI Funding", col = "lightblue", border = "black")

## RGI vs Non RGI

funds4 <- funds %>% 
  select(year, city, rgi_funding, non_rgi_funding) %>%
  pivot_longer(cols = c(rgi_funding, non_rgi_funding), 
               names_to = "funding_type", 
               values_to = "funding_value")

# Centered year for modeling
funds4 <- funds4 %>% 
  mutate(year_centered = scale(year, scale = FALSE))

# Linear Regression Model
lm_model <- lm(funding_value ~ year_centered * funding_type * city, data = funds4)
summary(lm_model)

# ANOVA Model
aov_model <- aov(funding_value ~ year_centered * funding_type * city, data = funds4)
summary(aov_model)

# Mixed Effects Model
mixed_model <- lmer(log(funding_value + 1) ~ year_centered * funding_type + (1 | city), data = funds4)
summary(mixed_model)
