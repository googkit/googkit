_googkit() {
	if ((CURRENT == 2)); then
		_values -w \
			'subcommand' \
			'apply-config' \
			'compile' \
			'init' \
			'setup' \
			'update-deps'
	fi
}
compdef _googkit googkit
