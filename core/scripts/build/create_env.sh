#!/bin/bash

# --------------------------------------------------------------------------------------------
# [Valentyn] create_env.sh
#				Generate .env file during the CICD build phase.
# --------------------------------------------------------------------------------------------

# Change directory to the source of the script, go back one, send output to /dev/null and print working directory with /.sample.env
app_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && cd .. && cd .. && pwd )"

# 1. Make sure we have sample.env file to build .env file off for the build instance.
if [[ ! -f "${app_dir}/.sample.env" ]]; then
	echo "No .sample.env file found. Exiting script (1)." >&2; exit 1
fi

# 2. For each line, split by `=` and grab first.
env_variables=()
while IFS= read -r line
do
  env_pair=(${line//=/ }) # Split line delimited by equal sign.
  env_variables+=("${env_pair[0]}")
done < "${app_dir}/.sample.env"

# 3. Make sure we don't accidentally run this on an environment with .env already existing.
if [[ -f "${app_dir}/core/core/.env" ]]; then
	echo "This environment already has a .env file generated. Exiting script (1)." >&2
	exit 1
fi

# 4. Create the .env file based on our pipeline keys.
missing_variables=()
for env_var in ${env_variables[@]}; do
	# Check if this variable is not defined, and not an optional variable.
	if [[ "${!env_var}" = '' ]]; then
		missing_variables+=($env_var)
	# Only store variables that have values ( to address optional but empty case ).
	elif [[ "${!env_var}" != '' ]]; then
		echo "${env_var}=${!env_var}" >> "$app_dir/core/core/.env"
	fi
done

# 5 Let user know if we don't have any deployment variable(s) set up correctly.
if [[ ${#missing_variables[@]} -gt 0 ]]; then
	for missing_var in ${missing_variables[@]}; do
		echo "Please ensure deployment variable ${missing_var} is defined."
	done
	echo "Exiting script (1)."; exit 1
fi

echo "Successfully created .env file using the build's environment variables."