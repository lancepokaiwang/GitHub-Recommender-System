# Issue and Project Recommendation System for a GitHub Newcomer

The project is a content-based filtering approach for suggesting tasks and projects to GitHub newcomers.

See the project proposal [here](PROPOSAL.md)

***
## 2019.11.05 Update
* Param/Model outpts from Nov 4 [RESULTS.md](RESULTS.md)

## 2019.11.04 Update
>* Rewrite data extraction and user extration in order to get more data and increase predict precision.
>* Added "User Classification" file to predict newcomer.
>* Saved "User Decision Tree Model" and "User Random Forest Model" files for future usage.
>* Symfony data set, MSR 14 [https://github.com/symfony/symfony](https://github.com/symfony/symfony)

| Data                                | Description                                                     |
| ----------------------------------- | --------------------------------------------------------------- |
| `data.json`                         | list of repository issues that are bug fixes and/or "easy pick" |
| `data_users.json`                   | list of users from issues that are bug fixes and/or "easy pick" |
| `data_users_ready_to_analysis.csv` | clean/preprocessed data_users.json                               |


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
