# Feature Specification: 外包员工工时填报系统 (Outsourced Employee Work Reporting)

> Status: Active  
> Canonical Source of Truth: `specs/work-report/spec.md`  

## 1. Problem & Context

Currently, outsourced employees report their daily working hours via disconnected spreadsheets, causing delays in monthly billing reconciliations, frequent accounting disputes, and lack of real-time visibility into vendor labor capacity. We need a unified, lightweight work reporting feature integrated with our enterprise vendor management system.

## 2. Goals & Non-Goals

### Goals
- Allow outsourced employees to record and submit daily project hours transparently.
- Enforce strict legal and corporate time-tracking constraints (e.g. daily maximums and submission time limits).
- Give department managers real-time visibility into outsourced resource utilization within their respective departments.

### Non-Goals
- Automated payroll calculation or direct bank payouts (handled by the ERP finance module).
- Biometric hardware time-clock synchronization for on-premise attendance.

## 3. User Stories

### User Story 1: Daily Work Hour Submission
As an outsourced employee,  
I want to submit my daily working hours and project notes,  
So that my work contributions can be recorded for billing and performance verification.

#### Acceptance Scenarios
1. **Successful standard submission**:
   Given today is September 19, 2026, and I have not submitted hours for today yet,  
   When I submit 8.0 working hours under project "Atlas",  
   Then the record is saved in "Submitted" status, and my daily summary updates to 8.0 hours.

2. **Exceeding maximum daily limit**:
   Given I already have 20.0 confirmed working hours logged for September 19, 2026,  
   When I attempt to submit an additional 5.0 hours for the same date,  
   Then the system blocks the submission and displays an error explaining the 24-hour daily threshold has been exceeded.

### User Story 2: Reviewing Personal Historical Reports
As an outsourced employee,  
I want to browse my historical daily reports by month,  
So that I can verify my attendance and reconcile discrepancies with my agency.

#### Acceptance Scenarios
1. **Browse history within editable window**:
   Given I have logged reports in the current calendar week,  
   When I navigate to the history view,  
   Then I see a chronological list of all submitted hours with project breakdowns.

## 4. Requirements

- **FR-001**: Users MUST view their own work reports and historical submission logs.
- **FR-002**: Users MUST NOT report more than 24 hours per day across all assigned projects.
- **FR-003**: Historical reports older than N days cannot be modified or deleted by employees.
- **FR-004**: Department managers CAN view work reports for all members in their department, but CANNOT view reports from other departments.
- **FR-005**: Reports transition from 'Draft' to 'Submitted' upon user submission; submitted reports enter a read-only lock for normal users.
- **FR-006**: Minimum reporting increment MUST be 0.5 hours (30 minutes).
- **FR-007**: `[NEEDS CLARIFICATION: The exact value of N in FR-003 is pending decision by Corporate Compliance: 7 calendar days vs 30 calendar days?]`

## 5. Edge Cases
- Cross-midnight reporting: Any work spanning across 00:00 must be attributed to the date on which the shift commenced according to the local corporate timezone (UTC+8).
- Disconnected network: If connectivity drops during submission, input data must be preserved in client draft memory without duplication.
