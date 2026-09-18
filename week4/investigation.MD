# Data Exploration Notes and Process

## Thoughts from quick peek at/skim over the raw data
1. `data/participants.csv` symptoms_onset column has null values and what appears to be dates of birth.
2. `data/participants.csv` weight column appears to contain values tht *may* map to either pounds of kilograms
3. `data/blood_pressure.csv` I don't know what any of these columns could mean, this is raising a large red flag for my own lack of domain knowledge. Also, a lot of empty cells 
4. `data/heart_rate.csv` what does the numeric value in the `is_resting` column mean?
5. `data/hrv_measurements.csv` what is going on with the `tags` column?
6. `data/sleep.csv` lots of empty cells. Sleep duration unit of measure not specified, but probably safe to infer based on expected human nighttime sleep behavior...but maybe there are also naps in here?
7. `data/wearables.csv` lots of blank cells. `average_headphone_exposure` column seems random
8. `data/weather.csv` weird rounding for the `avg_temperature_C` column. `clouds` column containing a float value is also strange

## Questions to explore through the data
1. Was the reported severity of COVID-19 symptoms of users who report taking vitamins/nootropics meaningfully different from those users who did not? (Ultimately not enough data)
2. Did users who report having anxiety report their COVID-19 symptoms as more severe than those who did not? (Ultimately not enough data)

## Exploratory Process
The most important transformation that I did on the data was pivoting the survey data into a dataframe that treated every row as a complete survey pass. This was accomplished by indexing the `user_code` x `created_at` values to infer a single survey pass. This method is flawed as the `created_at` timestamp is not precise down to the minute, so we make the assumption that every time we enounter a new `scale` + `created_at` + `user_code` row, is maps cleanly to the first survey attempt that day and that all subsequent rows for that scale + user + day map sequentially. I'm not sure that this would be considered actual feature engineering as opposed to manipulating the shape of the raw data.

I did this because I wanted to cleanly look at scores to individual questions across the board for users. From there, my engineered feature was the percieved severity of the COVID experience for the user by using averaging the score of the symptoms across the idenitified COVID symtpom columns. This assumes equal weight applied to each symptom which may be misleading. For example, fatigue and shortness of breath, while both unpleasant may not necessarily cause the same amount of "misery" for a user. The subjective nature of perception makes this a risky feature to put any real significance on.

## Reflection
Jumping directly into a dataset without a specific question to answer ahead of time made finding direction in this activity challenging. I'm not sure how accurately the exercise reflects real world data scientist work, but I'd imagine that in the industry I would have been exploring this dataset as a possible source of insight to answer a specfic question and therefore would have had an easier time deciding how and why to perform various transformations or attempt to engineer features. The more time I spent with the data, the more opportunities I saw to look for patterns, but I wonder if this may be something of a workflow antipattern similar to that of trying to look for and retrofit a problem to a solution.
