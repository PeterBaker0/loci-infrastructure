#!/bin/bash -e
destroy_prefix=time-demo/DESTROY
echo "Incrementing action id"
current_id=$(cat action_id)
new_id=$((current_id + 1))
echo $new_id > action_id
echo "ID:$current_id -> ID:$new_id"
echo "Creating empty git commit with new tag" 
git commit --allow-empty -m "Azure CI Tear Down:${new_id}."
git tag $destroy_prefix-${new_id}
echo "Pushing tag and empty commit"
git push --tag 
git add action_id 
git commit -m "Updating action id after tear down" 
git push 
