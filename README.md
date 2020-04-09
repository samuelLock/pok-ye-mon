Synopsis: A REST API built using Flask that receives the name of a Pokemon and returns the shakespearean translation of it's description.

The Swagger page for the API can be found at: https://app.swaggerhub.com/apis-docs/Pok-Ye-Mon/pok-ye-mon/1.0.
The Swagger json file can be found at the root of this directory too.

The project can be deployed locally in a Docker container or deployed to an existing ECS cluster.

ECS Deployment:
How To Use:
    -   Link CircleCI pipeline to repo (https://circleci.com/docs/2.0/getting-started/)
    -   The pipeline requires 3 environment variables to be set manually: (https://circleci.com/docs/2.0/ecs-ecr/)
        . AWS_ACCESS_KEY_ID
        . AWS_SECRET_ACCESS_KEY
        . AWS_DEFAULT_REGION
    -   The pipeline has two workflows:
        . Local build of the flask app and runs unit tests.
        . Build the docker image and push it to the ECR repo. (https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

Limitations:
    -   The pipelines requires the ECS environment to already be set up. (See https://github.com/samuelLock/poke-ye-mon-infrastructure)
    -   The call to ECR to get the RepositoryID expects there to only be one repository. If there are multiple, the image will be pushed to the zero-indexed repository returned using the CLI.

    Local Deployment:
    How To Use:
        -   You can run the flask app directly using 'flask run' when in the root directory of the repo.
        -   A docker image can be built using 'docker build -t pok-ye-mon' (Docker must be installed).
        -   A standard 'docker run' command can then be executed to produce a local docker deployment of the API.

