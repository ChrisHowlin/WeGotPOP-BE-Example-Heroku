# We Got POP BE example

The server exposes an 'artists' path, which can be queried using a GET request.
The parameters accepted by this interface are:

Age criteria:
* **age_min** - the minimum age, as an integer
* **age_max** - the maximum age, as an integer
* **age_wgt** - indication of the relative weight for age for relevancy considerations

Location criteria:
* **loc_lat, loc_lon** - the location to search around, in decimal format
* **loc_rad** - the maximum radius to search within, in miles
* **loc_wgt** - indication of the relative weight of artist location for relevancy considerations

Pay rate criteria:
* **rate_max** - sets a maximum limit on the artist rate_max, in GBP
* **rate_wgt** - indication of the relative weight of artist rate for relevancy considerations

Gender criteria
* **gender** - specify gender out of 'M' (male) or 'F' (female)
* **gender_wgt** - indication of the relative weight of artist gender for relevancy considerations

Filtering and relevance strategy
* **relevance** - A value in 'basic', 'relaxed' or 'blended'. Defaults to 'basic'.

## Assumptions

### Handling input

While none of the parameters are independently mandatory, there are some
conditional dependencies. In all cases, if the weight parameter is specified,
but none of the others in the group are specified (e.g. **rate_wgt** is
provided but not **rate_max**), then the whole set of criteria are ignored.

Similarly, if there is a parameter without the associated weight parameter,
then the whole group will be ignored.

#### Gender

Increasingly in today's world we have to consider gender people's desire to
define their gender outside of the conventional 'Male' or 'Female'. For the
purposes of this example, as all of the dataset is labelled with either 'M' or
'F', I have restricted the gender parameter in this way, in order to align with
the provided data.

### Error handling

Age:
* If **age_min** or **age_max** < 16, then assume value is 16
* If **age_min** or **age_max** > 74, then assume value is 74
* If **age_min** > **age_max**, then **age_max** will be set to the value of **age_min**

Location:
* If either **loc_lat** or **loc_lon** is not provided then ignore the location
criteria entirely
* If (**loc_lat**, **loc_lon**) is not a valid coordinate then set to default
London coordinate (51.5074, 0.1278)
* If **loc_rad** is not provided, or is less than the minimum value (0.5 miles),
then set to the minimum value

Rate:
* If **rate_max** is < 10.0 or > 39.97, then set to the appropriate value

Gender:
* If gender not either 'M' or 'F' then gender criteria will be ignored

### Filtering and relevance strategy

There is some tension between two of the requirements in the problem outline.
That is, the requirement to require a match against the parameters against the
requirement to consider the relevance of the match.

The specification states that the response content should match the criteria
(e.g. if maximum age specified is 40, then no artists should be returned
greater than that age). However, it is not clear how to order these returned
results by age relevance if all the artist ages that match the criteria are
considered to be equally relevant. On the converse, if the ages within the
criteria are not equally relevant, then it is not clear what assumption to make
to order the artists by.

To put this in an example, a search with a specified age range of 21-40 may
have different consderations of relevance, depending on the context. In a
night club scene, you would probably want a younger age sken than in a wine bar.

For location and rate, it may be possible to assume a natural ordering (such as
closer to the location, and lower rate are more relevant), and this is what is
assumed in this strategy. For artists which match the location and rate, they
will be ordered according to this approach.

For gender, I can see that there is no general ordering. If the caller has a
preference for a gender, this would presumably be provided expliticly or not at all. 

### Basic approach (strict matching, limited relevance)

In the basic matching approach, only artists which explicitly match the
parameters are returned. If a rate or a location is specified, then the results
are ordered by which of these criteria sets has the strongest weighting, then
the other if there is a match.

Outside of whether the artist matches, age and gender have no impact on the
relevance ordering.

### Alternative approach (relaxed matching)

The basic approach is quite restrictive, and possibly goes outside of the
intent of the searching engine, which is to maximise the number of artists that
the user is interested in.

To put it this way, if the caller cannot find enough interesting artists within
a 40-60 range, they would probably be interested in 39 or 61 year olds to make
up the numbers.

If a request is made with too restrictive criteria, there may only be a small
number of artists which strictly meet the conditions. In this case, you may
want to trade off the strictness of the match to get more results returned,
which are close to what you requested.

One way to approach this would to always target to return 100 artists, with the
exact matches first, and then if there were not enough to satisfy that criteria
then gradually relax the constraints using the criteria weight information to
decide which constraint to relax first.

Example:
If you are looking for artists in age group 21-25 and within five miles of
location (51.5074, 0.1278), with a strict matching perhaps only 20 results
would be returned. If age were indicated as more important than location in
this case you could increase the number of matches by increasing the location
radius (and maintaining the same)cage criteria until reaching 100 artists.
Then, if increasing the location radius were not sufficient, you could start
relaxing the age constraints until reaching the required limit.

### Extension approach (relaxed matching, blended relevance)

In this alternative strategy, the constrints are relaxed in an ordered manner
based on the weighting provided (so, the location radius is completely
expanded before the age range is increased). This would likely not achieve the
intended outcomes, as for hiring in London, you would prioritise a 25 year old
in Edinburgh before returning a 26 year old in London.

Instead, it may be better to relax all the constraints at the same time, but at
different speeds depending on the weight. 

In the previous example if, instead of exhausting all possible locations before
relaxing age, you could may consider 16-30 in London, to be equal to 20-26
in Edinburgh.

#### Implementation

This is the first solution that gets really interesting in determining relevant
artists.

In this case, all artists which fit completely in the criteria are 'perfect'
matches, and the others are scored to an equation such as this:

score_artist = (1/age_wgt * k_age * d_age) + (1/loc_wgt * k_location * d_location) + 
  (1/rate_wgt * k_rate * d_rate) + (1/gender_wgt * k_gender * d_gender)

k_n is the normalising factor for each criteria, as using unnormalised values
would give all distances the same weight (e.g. an increase in 1 mile would be
equivalent to one year in age) and would cause location to have a much worse
effective weight than age or rate.

What is interesting with this approach is while in the simplest case, the
distance between, for example, the target age range and the actual range is
linear in the formula above. Instead it could be non-linear or even parametric
based on the target age range. This would allow the relevance to recognise that
the distance between 21 and 16 is actually much different to 21 and 26, despite
being 5 years in each case.

The complexity of this approach is that the normalisation factors and difference
functions need to be defined, which involves a lot of tweaking to make sure
that the output is actually relevant. This could be done by eye or, if there
were enough data, by using a machine learning approach to learn the coefficents
that give the most relevant distribution of results.

## Examples

artists?age_min=50&age_max=60&age_wgt=1&rate_max=20&rate_wgt=2&loc_lat=51.55587162&loc_lon=0.13083594&loc_rad=20&loc_wgt=3&relevance=basic

* Searches within 50-60 age range, with max rate £20 and within 20 miles of (51.55587162,0.13083594). Only returns exact matches. Within the results artist are ordered by lowest rate and then by distance from location radius (if the rates are equal)

artists?age_min=50&age_max=60&age_wgt=1&rate_max=20&rate_wgt=2&loc_lat=51.55587162&loc_lon=0.13083594&loc_rad=20&loc_wgt=3&relevance=relaxed

* Searches within 50-60 age range, with max rate £20 and within 20 miles of (51.55587162,0.13083594), age weighted before rate before location. Once determining the exact matches append non-exact matches taken from an ordered list which is sorted in order of the specified weights (so age first, then rate, then location).

artists?age_min=50&age_max=60&age_wgt=1&rate_max=20&rate_wgt=2&loc_lat=51.55587162&loc_lon=0.13083594&loc_rad=20&loc_wgt=3&relevance=blended

* Searches within 50-60 age range, with max rate £20 and within 20 miles of (51.55587162,0.13083594), using the blended relevance. Age is most important, followed by rate, followed by location.
  * In the results, you can see that after all the complete matches have been returned, the age, rate and location criteria are slowly relaxed to include artists which are close to the criteria but don't match exactly. In this case as the location is a low priority, the radius will be expanded by, 3 miles before increasing the rate limit by £1, and 6 miles before increasing the age limits by 1 in either direction. Effectively a 61 year old within the search radius and a 60 year old within 6 miles of the search radius have the same weight.
  * If the weights were switched such that location was weighted 1 and age was weighted 3, then one mile would be equal to 0.67 years (so we would relax age a lot more quickly than before to focus on keeping the location in the same area 
