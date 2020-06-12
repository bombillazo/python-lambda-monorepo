# Python AWS Lambda Monorepo

## About

This repository contains a micro-service monorepo example project using Python, AWS Lambdas and CircleCI.

### Goals of this project

- Create my own custom Python package
- Reuse my custom package in multiple Lambda functions
- Automate the build and deployment process for the Lambda function. This includes:
  - Have a single code location for my custom packages in the project.
  - No copy pasting my code across the different services.
  - Each Lambda function installs ***only*** the packages it needs (no blind installation of all packages "just in case")
  - Deploy code to AWS upon merging to master branch
- Build something cool related to dinosaurs

### Potential future improvements

- Local testing
- Automate cleanup of project
- Tag-based code deployment

## Medium

This project is also the foundation for a 3-part Medium series. Feel free to check out each part:

- [Part 1 - Project Setup](https://medium.com/@bombillazo/python-aws-lambda-monorepo-part-1-project-setup-12bdcca47d2d)
- [Part 2 - Custom Package Sharing](https://medium.com/@bombillazo/python-aws-lambda-monorepo-part-2-custom-package-sharing-b97c5b96e858)
- [Part 3 - Test, Build and Deploy](https://medium.com/@bombillazo/python-aws-lambda-monorepo-part-3-test-build-and-deploy-1260379dd3d1)

For questions or feedback, contact [@bombillazo](https://twitter.com/bombillazo)