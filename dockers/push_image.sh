#!/bin/bash
set -x
set -e

VERSION_FILE_PATH="src/version.py"

authen(){
    set +e
    docker login artifact.twinape.org
    pass show docker-credential-helpers/docker-pass-initialized-check
    docker login artifact.twinape.org
    set -e
}

if command -v docker-compose &> /dev/null; then
    build_command(){
        docker-compose build $1
    }
    push_command(){
        docker-compose push $1
    }
else
    build_command(){
        docker compose build $1
    }
    push_command(){
        docker compose push $1
    }
fi

authen

version=$(grep -oP '__version__ = "\K[0-9]+\.[0-9]+\.[0-9]+' "$VERSION_FILE_PATH")
if [[ -z "$version" ]]; then
    echo "Current version not found in $VERSION_FILE_PATH."
    exit 1
fi

cd dockers
version=$version build_command $1
build_command $1

authen

echo --------- Pushing Client Docker Image to artifact ---------
version=$version push_command $1
push_command $1
echo --------- Done ---------
