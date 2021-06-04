# Tracking Reported Cases of Illegal Fireworks in 2020
 
 
Arguably, it may be insufficient to compare two years of data. Yet the story holds in the second subplot. When comparing the total number of illegal fireworks being set off in June over the past decade, 2020 is not normal. The bars that represent the number of reports from 2010 to 2019 are almost non-existent when placed on a set of axes alongisde the 2020 data. 

![Image showing trend in fireworks](https://github.com/danielbchen/June-2020-Fireworks/blob/master/Reported%20Fireworks%20Cases%20in%20NYC.png)

For the second part of this brief analysis, I explore the location in which illegal fireworks are reported. Luckily, 311 provides the zip code that corresponds to a report. While the zip code of the reporter is not identical to the zip code of the incident, I assume that the neighborhoods are close enough in proximity. It would be unlikely that a reporter in Union Square would call in to 311 with a complaint of fireworks being set off across the bridge in Brooklyn. The choropleth below shows the number of reported cases of illegal fireworks per zip code in June 2020. Darker shades of red indicate a higher number of reports relative to lighter shades.

![Image showing number of reports by zip code](https://github.com/danielbchen/June-2020-Fireworks/blob/master/Fireworks%20Choropleth.png)

First, it's striking how dark zip code 11226 is in Brooklyn. Over 8000 reports stem from 11226 only. Second, the reports of fireworks are generally from Harlem, Washington Heights and Flatbush - communities where a large number of people of color reside. It is not a conicidence that these are also lower income neighborhoods relative to other areas in the five boroughs. Zip code 11226, for example, has a median income of $52,729 whereas the median for Kings County is $62,050 according to data from [NY HomeTown Locator](https://newyork.hometownlocator.com) in 2020. I am unsure as to how we make sense of the data in this scenario, but it is extremely odd that the zip code with the largest number of reports has more than twice as many reported incidents than that of the zip code with the second largest number of reports (10032 in Washington Heights with 723 reports in June). 

