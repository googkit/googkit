_googkit() {
	local words completions
	read -cA words

	total_words=${#words}
	if [[ $total_words -eq 2 ]]; then
		completions="$(googkit _candidates)"
	else
		completions="$(googkit _candidates ${words[2,-2]})"
	fi

	reply=("${(ps:\n:)completions}")
}

compctl -K _googkit googkit
