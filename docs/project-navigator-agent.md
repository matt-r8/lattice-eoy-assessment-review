# Project Navigator Agent Documentation

The Project Navigator is your project's institutional memory and knowledge companion that learns, remembers, and guides based on your specific project's evolution.

## Overview

The Project Navigator agent continuously builds a comprehensive understanding of your project through code analysis, documentation review, and conversation learning. It becomes your go-to source for project-specific questions, historical context, and institutional knowledge.

## When to Use Project Navigator

### Always Use For:
- ✅ **Project-Specific Questions**: "Where is the authentication logic?"
- ✅ **Historical Context**: "Why did we choose this architecture?"
- ✅ **Decision Rationale**: "What were the trade-offs for this approach?"
- ✅ **Pattern Queries**: "What's our established error handling pattern?"
- ✅ **Business Logic**: "How does the payment flow work?"
- ✅ **Evolution Tracking**: "How has this feature changed over time?"

### Don't Use For:
- ❌ **General Programming**: Use `software-engineer` instead
- ❌ **System Setup**: Use `solutions-guide` instead
- ❌ **Infrastructure**: Use `platform-engineer` instead
- ❌ **Security Analysis**: Use `cybersecurity-engineer` instead

## Key Capabilities

### 📚 Continuous Learning
The Project Navigator automatically learns from:

```
GIT COMMIT ANALYSIS:
✅ Commit messages for decision context
✅ Code diffs for pattern identification
✅ Pull request descriptions for rationale
✅ Tag annotations for milestone context

DOCUMENTATION MINING:
✅ README updates and project documentation
✅ Code comments and inline documentation
✅ API documentation changes
✅ Architecture decision records (ADRs)

CONVERSATION LEARNING:
✅ Technical discussions about decisions
✅ Architecture explanations and rationale
✅ Business logic clarifications
✅ Performance and scaling considerations
```

### 🧠 Knowledge Synthesis
Builds comprehensive project understanding:

```
DECISION TRACKING:
- Why was technology X chosen over Y?
- What were the constraints at the time?
- How has the decision worked out in practice?
- What related decisions were influenced?

PATTERN RECOGNITION:
- How do we typically handle error cases?
- What's our standard API response format?
- How do we structure database migrations?
- What testing patterns do we follow?

BUSINESS LOGIC MAPPING:
- How does user onboarding flow work?
- What are the payment processing rules?
- How do we handle refunds and cancellations?
- What validation rules apply to user data?
```

### 🔍 Contextual Question Answering
Provides rich, project-specific responses:

```
EXAMPLE INTERACTIONS:

Q: "Where is user authentication implemented?"
A: User authentication is implemented across several components:

MAIN LOGIC: src/auth/AuthService.js (lines 23-156)
- JWT token generation and validation
- Password hashing using bcrypt
- Session management with Redis

MIDDLEWARE: src/middleware/auth.js
- Route protection middleware
- Token extraction from headers
- User context injection

DECISION CONTEXT: We chose JWT over sessions because of our microservices architecture (Decision #003, 2024-08-15). This allows stateless authentication across services.

RELATED PATTERNS: Follows our established error handling pattern with try/catch blocks and centralized error middleware.
```

## Knowledge Base Structure

### Automatic Knowledge Organization
```
.claude/project-knowledge/
├── decisions/              # Architectural and business decisions
│   ├── architecture.md     # System design choices
│   ├── technology.md       # Tech stack decisions
│   ├── business.md         # Business logic decisions
│   ├── performance.md      # Performance-related choices
│   └── security.md         # Security decisions
├── patterns/               # Established patterns and conventions
│   ├── code-patterns.md    # Coding conventions
│   ├── design-patterns.md  # Design pattern usage
│   ├── api-patterns.md     # API design standards
│   └── anti-patterns.md    # Things to avoid
├── evolution/              # Project timeline and changes
│   ├── timeline.md         # Project evolution history
│   ├── milestones.md       # Major project milestones
│   ├── refactoring.md      # Refactoring decisions
│   └── scaling.md          # Scaling strategies
├── business/               # Domain and business logic
│   ├── domain-model.md     # Business entities and rules
│   ├── user-flows.md       # User journey implementations
│   ├── requirements.md     # Requirements evolution
│   └── constraints.md      # Business constraints
└── meta/                   # Knowledge management
    ├── knowledge-index.md  # Searchable index
    ├── session-continuity.md # Cross-session context
    └── learning-log.md     # Learning activity history
```

## Learning Workflows

### Commit-Based Learning
```
TRIGGER: New git commits detected
AUTOMATIC PROCESS:

1. COMMIT MESSAGE ANALYSIS:
   - "feat: implement OAuth2 authentication"
   → Logs new authentication decision
   → Updates security patterns
   → Links to related auth components

2. CODE DIFF ANALYSIS:
   - New error handling pattern detected
   → Documents pattern in code-patterns.md
   → Notes usage context and benefits
   → Cross-references similar implementations

3. FILE CHANGE TRACKING:
   - Database schema changes
   → Updates data model documentation
   → Tracks migration decisions
   → Notes impact on business logic

KNOWLEDGE UPDATES:
✅ Decision log entries created
✅ Pattern library updated
✅ Timeline events recorded
✅ Cross-references established
```

### Documentation-Based Learning
```
TRIGGER: Documentation changes detected
AUTOMATIC PROCESS:

1. README UPDATES:
   - Setup instruction changes
   → Updates project context understanding
   → Notes new dependencies or requirements
   → Tracks deployment process evolution

2. INLINE COMMENTS:
   - Business rule explanations added
   → Enhances domain model understanding
   → Updates business logic documentation
   → Improves decision context

3. API DOCUMENTATION:
   - New endpoint documentation
   → Updates API patterns knowledge
   → Documents request/response formats
   → Notes authentication requirements

KNOWLEDGE UPDATES:
✅ Business context enhanced
✅ Technical patterns documented
✅ Decision rationale captured
✅ Integration patterns noted
```

### Conversation-Based Learning
```
TRIGGER: Technical discussions with user
INTERACTIVE PROCESS:

USER: "I'm implementing user notifications. I chose WebSockets over polling because of real-time requirements and server resource efficiency."

AGENT LEARNING:
1. DECISION CAPTURE:
   - Technology: WebSockets chosen over polling
   - Context: User notifications feature
   - Rationale: Real-time + resource efficiency
   - Date: Current timestamp

2. PATTERN IDENTIFICATION:
   - Real-time communication pattern established
   - WebSocket integration approach documented
   - Performance consideration pattern noted

3. KNOWLEDGE INTEGRATION:
   - Links to existing real-time features
   - Cross-references performance decisions
   - Updates communication patterns library

KNOWLEDGE UPDATES:
✅ decisions/technology.md updated
✅ patterns/communication.md enhanced
✅ evolution/timeline.md recorded
✅ Cross-references established
```

## Question Response Patterns

### Architecture Questions
```
QUESTION TYPE: "Where is [component] implemented?"

RESPONSE STRUCTURE:
1. PRIMARY LOCATION: Specific files and line ranges
2. RELATED COMPONENTS: Connected systems and dependencies
3. DECISION CONTEXT: Why this architecture was chosen
4. EVOLUTION HISTORY: How it has changed over time
5. USAGE PATTERNS: How other parts of the system interact with it

EXAMPLE:
Q: "Where is user authentication implemented?"
A: Authentication is implemented in a distributed pattern:

PRIMARY: src/auth/AuthService.js (lines 23-156)
- Core JWT handling and validation
- Integration with user database

MIDDLEWARE: src/middleware/authMiddleware.js
- Express middleware for route protection
- Token extraction and validation

FRONTEND: src/components/auth/ directory
- Login/logout UI components
- Token storage and management

DECISION CONTEXT: Chose JWT over sessions (Decision #003, Aug 2024) for stateless auth across microservices. Alternative considered was OAuth2, but internal auth was sufficient for current needs.

RELATED PATTERNS: Follows established error handling with centralized middleware.
```

### Decision History Questions
```
QUESTION TYPE: "Why did we choose [technology/approach]?"

RESPONSE STRUCTURE:
1. ORIGINAL DECISION: What was decided and when
2. CONTEXT: Circumstances and requirements at the time
3. ALTERNATIVES: Other options that were considered
4. TRADE-OFFS: Advantages and disadvantages weighed
5. OUTCOME: How the decision has worked in practice

EXAMPLE:
Q: "Why did we choose PostgreSQL over MongoDB?"
A: Database decision made September 15, 2024 (Decision #007):

ORIGINAL CONTEXT:
- Need for ACID transactions in payment processing
- Complex relational data with user accounts, orders, payments
- Team expertise primarily in SQL databases

ALTERNATIVES CONSIDERED:
- MongoDB: Better for document storage, but lacking strong consistency
- MySQL: Familiar, but PostgreSQL's JSON support was compelling
- DynamoDB: Scalable, but vendor lock-in and complex pricing

TRADE-OFFS ACCEPTED:
✅ Strong consistency and ACID compliance
✅ Excellent JSON support for flexible schemas
✅ Team familiarity reduces development time
❌ Potentially more complex scaling than NoSQL
❌ More rigid schema changes

OUTCOME: Has worked well for 6 months. Complex queries are efficient, and JSON columns provide needed flexibility. No scaling issues at current 10K user level.
```

### Pattern Questions
```
QUESTION TYPE: "What's our pattern for [common task]?"

RESPONSE STRUCTURE:
1. ESTABLISHED PATTERN: Standard approach used in the project
2. CODE EXAMPLES: Where pattern is implemented
3. VARIATIONS: Context-specific adaptations
4. EVOLUTION: How pattern has been refined
5. ANTI-PATTERNS: What to avoid based on experience

EXAMPLE:
Q: "What's our error handling pattern?"
A: We use a centralized error handling pattern established in v2.1:

STANDARD PATTERN:
try {
  // Business logic
} catch (error) {
  logger.error('Context-specific message', { error, context });
  throw new AppError(error.message, error.code || 500);
}

IMPLEMENTATION LOCATIONS:
- src/middleware/errorHandler.js: Centralized Express error middleware
- src/utils/AppError.js: Custom error class with proper structure
- src/services/*.js: Service layer implements try/catch pattern

PATTERN EVOLUTION:
v1.0: Basic try/catch with console.log
v2.0: Added centralized error middleware
v2.1: Custom AppError class with error codes
v2.2: Added structured logging with context

VARIATIONS BY CONTEXT:
- Database operations: Include transaction rollback
- API calls: Include retry logic for transient failures
- Authentication: Sanitize error messages for security

ANTI-PATTERNS TO AVOID:
❌ Silent failures (catching without logging)
❌ Generic error messages without context
❌ Exposing internal error details to clients
```

### Business Logic Questions
```
QUESTION TYPE: "How does [business process] work?"

RESPONSE STRUCTURE:
1. BUSINESS FLOW: Step-by-step process description
2. IMPLEMENTATION: Code locations for each step
3. BUSINESS RULES: Domain-specific rules and validations
4. EDGE CASES: Special conditions and handling
5. EVOLUTION: How process has changed over time

EXAMPLE:
Q: "How does the payment processing flow work?"
A: Payment processing follows a multi-step verification flow:

BUSINESS FLOW:
1. Cart validation and pricing calculation
2. Payment method verification
3. Charge authorization with payment provider
4. Order creation and inventory reservation
5. Payment capture and order confirmation
6. Fulfillment initiation

IMPLEMENTATION MAP:
Step 1: src/services/CartService.js → validateCart()
Step 2: src/services/PaymentService.js → verifyPaymentMethod()
Step 3: src/integrations/stripe/StripeService.js → authorizeCharge()
Step 4: src/services/OrderService.js → createOrder()
Step 5: src/services/PaymentService.js → capturePayment()
Step 6: src/services/FulfillmentService.js → initiateShipping()

BUSINESS RULES:
- Maximum order value: $10,000 (configurable)
- Inventory reserved for 15 minutes during payment
- Failed payments allow 3 retry attempts
- Refunds must be processed within 30 days

EDGE CASES:
- Payment authorization succeeds but order creation fails → Auto-refund
- Inventory becomes unavailable during payment → Partial refund
- Payment capture fails after order creation → Manual intervention required

EVOLUTION HISTORY:
v1.0: Simple single-step payment processing
v1.5: Added inventory reservation to prevent overselling
v2.0: Implemented two-phase payment (auth + capture) for better reliability
v2.3: Added partial refund support for inventory issues
```

## Search and Discovery

### Knowledge Search Commands
```
SEARCH CAPABILITIES:

# General search across all knowledge
project-navigator search "authentication"
project-navigator search "database migration"
project-navigator search "error handling"

# Category-specific searches
project-navigator search --category=decisions "api design"
project-navigator search --category=patterns "async operations"
project-navigator search --category=business "user onboarding"

# Time-based searches
project-navigator search --since="2024-09-01" "performance"
project-navigator search --between="2024-08-01,2024-09-01" "refactoring"

# Contextual queries
project-navigator ask "What performance optimizations have we made?"
project-navigator ask "How has our authentication evolved?"
project-navigator ask "What are our deployment patterns?"
```

### Knowledge Discovery
```
PROACTIVE KNOWLEDGE SURFACING:

RELATED KNOWLEDGE SUGGESTIONS:
When you ask about authentication, I also found:
- Related security decisions about password policies
- Integration patterns with user management
- Performance considerations for JWT validation

PATTERN CONNECTIONS:
The error handling pattern you're asking about connects to:
- Logging patterns established in August
- API response format standards
- Monitoring and alerting setup decisions

EVOLUTION INSIGHTS:
This business logic has evolved significantly:
- Originally implemented in v1.2 (simple approach)
- Major refactoring in v2.0 (added validation)
- Recent optimization in v2.5 (performance improvement)
```

## Integration with Development Workflow

### Automatic Context for Other Agents
```
WHEN software-engineer AGENT IS INVOKED:
Project Navigator automatically provides:
- Relevant code patterns for the task
- Historical decisions affecting the implementation
- Business logic context and constraints
- Performance considerations from past work

ENHANCED AGENT BRIEFING:
Task: Implement user password reset
Context from Project Navigator:
- Authentication pattern: JWT-based (Decision #003)
- Security requirements: 2FA required for admin users
- Email service: SendGrid integration (src/services/EmailService.js)
- Error handling: Use AppError class with specific codes
- Business rule: Password reset links expire in 1 hour
```

### Learning from Agent Work
```
WHEN SPECIALIZED AGENTS COMPLETE TASKS:
Project Navigator captures:
- Implementation patterns used
- Decisions made during development
- Performance considerations discovered
- Business logic insights gained

EXAMPLE LEARNING CYCLE:
1. software-engineer implements new API endpoint
2. Project Navigator learns:
   - New API pattern established
   - Authentication method used
   - Error handling approach taken
   - Performance considerations noted
3. Knowledge base updated with:
   - API patterns documentation
   - Security decision context
   - Implementation examples
   - Integration guidance for future endpoints
```

## Knowledge Quality and Maintenance

### Automatic Quality Assurance
```
KNOWLEDGE VALIDATION:
- Cross-reference consistency checking
- Decision timeline validation
- Pattern usage verification
- Business logic coherence review

QUALITY METRICS:
- Knowledge coverage completeness
- Decision context richness
- Pattern documentation accuracy
- Cross-reference integrity

MAINTENANCE ACTIVITIES:
- Archive outdated decisions
- Update pattern examples
- Refine business logic documentation
- Enhance cross-references
```

### Manual Knowledge Enhancement
```
USER-DRIVEN IMPROVEMENTS:

EXPLICIT KNOWLEDGE ADDITION:
"Project Navigator, document that we chose Redis for session storage because of its performance and our existing Redis infrastructure."

PATTERN CLARIFICATION:
"Add to our error handling pattern that database errors should always include the table name in the log message."

DECISION CONTEXT:
"Update the authentication decision - we're now considering moving to OAuth2 in Q2 2025 due to SSO requirements."

BUSINESS RULE UPDATES:
"The maximum order value has been increased to $25,000 for premium customers as of November 1st."
```

## Advanced Features

### Cross-Session Continuity
```
SESSION BRIDGING:
When you return to work, Project Navigator provides:
- Context from previous sessions
- Decisions made since last conversation
- New patterns identified in recent commits
- Updated business logic understanding

EXAMPLE SESSION RESUMPTION:
"Welcome back! Since our last conversation:
- 3 new commits analyzed with payment processing improvements
- Updated error handling pattern identified in OrderService
- New business rule added for international shipping
- Performance optimization implemented for database queries

What would you like to explore today?"
```

### Predictive Insights
```
PATTERN-BASED PREDICTIONS:
"Based on your recent work on user notifications, you might need:
- WebSocket connection management patterns (established in chat feature)
- Error handling for real-time connections (see ConnectionService.js)
- Performance considerations for high-frequency updates"

ARCHITECTURE GUIDANCE:
"For the new analytics feature, consider:
- Our established event-driven pattern (UserActivityService)
- Data pipeline decisions from reporting module
- Performance lessons from metrics dashboard implementation"
```

### Knowledge Export and Sharing
```
TEAM KNOWLEDGE SHARING:
# Generate onboarding documentation
project-navigator export --type=onboarding --format=markdown

# Create architecture decision record
project-navigator export --decisions --since="2024-09-01"

# Export patterns guide
project-navigator export --patterns --category=api

# Generate business logic documentation
project-navigator export --business-logic --format=confluence
```

The Project Navigator becomes your project's institutional memory - preserving the why behind every decision and helping you build on the knowledge gained throughout your project's evolution!