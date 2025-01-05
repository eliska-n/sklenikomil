#!/bin/sh

docker build -t sklenikomil-be .
exec docker run --rm --network host -v ${PWD}/etc:/conf sklenikomil-be