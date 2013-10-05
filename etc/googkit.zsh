_googkit() {
	local words completions
	read -cA words

	total_words=${#words}
	if [[ $total_words -eq 2 ]]; then
		completions=$'compile\nconfig\ndeps\ninit\nsetup\nupdate'
	elif [[ $total_words -eq 3 ]]; then
		if [[ $words[2] = 'config' ]]; then
			completions='update'
		elif [[ $words[2] = 'deps' ]]; then
			completions='update'
		fi
	fi

	reply=("${(ps:\n:)completions}")
}

compctl -K _googkit googkit
