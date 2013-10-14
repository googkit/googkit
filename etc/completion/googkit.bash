_googkit() {
	COMPREPLY=()
	local word="${COMP_WORDS[COMP_CWORD]}"

	if [ "$COMP_CWORD" -eq 1 ]; then
		COMPREPLY=( $(compgen -W "$(googkit _commands)" -- "$word") )
	else
		local words=("${COMP_WORDS[@]}")
		unset words[0]
		unset words[$COMP_CWORD]
		local completions=$(googkit _commands "${words[@]}")
		COMPREPLY=( $(compgen -W "$completions" -- "$word") )
	fi
}

complete -F _googkit googkit