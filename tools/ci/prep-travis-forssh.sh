#!/bin/bash

mkdir -p ~/.ssh

cat >>~/.ssh/config <<'EOF'

Host datalad-test
HostName localhost
Port 42241
User dl
StrictHostKeyChecking no
IdentityFile /tmp/dl-test-ssh-id
EOF


cat >>~/.ssh/config <<'EOF'

Host datalad-test2
HostName localhost
Port 42242
User dl
StrictHostKeyChecking no
IdentityFile /tmp/dl-test-ssh-id
EOF

ssh-keygen -f /tmp/dl-test-ssh-id -N ""
eval $(ssh-agent)
ssh-add /tmp/dl-test-ssh-id

(
    # At this point part of the set up is building the image, but this will
    # just be downloaded.
    cd tools/ci/docker-ssh
    ./setup /tmp/dl-test-ssh-id.pub
)

# FIXME: This is hacky and likely too long, but we need to sleep at least a
# little.
sleep 10
ssh -v datalad-test exit
ssh -v datalad-test2 exit
