# Database Relationships for Inspection Scheduling System

This document explains the relationships between the various tables in the database

## Table Structure and Relationship

### 1. Inspector and Qualification
- **Tables Involved**: `Inspector`, `Qualification`, `Inspector_Qualification`
- **Relationship Type**: Many-to-Many
   - **Description**: Each inspector can hold multiple qualifications, and each qualification can apply to multiple inspectors.
   - **Implementation**: 
     - The `Inspector_Qualification` table acts as a **junction table** to establish a many-to-many relationship between `Inspector` and `Qualification`.
     - `Inspector_Qualification` includes:
       - `inspector_id` - Foreign key referencing `Inspector(id)`.
       - `qualification_code` - Foreign key referencing `Qualification(code)`.

### 2. Building_Consent and Inspection
   - **Tables Involved**: `Building_Consent`, `Inspection`
   - **Relationship Type**: One-to-Many
   - **Description**: Each building consent can have multiple inspections assigned to it, such as inspections at different stages of the construction process.
   - **Implementation**:
     - `Inspection` includes:
       - `bc_number` - Foreign key referencing `Building_Consent(bc_number)`.

### 3. Inspector and Inspection
   - **Tables Involved**: `Inspector`, `Inspection`
   - **Relationship Type**: One-to-Many
   - **Description**: Each inspection may have a single assigned inspector, but an inspector can oversee multiple inspections. An inspection does not require an inspector at the time of creation.
   - **Implementation**:
     - `Inspection` includes:
       - `inspector_id` - Foreign key referencing `Inspector(id)`, allowing nullable values for unassigned inspections.

## Summary of Relationships
1. **Many-to-Many**: `Inspector` and `Qualification` (through `Inspector_Qualification`).
2. **One-to-Many**: `Building_Consent` and `Inspection`.
3. **One-to-Many**: `Inspector` and `Inspection`.