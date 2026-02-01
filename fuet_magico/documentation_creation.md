# Cubix One - Documentation Creation Standard

**Purpose:** This document defines the standard structure and guidelines for creating documentation for all features in Cubix One.  
**Audience:** AI assistants and developers creating new feature documentation.  
**Developer:** [Bruno Coelho](https://github.com/BrunoKorpuzCoelho)  
**Last Updated:** November 23, 2025

---

## Overview

All Cubix One features must be documented following this standard structure. This ensures:

- ✅ **Consistency** - All documentation follows the same format
- ✅ **AI Searchability** - Keywords and structure optimized for AI search
- ✅ **Clarity** - Both technical and non-technical explanations
- ✅ **Granularity** - One document per feature (not monolithic docs)
- ✅ **Completeness** - All aspects covered systematically

---

## File Naming Convention

### Pattern

```
[sequence_number]_[feature_name_in_snake_case].md
```

### Rules

1. **Always use English** - Files must have English names for AI searchability
2. **Use lowercase** - All letters lowercase
3. **Use underscores** - Separate words with `_` (not hyphens or spaces)
4. **Sequential numbering** - Start with `01`, `02`, etc. (with leading zero)
5. **Descriptive names** - Name should clearly indicate the feature
6. **One feature per file** - Each file documents ONE specific feature

### Examples

✅ **Good:**

- `01_basemodel_base_fields.md`
- `02_basemodel_relationships.md`
- `03_basemodel_crud_operations.md`
- `08_database_connection_and_sqlalchemy_configuration.md`
- `15_event_system_and_hooks.md`

❌ **Bad:**

- `BaseModel.md` - No number, not snake_case
- `base-model-fields.md` - Hyphens instead of underscores
- `01-BaseModelFields.md` - Mixed case, hyphens
- `basemodel.md` - No number, too generic
- `documentação.md` - Not in English

---

## Document Structure Template

Every documentation file must follow this exact structure:

```markdown
# [Feature Name]

**Phase:** [Phase Number and Name]  
**Feature:** [Brief feature description]  
**Status:** [✅ Complete | 🚧 In Progress | 📋 Planned]  
**Developer:** [Bruno Coelho](https://github.com/BrunoKorpuzCoelho)  
**Location:** `[file/path/to/implementation.py]`

---

## Overview

**What this feature does:** [Non-technical explanation in simple language. Anyone should be able to understand what this feature does and why it exists. Use real-world examples. 2-4 sentences.]

**Technical details:** [Technical explanation for developers. What the feature is from a technical perspective. 1-2 sentences.]

**Keywords for AI search:** [comma-separated list of keywords that AI would use to find this documentation]

---

## [Main Section 1]

[Content organized in clear sections...]

---

## [Main Section 2]

[Content with code examples, tables, etc...]

---

## [Additional Sections as Needed]

---

## Best Practices

[Guidelines for using this feature correctly]

---

## Common Patterns

[Typical usage patterns and examples]

---

## Troubleshooting

[Common issues and solutions]

---

## Related Documentation

- [Link to related doc 1](./relative_path.md)
- [Link to related doc 2](./relative_path.md)

---

**Last Updated:** [Date in format: November 23, 2025]  
**Version:** [Version number: 1.0]
```

---

## Required Sections Explained

### 1. Header Metadata

```markdown
# [Feature Name]

**Phase:** 1.1 Database & ORM Foundation  
**Feature:** Brief description of what this feature is  
**Status:** ✅ Complete  
**Developer:** [Bruno Coelho](https://github.com/BrunoKorpuzCoelho)  
**Location:** `python/platform/config/model_system/model_base.py`
```

**Rules:**

- Feature name in title case with hyphens/spaces (not snake_case)
- Phase must reference the development roadmap
- Status uses emoji indicators: ✅ Complete, 🚧 In Progress, 📋 Planned
- Developer must always be: **Developer:** [Bruno Coelho](https://github.com/BrunoKorpuzCoelho)
- Location shows the main implementation file(s)

### 2. Overview Section (CRITICAL)

This is the **most important section** - it has three required parts:

#### Part A: "What this feature does" (Non-Technical)

```markdown
**What this feature does:** Every model in Cubix One automatically inherits 6 essential fields from BaseModel. These fields provide automatic record identification (id), soft delete capability (active), audit timestamps (create_date, write_date), and user tracking (create_uid, write_uid). You never need to manually define these fields - they're always there, working automatically.
```

**Requirements:**

- Start with "What this feature does:"
- Written in **simple, non-technical language**
- Anyone (even non-developers) should understand
- 2-4 sentences maximum
- Use real-world examples when possible
- Explain the "why" not just the "what"

#### Part B: "Technical details" (Technical)

```markdown
**Technical details:** Every model in Cubix One inherits from `BaseModel`, which automatically provides 6 standard fields for identification, audit tracking, and soft delete functionality.
```

**Requirements:**

- Start with "Technical details:"
- Technical explanation for developers
- 1-2 sentences maximum
- Can use technical terms
- Describes implementation approach

#### Part C: "Keywords for AI search" (Critical for AI)

```markdown
**Keywords for AI search:** base fields, id field, active field, soft delete, create_date, write_date, create_uid, write_uid, audit tracking, automatic timestamps, user tracking
```

**Requirements:**

- Start with "Keywords for AI search:"
- Comma-separated list of keywords
- Think about what an AI assistant would search for
- Include technical terms, function names, concepts, common synonyms
- 8-15 keywords recommended
- No special characters or quotes

**Example Keywords by Feature Type:**

| Feature Type    | Example Keywords                                                                            |
| --------------- | ------------------------------------------------------------------------------------------- |
| Database/ORM    | sqlalchemy setup, database connection, engine configuration, connection pooling, postgresql |
| CRUD Operations | create record, save model, update data, delete record, write method, destroy method         |
| Relationships   | many2one, one2many, many2many, foreign key, belongs to, has many, associations              |
| Query Methods   | where clause, filter records, find by, query builder, search records, pagination            |
| Lifecycle Hooks | before save, after update, callbacks, event hooks, lifecycle events                         |

### 3. Main Content Sections

Organize content logically with clear headings:

```markdown
## The 6 Base Fields

### Field Definitions

[Code examples...]

### Field Reference Table

| Field | Type | Description |
| ----- | ---- | ----------- |
| ...   | ...  | ...         |

---

## Field Details

### 1. id (Primary Key)

[Detailed explanation...]

### 2. active (Soft Delete)

[Detailed explanation...]
```

**Rules:**

- Use `##` for major sections
- Use `###` for subsections
- Use `---` horizontal lines to separate major sections
- Include code examples for every concept
- Use tables for structured data
- Use lists for multiple items

### 4. Code Examples

Every concept must have code examples:

````markdown
### Basic Usage

​```python

# Simple creation

user = User.create({
'name': 'John Doe',
'email': 'john@example.com',
'active': True
})

print(user.id) # Auto-generated ID: 1
print(user.create_date) # Auto: 2025-11-23 14:30:00
​```
````

**Rules:**

- Use proper syntax highlighting (```python)
- Include comments explaining what code does
- Show both the code AND expected output
- Start with simple examples, then advanced
- Show both ✅ good and ❌ bad examples when relevant

### 5. Comparison Tables

Use tables to compare options or show features:

```markdown
| Method      | Purpose                 | Returns | Alias     |
| ----------- | ----------------------- | ------- | --------- |
| `create()`  | Create new record       | Model   | -         |
| `save()`    | Save (create or update) | Model   | -         |
| `update()`  | Update existing record  | Model   | `write()` |
| `destroy()` | Delete record           | Boolean | -         |
```

**Rules:**

- Always include header row
- Use `---` for header separator
- Use `|` for column separators
- Keep columns aligned for readability
- Use backticks for code elements

### 6. Best Practices Section

````markdown
## Best Practices

### 1. Always Use Soft Delete

​```python

# ✅ Good - Soft delete

user.update({'active': False})

# ❌ Bad - Hard delete (unless required)

user.destroy()
​```

### 2. Never Manually Set Timestamps

​```python

# ❌ Bad - Timestamps are automatic

product.create_date = datetime.now()

# ✅ Good - Let database handle it

product = Product.create({'name': 'Laptop'})
​```
````

**Rules:**

- Number each best practice
- Show ✅ good and ❌ bad examples
- Explain WHY it's a best practice
- Keep each practice focused on one concept

### 7. Troubleshooting Section

````markdown
## Troubleshooting

### Issue: create_uid is NULL

**Problem:**

​`python
product = Product.create({'name': 'Mouse'})
print(product.create_uid)  # None
​`

**Causes:**

1. No Flask request context
2. User not authenticated
3. Running in background job/cron

**Solutions:**

​```python

# Solution 1: Explicitly set user

Product.create({
'name': 'Mouse',
'create_uid': 1 # System user
})
​```
````

**Rules:**

- Each issue has: Problem, Causes, Solutions
- Show code that demonstrates the problem
- List all possible causes
- Provide working code solutions
- Use realistic scenarios

### 8. Related Documentation

```markdown
## Related Documentation

- [BaseModel Base Fields](./01_basemodel_base_fields.md)
- [BaseModel Relationships](./02_basemodel_relationships.md)
- [BaseModel CRUD Operations](./03_basemodel_crud_operations.md)
- [Database Connection](./08_database_connection_and_sqlalchemy_configuration.md)
```

**Rules:**

- Link to related features
- Use relative paths (`./../`)
- Include features that are dependencies
- Include features that build on this one

### 9. Footer

```markdown
---

**Last Updated:** November 23, 2025  
**Version:** 1.0
```

**Rules:**

- Always include last updated date
- Use format: `Month DD, YYYY`
- Include version number
- Separated by `---` horizontal line

---

## Content Guidelines

### Language Style

1. **Overview "What this feature does":**

   - ✅ Simple, non-technical language
   - ✅ Real-world examples ("like connecting an Order to a Customer")
   - ✅ Explain the benefit/purpose
   - ❌ No technical jargon
   - ❌ No implementation details

2. **Technical Details:**

   - ✅ Technical terms allowed
   - ✅ Reference specific classes/functions
   - ✅ Implementation approach
   - ❌ Don't repeat "what it does"

3. **Main Content:**
   - ✅ Balance between explanation and code
   - ✅ Start simple, progress to advanced
   - ✅ Use bullet points and lists
   - ✅ Include visual elements (tables, diagrams)

### Code Examples Guidelines

````markdown
## Code Example Template

### [Feature Name]

[Brief explanation of what this example demonstrates]

​```python

# Step-by-step comments explaining each part

result = SomeModel.some_method({
'field': 'value' # Explain this parameter
})

# Show the output

print(result.id) # 1
​```

**Explanation:**

- Point 1: What happens here
- Point 2: Why this works
- Point 3: What to watch out for
````

**Rules:**

- Every code block must have context
- Add comments explaining non-obvious code
- Show expected output when relevant
- Follow up with explanation if needed
- Use realistic data (not foo/bar)

### Table Guidelines

**Configuration/Options Table:**

```markdown
| Option         | Description                      | Default | Required |
| -------------- | -------------------------------- | ------- | -------- |
| `pool_size`    | Number of persistent connections | 10      | No       |
| `max_overflow` | Extra connections allowed        | 20      | No       |
```

**Method/Function Table:**

```markdown
| Method     | Purpose           | Parameters | Returns |
| ---------- | ----------------- | ---------- | ------- |
| `create()` | Create new record | dict       | Model   |
| `update()` | Update record     | dict       | Model   |
```

**Feature Comparison Table:**

```markdown
| Feature     | PostgreSQL | SQLite | MySQL   |
| ----------- | ---------- | ------ | ------- |
| Production  | ✅ Primary | ❌     | 📋 Prep |
| Development | ✅ Primary | ❌     | 📋 Prep |
| Testing     | ✅ Primary | ❌     | 📋 Prep |
```

**Rules:**

- Use emojis for status (✅ ❌ 🚧 📋 ⚠️)
- Keep columns aligned
- Use backticks for code elements
- Include header row separator

---

## Keyword Selection Strategy

The "Keywords for AI search" section is **critical** for AI assistants to find relevant documentation.

### Keyword Categories

#### 1. Feature Name Variations

```
Primary: create record
Variations: create model, new record, insert record, save new record
```

#### 2. Function/Method Names

```
create(), save(), update(), write(), destroy(), delete()
```

#### 3. Technical Concepts

```
CRUD operations, ORM, SQLAlchemy, database connection, connection pooling
```

#### 4. Common Search Terms

```
how to create, how to update, how to delete, database setup
```

#### 5. Related Technologies

```
PostgreSQL, SQLite, Flask-SQLAlchemy, Alembic, Flask-Migrate
```

#### 6. Problem/Solution Terms

```
soft delete, user tracking, audit trail, lifecycle hooks, event system
```

### Keyword Examples by Feature Type

**BaseModel Fields:**

```
base fields, id field, active field, soft delete, create_date, write_date,
create_uid, write_uid, audit tracking, automatic timestamps, user tracking
```

**Relationships:**

```
many2one, one2many, many2many, relationships, foreign key, belongs to,
has many, associations, sqlalchemy relationships, bidirectional relationships
```

**CRUD Operations:**

```
create record, save model, update data, delete record, write method,
destroy method, insert, modify, remove, persist
```

**Database Connection:**

```
sqlalchemy setup, database connection, engine configuration, database URI,
connection pooling, postgresql, flask-sqlalchemy, database setup
```

**Query Methods:**

```
where clause, filter records, find by, query builder, search records,
pagination, sorting, find, search, query
```

**Bulk Operations:**

```
bulk create, bulk update, bulk delete, batch operations, mass insert,
performance optimization, high volume
```

**Lifecycle Hooks:**

```
before save, after save, before update, after update, lifecycle hooks,
callbacks, event hooks, triggers, lifecycle events
```

### How to Generate Keywords

1. **Start with the feature name** - Include the main feature and variations
2. **Add all function/method names** - Everything a developer might call
3. **Think like a user** - "How would someone ask for this?"
4. **Include related concepts** - What else is this connected to?
5. **Add technical terms** - Class names, patterns, technologies
6. **Consider problems solved** - What issues does this fix?
7. **Review 8-15 keywords** - Not too few, not too many

### Keyword Testing

Ask yourself:

- ✅ Would an AI search for "how to create a record" find this?
- ✅ Would searching for "many2one" find the relationships doc?
- ✅ Would searching for "connection pooling" find database setup?
- ✅ Would searching for "soft delete" find base fields?

---

## Document Organization Patterns

### Pattern 1: Feature Overview Documents

For features with multiple capabilities (like BaseModel):

```
01_basemodel_base_fields.md         # The 6 automatic fields
02_basemodel_relationships.md       # many2one, one2many, many2many
03_basemodel_crud_operations.md     # create, save, update, destroy
04_basemodel_query_methods.md       # where, find_by, browse, etc.
05_basemodel_bulk_operations.md     # bulk_create, bulk_update, etc.
06_basemodel_lifecycle_hooks.md     # before/after hooks
07_basemodel_recordset_operations.md # RecordSet methods
```

**When to use:** Feature has 5+ distinct capabilities that each need detailed explanation

### Pattern 2: Configuration Documents

For setup and configuration topics:

```
08_database_connection_and_sqlalchemy_configuration.md
09_database_session_management.md
10_transaction_management.md
11_read_replicas_configuration.md
```

**When to use:** Focus is on setup, configuration, infrastructure

### Pattern 3: Integration Documents

For features that connect systems:

```
15_event_system_and_hooks.md
16_ai_agent_integration.md
17_audit_trail_system.md
```

**When to use:** Feature connects multiple parts of the system

### Pattern 4: Service/Module Documents

For standalone services:

```
20_background_job_system.md
21_email_service.md
22_file_storage_service.md
```

**When to use:** Feature is a standalone service/module

---

## Quality Checklist

Before considering documentation complete, verify:

### Structure ✅

- [ ] File name follows convention (number_snake_case.md)
- [ ] File name is in English
- [ ] Header metadata complete (Phase, Feature, Status, Location)
- [ ] Overview has all 3 parts (What it does, Technical details, Keywords)
- [ ] Footer has date and version

### Content ✅

- [ ] "What this feature does" is non-technical and clear
- [ ] "Technical details" is concise (1-2 sentences)
- [ ] Keywords include 8-15 relevant search terms
- [ ] Every concept has code examples
- [ ] Code examples have comments and expected output
- [ ] Tables are properly formatted
- [ ] Best Practices section exists
- [ ] Troubleshooting section exists
- [ ] Related Documentation links exist

### Clarity ✅

- [ ] Non-developers can understand the overview
- [ ] Developers can understand technical implementation
- [ ] Examples progress from simple to advanced
- [ ] All code examples are realistic (not foo/bar)
- [ ] Technical terms are explained on first use

### Completeness ✅

- [ ] All major capabilities documented
- [ ] Common use cases covered
- [ ] Edge cases explained
- [ ] Known limitations mentioned
- [ ] Related features referenced

### AI Searchability ✅

- [ ] Keywords cover all search variations
- [ ] Function/method names included
- [ ] Common problem terms included
- [ ] Related technology names included
- [ ] File name reflects content for search

---

## Examples Reference

### ✅ Excellent Documentation Examples

Study these files as templates:

1. **`01_basemodel_base_fields.md`**

   - Clear overview with non-technical explanation
   - Comprehensive coverage of all 6 fields
   - Excellent code examples with output
   - Strong troubleshooting section

2. **`03_basemodel_crud_operations.md`**

   - Perfect method comparison table
   - Clear CRUD operation explanations
   - Good/bad example patterns
   - Realistic use cases

3. **`08_database_connection_and_sqlalchemy_configuration.md`**
   - Excellent architecture diagram (text)
   - Configuration tables with explanations
   - Environment-specific examples
   - Performance optimization section

### Common Patterns to Follow

**Pattern: Method Documentation**

```markdown
## method_name() - Brief Description

### Signature

[Show the method signature]

### Basic Usage

[Simple example]

### Advanced Usage

[Complex example]

### Parameters

[Table of parameters]

### Return Value

[What it returns]

### Automatic Behavior

[What happens automatically]
```

**Pattern: Configuration Documentation**

```markdown
## Configuration Option

### What It Does

[Simple explanation]

### Default Value

[Default setting]

### Recommended Settings

[Environment-specific recommendations]

### Example

[Code example]

### Impact

[What happens when you change this]
```

---

## Documentation Workflow

### Step 1: Verify Implementation

Before writing documentation:

1. ✅ Feature is implemented and working
2. ✅ Code is tested and stable
3. ✅ File locations are known
4. ✅ All capabilities are identified

### Step 2: Determine File Name

```
[next_sequence_number]_[feature_name_in_snake_case].md
```

Example: `09_database_session_management.md`

### Step 3: Create File Structure

Copy this template:

```markdown
# [Feature Name]

**Phase:** [Phase Number and Name]  
**Feature:** [Brief description]  
**Status:** ✅ Complete  
**Location:** `[file/path.py]`

---

## Overview

**What this feature does:** [Non-technical explanation]

**Technical details:** [Technical explanation]

**Keywords for AI search:** [keywords]

---

[Main content sections...]

---

## Best Practices

---

## Troubleshooting

---

## Related Documentation

---

**Last Updated:** November 23, 2025  
**Version:** 1.0
```

### Step 4: Write Overview Section

1. **What it does (non-technical):**

   - Explain in simple language
   - Use real-world examples
   - 2-4 sentences
   - Anyone can understand

2. **Technical details:**

   - Technical summary
   - 1-2 sentences
   - For developers

3. **Keywords:**
   - 8-15 keywords
   - All search variations
   - Function names
   - Related concepts

### Step 5: Write Main Content

1. Start with simple concepts
2. Add code examples for each
3. Build to advanced topics
4. Include tables for comparisons
5. Add diagrams if helpful (ASCII art is fine)

### Step 6: Add Support Sections

1. **Best Practices:** Do's and don'ts
2. **Common Patterns:** Typical usage scenarios
3. **Troubleshooting:** Issues and solutions
4. **Related Docs:** Links to connected features

### Step 7: Review Quality Checklist

Go through the quality checklist above and verify all items.

### Step 8: Update Related Documentation

1. Update README.md with link to new doc
2. Add links in related documents
3. Update any index/navigation files

---

## Special Cases

### Documenting Deprecated Features

```markdown
# [Feature Name] (DEPRECATED)

⚠️ **DEPRECATED:** This feature is deprecated as of [date] and will be removed in version [X.X]. Use [alternative] instead.

**Migration Guide:** [Link to migration guide]

---

## Overview

[Standard documentation...]
```

### Documenting Experimental Features

```markdown
# [Feature Name] (EXPERIMENTAL)

🧪 **EXPERIMENTAL:** This feature is experimental and may change in future versions. Use in production at your own risk.

---

## Overview

[Standard documentation...]
```

### Documenting Planned Features

```markdown
# [Feature Name]

**Status:** 📋 Planned

This feature is planned but not yet implemented.

## Planned Capabilities

- Capability 1
- Capability 2

## Expected Release

Version [X.X] - [Quarter/Year]

---
```

---

## Anti-Patterns (What NOT to Do)

### ❌ Monolithic Documents

**Bad:**

```
basemodel_complete_documentation.md (5000 lines)
```

**Good:**

```
01_basemodel_base_fields.md
02_basemodel_relationships.md
03_basemodel_crud_operations.md
```

### ❌ Missing Overview

**Bad:**

```markdown
# Feature

## Implementation

[Technical details only]
```

**Good:**

```markdown
# Feature

## Overview

**What this feature does:** [Simple explanation]
**Technical details:** [Technical explanation]
**Keywords for AI search:** [keywords]
```

### ❌ No Code Examples

**Bad:**

```markdown
The create method creates a new record.
```

**Good:**

```markdown
The create method creates a new record:

​`python
user = User.create({'name': 'John'})
print(user.id)  # 1
​`
```

### ❌ No Keywords

**Bad:**

```markdown
## Overview

This feature handles database connections.
```

**Good:**

```markdown
## Overview

**Keywords for AI search:** database connection, sqlalchemy setup, connection pooling, postgresql
```

### ❌ Non-English Names

**Bad:**

```
documentação_basemodel.md
01_campos_base.md
```

**Good:**

```
01_basemodel_base_fields.md
02_basemodel_relationships.md
```

---

## Maintenance

### Updating Existing Documentation

When updating documentation:

1. ✅ Update "Last Updated" date
2. ✅ Increment version if major changes
3. ✅ Add deprecation notices if needed
4. ✅ Update related documentation links
5. ✅ Verify all code examples still work
6. ✅ Update keywords if feature expanded

### Version Numbering

- `1.0` - Initial complete documentation
- `1.1` - Minor updates (typos, clarifications)
- `1.2` - Added new sections or examples
- `2.0` - Major restructuring or feature changes

---

## Summary

This standard ensures:

1. **Consistency** - All docs follow same structure
2. **Discoverability** - AI can find relevant docs via keywords
3. **Clarity** - Both technical and non-technical audiences served
4. **Completeness** - All aspects systematically covered
5. **Maintainability** - Easy to update and extend

**Remember:**

- One feature = One file
- English file names always
- Non-technical overview required
- Keywords are critical for AI search
- Code examples for everything
- Best practices and troubleshooting sections mandatory

---

**Last Updated:** November 23, 2025  
**Version:** 1.0
