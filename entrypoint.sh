#!/bin/bash

COMMAND="${1}"

set -euo pipefail

# shell
if [[ ${COMMAND} == 'shell' ]]; then
    exec "flask shell"
elif [[ ${COMMAND} == 'python' ]]; then
    shift
    exec "python" "${@}"
elif [[ ${COMMAND} == 'bash' ]]; then
    shift
    exec "/bin/bash" "${@}"
elif [[ ${COMMAND} == 'alembic' ]]; then
    shift
    exec "alembic" "${@}"
fi

shift
exec "$COMMAND" "${@}"
