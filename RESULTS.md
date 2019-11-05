# Experiments

## Nov 4

### Features:
* age
* repo_num
* follower_num
* commit_comment_num
* commit_num'
* issue_comment_num
* issue_event_num
* issue_number
* org_number
* pr_comment_num
* pr_num
* collaborator_num

### K-means
* n_clusters: 2
* n_init: 10 (default)
* max_iter: 300 (default)
* tolerance: 0.0001 (default)
* algorithm: auto - em, elkan (default) 

### Training / Test Split 
* n = 474 
* 30%

### Model 1: Decision tree
* criterion: entropy
* split: best (default)
* max_depth: 13
* max_features: None - use all (default)
* random state: 0

### Model 2: Random Forest 
* criterion: entropy
* n_estimators: 10 (default) 
* max_depth: None (full depth)
* random_state=3
