# Issue and Project Recommendation System for a GitHub Newcomer

The project is a content-based filtering approach for suggesting tasks and projects to GitHub newcomers.

See the project proposal [here](PROPOSAL.md)

***
## 2019.11.24 Update
>* Fix preprocessing for issues_text; escape characters were being removed and fixed in [commit](https://github.com/jonlamca/comp5117-lam-wang/commit/553764211ce708fe8d373ad5299593b06a282c53)
>* TF-IDF results for title, body, and title-body. See [results](https://github.com/jonlamca/comp5117-lam-wang/tree/59d73e2/python37/data/issue_text) These were calculate separately for weighting purposes
>* Todo incoporate commit documents 


## 2019.11.18 Update
>* Simplified the code.
>* For 1.1., now we also collected "referenced commits" with issues.
>* Update K-Means, Decision Tree and Random Forest.
>* Add TF-IDF analysis for issues.

| Data                                          | Description                                                                                         |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `all_issues_REPO-NAME.json`                   | list of repository issues (also includs it's pr, commits) that are bug fixes and/or "easy pick"     |
| `users_REPO-NAME.json`                        | list of users from issues that are bug fixes and/or "easy pick" (THIS FILE MAY BE TOO HUGE TO OPEN) |
| `users_REPO-NAME_filtered.json`               | filtered user json file. include different ages with same user.                                     |
| `data_users_REPO-NAME_ready_to_analysis.csv`  | csv format file of `users_REPO-NAME_filtered.json`                                                  |
| `data_users_cluster_with_results.csv`         | K-Means result table                                                                                |
| `issue_text_REPO-NAME.json`                   | textual content of each issue                                                                       |

## 2019.11.17 Update
>* Simplified the code.
>* For 1.1., now only concern users who submit pr and commits whth related the issues with "Easy Pick" label
>* For 1.1., now collect all issue data and its related pr and commits data in order to save needed time when future usage.
>* For 1.2., now collect users' whole data in order to save needed time when future usage.
>* For 1.3., simplified the user data extraction process.
>* For 2.1. and 2.1.2., modified the code to fit latest version of data files.

## 2019.11.12 Update
>* For 1.1., modify the process logic in order to reduce the time needed.
>* For 2.1., add column "newcomer" in order to verify the newcomer.
>* For 3.1., modify KMeans in order to get more accuracy clustering result.
>* For 3.2., add "Silhouette Analysis" to determine the number of clusters.
>* For 4.1., move Decision Tree to this file.
>* For 4.2., move Random Forest to this file.
>> Next:
>>* Finalising how many cluster we need to use.
>>* Starting issue classify.

## 2019.11.05 Update
* Param/Model outpts from Nov 4 [RESULTS.md](RESULTS.md)

## 2019.11.04 Update
>* Rewrite data extraction and user extration in order to get more data and increase predict precision.
>* Added "User Classification" file to predict newcomer.
>* Saved "User Decision Tree Model" and "User Random Forest Model" files for future usage.
>* Symfony data set, MSR 14 [https://github.com/symfony/symfony](https://github.com/symfony/symfony)

## 2019.10.31 Update
>* Rewrite data extraction (in order to get more data)
>> Next:
>>* Getting user data and train user model to determine what charateristics that newcomers should have.

## 2019.10.25 Update
>* Create Python 3.7 environment for data analysis and process.
>* Filter the features which may be useful.
>* Dataset: [MSR 2014](http://ghtorrent.org/msr14.html)
>* The IDE I use: [PyCharm](https://www.jetbrains.com/pycharm/)

***

## License

No license. All rights reserved by Jonathan Lam ([@jonlamca](https://github.com/jonlamca)) and Lance Wang ([@ycpss91303](https://github.com/ycpss91303)).
