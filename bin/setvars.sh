#!/bin/bash
export MPLCONFIGDIR="/tmp"
export PYTHONPATH="${PYTHONPATH}:${PWD}"
export PATH="/venv/bin:$PATH"

#export $(grep -v '^#' env.list | xargs -d '\n')
# check directory if not exists
## declare an array dir
declare -a arr=("users" "moods" "carts" "caches" "models")
## now loop through the above array
for i in "${arr[@]}"; do
  dir="${DATA_DIR}/${i}"
  [ -d "${dir}" ] || mkdir "${dir}"
done
echo "${DATA_DIR} directories created successfully"
