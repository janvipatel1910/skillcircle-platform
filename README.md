# SkillCircle Lite

## Ask. Help. Earn. Reuse.

SkillCircle Lite is a social-impact platform where adults can request online help, complete tasks for others, earn demo credits, and reuse those credits to request help in the future.

## Problem

People frequently ask friends, followers, or online communities for help, but there is often no structured process for:

- Creating a clear help request
- Selecting a helper
- Tracking task completion
- Rewarding the helper fairly
- Reusing earned rewards within the community

## MVP Goal

An adult user can create an online help task funded with demo credits. Another user can complete the task, receive the reward exactly once, and reuse earned credits to fund a new task.

## Core Workflow

1. A requester creates an online help task.
2. The requester reserves demo credits for the task.
3. A helper is selected.
4. The helper submits the completed task.
5. The requester confirms completion.
6. The system credits the helper exactly once.
7. The helper can reuse earned credits to fund a new help request.

## User Roles

Requester and Helper are roles, not separate account types.

The same adult user can:

- Request help
- Provide help
- Earn credits
- Reuse earned credits

## Reward Model

- 1,000 SkillCircle Credits represent £1 in demo calculations
- The requester funds the reward before publishing a task
- Funded credits remain reserved until the task is completed or cancelled
- Approved rewards are credited to the helper exactly once
- Earned available credits can fund a new help request
- Cancelled-task credits return to the requester
- Version 1 uses simulated credits only
- Credits cannot be withdrawn or exchanged for real money
- Real payments are outside the SkillCircle Lite MVP

## Task Lifecycle

```text
OPEN → ASSIGNED → SUBMITTED → COMPLETED
```

A task can also become `CANCELLED` when permitted by the system rules.

## Version 1 Safety Scope

- Demo users must be 18 or older
- Online help only
- Simulated users and task data
- Demo credits only
- No real payments
- No credit withdrawals
- No emergency tasks
- No in-person tasks

## Not Included in the Lite MVP

- Real bank transfers
- Stripe integration
- Identity verification or KYC
- Tax calculations
- Chat or video calling
- AI task generation
- Mobile application
- Complex disputes
- Social-media integrations

These ideas can be considered only after the Lite MVP is complete.

## Planned Technology

- Python
- Pydantic
- Pytest
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Terraform
- Docker
- GitHub Actions
- Amazon CloudWatch

## Current Progress

- Project foundation created
- GitHub repository connected
- Python virtual environment configured
- Task data model created
- Input validation implemented
- Automated Task model tests passing
- Credit wallet model created
- Welcome, reservation, and cancellation rules implemented
- Automated Wallet model tests passing
- Task assignment and submission lifecycle implemented
- Requester-only task completion implemented
- Reserved rewards transferred to helpers exactly once
