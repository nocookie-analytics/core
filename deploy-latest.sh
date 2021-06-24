export PATH=$PATH:$HOME/.local/bin
export STACK_NAME=nocookieanalytics

git checkout main

git pull origin main

if [ -z "$TAG" ]
then
    export TAG=$(git rev-parse HEAD)
fi

echo "Deploying $TAG"

bash -x ./scripts/deploy.sh
