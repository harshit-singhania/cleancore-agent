---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Database Schema & Prisma Setup

## Objective

Initialize Prisma with Supabase and define the core multi-tenant data schema per the architectural decisions.

## Context

- .gsd/SPEC.md
- .gsd/ROADMAP.md
- .gsd/DECISIONS.md

## Tasks

<task type="auto">
  <name>Initialize Prisma and Environment</name>
  <files>prisma/schema.prisma, .env.local</files>
  <action>
    - Create `.env.local` if it doesn't exist and add the provided Supabase connection strings (`DATABASE_URL` with pooling and `DIRECT_URL` for migrations).
    - Ensure `prisma` logic is initialized. If `prisma` is not in package.json, install it as a dev dependency.
    - Configure `prisma/schema.prisma` with the `postgresql` provider and the connection strings from the `.env` references.
  </action>
  <verify>npx prisma validate</verify>
  <done>Prisma schema parses correctly without errors.</done>
</task>

<task type="auto">
  <name>Define Core Schema Modules</name>
  <files>prisma/schema.prisma</files>
  <action>
    - Create `Organization` and `User` models for multi-tenant isolation. Link Users to Organizations.
    - Create `ModernizationProject` model (belongs to Organization).
    - Create `CodeObject` model (belongs to ModernizationProject). Track specific metadata fields: `abapObjectType` (String), `legacyLoc` (Int).
    - Create `TranslationResult` model (belongs to CodeObject). Track specific metadata fields: `tokenCount` (Int), `processingType` (String).
    - Create `SAPDocument` model to store chunk references for RAG context mapping. Add a `qdrantId` (String) field to represent the alignment with Qdrant vector storage so vector embeddings can be linked.
  </action>
  <verify>npx prisma validate</verify>
  <done>Schema incorporates all required tracking fields and relations properly.</done>
</task>

<task type="auto">
  <name>Push Schema to Supabase</name>
  <files>prisma/schema.prisma</files>
  <action>
    - Ensure you have the `DIRECT_URL` correctly set up to push to Supabase.
    - Run `npx prisma db push` or `npx prisma migrate dev --name init` to sync the schema with the Supabase database.
    - Generate Prisma Client.
  </action>
  <verify>npx prisma generate</verify>
  <done>Supabase DB matches the Prisma schema and the generated client is ready for backend use.</done>
</task>

## Success Criteria

- [ ] `schema.prisma` contains User, Organization, ModernizationProject, CodeObject, TranslationResult, and SAPDocument models.
- [ ] Specific metadata fields requested by the user are fully typed.
- [ ] Database is successfully scaffolded in Supabase.
