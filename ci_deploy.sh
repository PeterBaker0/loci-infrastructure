build_prefix=time-demo/BUILD
echo "Incrementing action id"
current_id=$(cat action_id)
new_id=$((current_id + 1))
echo $new_id > action_id
echo "ID:$current_id -> ID:$new_id"
echo "Creating empty git commit with new tag" 
git commit --allow-empty -m "Azure CI Build:${new_id}."
git tag $build_prefix:${new_id}
echo "Pushing tag and empty commit"
git push --tag 
git add version 
git commit -m "Updating action id after build" 
git push 
